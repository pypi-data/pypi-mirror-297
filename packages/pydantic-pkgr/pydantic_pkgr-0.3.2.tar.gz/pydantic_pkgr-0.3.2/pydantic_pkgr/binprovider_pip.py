#!/usr/bin/env python
__package__ = "pydantic_pkgr"

import sys
import site
import shutil
import sysconfig
import venv

from pathlib import Path
from typing import Optional, List

from pydantic import model_validator, TypeAdapter, computed_field

from .base_types import BinProviderName, PATHStr, BinName, InstallArgs, HostBinPath, bin_abspath, path_is_executable
from .binprovider import BinProvider


class PipProvider(BinProvider):
    name: BinProviderName = "pip"
    INSTALLER_BIN: BinName = "pip"
    
    PATH: PATHStr = ''
    
    pip_install_venv: Optional[Path] = None                                                 # None = system site-packages (user or global), otherwise it's a path e.g. DATA_DIR/lib/pip/venv
    pip_install_args: List[str] = ["--no-input", "--disable-pip-version-check", "--quiet"]  # extra args for pip install ... e.g. --upgrade

    @computed_field
    @property
    def INSTALLER_BIN_ABSPATH(self) -> HostBinPath | None:
        """Actual absolute path of the underlying package manager (e.g. /usr/local/bin/npm)"""
        if self.pip_install_venv:
            assert self.INSTALLER_BIN != 'pipx', "Cannot use pipx with pip_install_venv"
            
            # use venv pip
            venv_pip_path = self.pip_install_venv / "bin" / self.INSTALLER_BIN
            if path_is_executable(venv_pip_path):
                abspath = str(venv_pip_path)
        else:
            # use system pip
            abspath = bin_abspath(self.INSTALLER_BIN, PATH=None) or shutil.which(self.INSTALLER_BIN)  # find self.INSTALLER_BIN abspath using environment path
            if not abspath:
                # underlying package manager not found on this host, return None
                return None
        return TypeAdapter(HostBinPath).validate_python(abspath)

    @model_validator(mode="after")
    def load_PATH_from_pip_sitepackages(self):
        PATH = self.PATH

        if self.pip_install_venv:
            # restrict PATH to only use venv
            pip_bin_dirs = {str(self.pip_install_venv / "bin")}
        else:
            # autodetect system python paths
            pip_bin_dirs = {
                * (
                    str(Path(d).parent.parent.parent / "bin") for d in site.getsitepackages()
                ),  # /opt/homebrew/opt/python@3.11/Frameworks/Python.framework/Versions/3.11/bin
                str(Path(site.getusersitepackages()).parent.parent.parent / "bin"),  # /Users/squash/Library/Python/3.9/bin
                sysconfig.get_path("scripts"),  # /opt/homebrew/bin
            }

            if self.INSTALLER_BIN == "pipx":
                if self.INSTALLER_BIN_ABSPATH and shutil.which(self.INSTALLER_BIN_ABSPATH):
                    proc = self.exec(bin_name=self.INSTALLER_BIN_ABSPATH, cmd=["debug"])
                    if proc.returncode == 0:
                        PIPX_BIN_DIR = proc.stdout.strip().split("PIPX_BIN_DIR=")[-1].split("\n", 1)[0]
                        paths.add(PIPX_BIN_DIR)

        for bin_dir in pip_bin_dirs:
            if bin_dir not in PATH:
                PATH = ":".join([*PATH.split(":"), bin_dir])
        self.PATH = TypeAdapter(PATHStr).validate_python(PATH)
        return self
    
    def init_venv(self):
        """create pip venv dir if needed"""
        if self.pip_install_venv:
            self.pip_install_venv.parent.mkdir(parents=True, exist_ok=True)
            
            # create venv in pip_install_venv if it doesnt exist
            if not (self.pip_install_venv / "bin" / "python").is_file():
                venv.create(
                    str(self.pip_install_venv),
                    system_site_packages=False,
                    clear=True,
                    symlinks=True,
                    with_pip=True,
                    upgrade_deps=True,
                )

    def on_install(self, bin_name: str, packages: Optional[InstallArgs] = None, **context) -> str:
        packages = packages or self.on_get_packages(bin_name)
        if not self.INSTALLER_BIN_ABSPATH:
            raise Exception(
                f"{self.__class__.__name__} install method is not available on this host ({self.INSTALLER_BIN} not found in $PATH)"
            )

        # print(f'[*] {self.__class__.__name__}: Installing {bin_name}: {self.INSTALLER_BIN_ABSPATH} install {packages}')

        if self.pip_install_venv:
            self.init_venv()

        proc = self.exec(bin_name=self.INSTALLER_BIN_ABSPATH, cmd=["install", *self.pip_install_args, *packages])

        if proc.returncode != 0:
            print(proc.stdout.strip())
            print(proc.stderr.strip())
            raise Exception(f"{self.__class__.__name__}: install got returncode {proc.returncode} while installing {packages}: {packages}")

        return proc.stderr.strip() + "\n" + proc.stdout.strip()

    # def on_get_abspath(self, bin_name: BinName | HostBinPath, **context) -> HostBinPath | None:
    #     packages = self.on_get_packages(str(bin_name))
    #     if not self.INSTALLER_BIN_ABSPATH:
    #         raise Exception(f'{self.__class__.__name__} install method is not available on this host ({self.INSTALLER_BIN} not found in $PATH)')

    #     proc = self.exec(bin_name=self.INSTALLER_BIN_ABSPATH, cmd=['show', *packages])

    #     if proc.returncode != 0:
    #         print(proc.stdout.strip())
    #         print(proc.stderr.strip())
    #         raise Exception(f'{self.__class__.__name__}: got returncode {proc.returncode} while getting {bin_name} abspath')

    #     output_lines = proc.stdout.strip().split('\n')
    #     location = [line for line in output_lines if line.startswith('Location: ')][0].split(': ', 1)[-1]
    #     PATH = str(Path(location).parent.parent.parent / 'bin')
    #     abspath = shutil.which(str(bin_name), path=PATH)
    #     if abspath:
    #         return TypeAdapter(HostBinPath).validate_python(abspath)
    #     else:
    #         return None


if __name__ == "__main__":
    result = pip = PipProvider()

    if len(sys.argv) > 1:
        result = func = getattr(pip, sys.argv[1])  # e.g. install

    if len(sys.argv) > 2:
        result = func(sys.argv[2])  # e.g. install ffmpeg

    print(result)
