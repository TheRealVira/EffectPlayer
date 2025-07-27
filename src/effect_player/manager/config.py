"""Config Manager just managing se configs."""

from configparser import ConfigParser

CONFIG = ConfigParser()
CONFIG.read("config.ini")
