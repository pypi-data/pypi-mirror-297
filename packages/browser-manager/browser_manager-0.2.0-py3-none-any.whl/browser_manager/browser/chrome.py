import json
import os
from .browser import Browser
from selenium.webdriver import Chrome as bwebdriver
from selenium.webdriver import ChromeOptions as Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager as DriverManager

class Chrome(Browser):
    @property
    def win_path(self):
        return os.path.join("Google", "Chrome", "Application", "chrome.exe")

    @property
    def linux_commands(self):
        return ["google-chrome", "google-chrome-stable"]

    @property
    def data_paths(self):
        return {
            "Windows": os.path.join(self.user_home, "AppData", "Local", "Google", "Chrome", "User Data"),
            "Linux": os.path.join(self.user_home, ".config", "google-chrome"),
            "Darwin": os.path.join(self.user_home, "Library", "Application Support", "Google", "Chrome"),
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
        local_state_path = os.path.join(self.user_data_path, "Local State")

        if os.path.isfile(local_state_path):
            with open(local_state_path, "r", encoding="utf-8") as local_state_file:
                local_state = json.load(local_state_file)
                if "profile" in local_state:
                    info_cache = local_state["profile"].get("info_cache", {})
                    
                    for id, info in info_cache.items():
                        if "name" in info:
                            name = info["name"]
                            path = os.path.join(self.user_data_path, id)
                            profiles.append({"name": name, "path": path})
        
        profiles.sort(key=lambda x: x["name"])                      
        return profiles

    def set_options(self, options=None):
        if options:
            self.options = options

        else:
            self.options = self._options()
            
        if self.profile:
            user_data_dir, profile_directory = os.path.split(self.profile['path'])
            self.options.add_argument(f"user-data-dir={user_data_dir}")
            self.options.add_argument(f'--profile-directory={profile_directory}')