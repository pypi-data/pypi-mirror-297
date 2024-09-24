import os
from .browser import Browser
from selenium.webdriver import Ie as bwebdriver
from selenium.webdriver import IeOptions as Options
from selenium.webdriver.ie.service import Service
from webdriver_manager.microsoft import IEDriverManager as DriverManager

class IExplore(Browser):
    @property
    def win_path(self):
        return os.path.join("Internet Explorer", "iexplore.exe")

    @property
    def linux_commands(self):
        return ["iexplore"],

    @property
    def data_paths(self):
        return {
            "Windows": os.path.join(self.user_home, "AppData", "Local", "Microsoft", "Internet Explorer"),
        }

    @property
    def driver_manager(self):
        return DriverManager
    
    @property
    def service(self):
        return Service
    
    @property
    def _options(self):
        return Options

    @property
    def driver_class(self):
        return bwebdriver

    def list_profiles(self):
        profiles = []
        return profiles

    def set_options(self, options=None):
        if options:
            self.options = options

        else:
            self.options = self._options()