import os
from . import Chrome
from webdriver_manager.opera import OperaDriverManager as DriverManager

class Opera(Chrome):
    @property
    def win_path(self):
        return os.path.join("Opera", "launcher.exe")

    @property
    def linux_commands(self):
        return ["opera"]

    @property
    def data_paths(self):
        return {
            "Windows": os.path.join(self.user_home, "AppData", "Roaming", "Opera Software", "Opera Stable"),
            "Linux": os.path.join(self.user_home, ".config", "opera"),
            "Darwin": os.path.join(self.user_home, "Library", "Application Support", "com.operasoftware.Opera"),
        },

    @property
    def driver_manager(self):
        return DriverManager

    def list_profiles(self):
        profiles = []
        opera_profile_path = os.path.join(self.user_data_path, "Opera Software", "Opera Stable")

        if os.path.exists(opera_profile_path) and os.path.isdir(opera_profile_path):
            profile_dirs = [d for d in os.listdir(opera_profile_path) if os.path.isdir(os.path.join(opera_profile_path, d))]
            for profile_dir in profile_dirs:
                path = os.path.join(opera_profile_path, profile_dir)
                profiles.append({"name": profile_dir, "path": path})

        return profiles