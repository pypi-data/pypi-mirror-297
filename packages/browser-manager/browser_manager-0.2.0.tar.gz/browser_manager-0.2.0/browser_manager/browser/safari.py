import os
from .browser import Browser
from selenium.webdriver import Safari as bwebdriver
from selenium.webdriver import SafariOptions as Options
from selenium.webdriver.safari.service import Service

class Safari(Browser):
    @property
    def win_path(self):
        return os.path.join("Safari", "safari.exe")

    @property
    def linux_commands(self):
        return ["safari"]

    @property
    def data_paths(self):
        return {
            "Darwin": os.path.join(self.user_home, "Library", "Safari"),
        }

    @property
    def driver_manager(self):
        return None
    
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
        safari_profiles_path = os.path.join(self.user_data_path, "Profiles")

        if os.path.exists(safari_profiles_path) and os.path.isdir(safari_profiles_path):
            profile_dirs = [d for d in os.listdir(safari_profiles_path) if os.path.isdir(os.path.join(safari_profiles_path, d))]
            for profile_dir in profile_dirs:
                path = os.path.join(safari_profiles_path, profile_dir)
                profiles.append({"name": profile_dir, "path": path})

        return profiles

    def set_options(self, options=None):
        if options:
            self.options = options

        else:
            self.options = self._options()

    def get_driver_path(self):
        return None

    def get_driver(self, options=None):
        if self.is_installed():
            self.set_options(options)

            executable_path = self.get_drive_path()
            service = self.service(executable_path=executable_path)

            if self.options:
                if self.binary_location:
                    self.options.binary_location = self.binary_location

                self.driver = self.driver_class(options=self.options)

            else:
                self.driver = self.driver_class()
        

            return self.driver
        else:
            raise ValueError("Browser is not installed.")