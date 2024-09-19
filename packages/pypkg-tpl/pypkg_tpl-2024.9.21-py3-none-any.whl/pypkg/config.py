import getpass
import pathlib


class Config:
    PYPKG_HOME = pathlib.Path(__file__).parent
    TPL_PATH = PYPKG_HOME / 'tpl_pkg'
    USERNAME = getpass.getuser()

config = Config()