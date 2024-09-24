import os
from .browser import Browser
from selenium.webdriver import Firefox as bwebdriver
from selenium.webdriver import FirefoxOptions as Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager as DriverManager

class Firefox(Browser):
    @property
    def win_path(self):
        return os.path.join("Mozilla Firefox", "firefox.exe")

    @property
    def linux_commands(self):
        return ["firefox", "firefox-nightly"]

    @property
    def data_paths(self):
        return {
            "Windows": os.path.join(self.user_home, "AppData", "Roaming", "Mozilla", "Firefox", "Profiles"),
            "Linux": os.path.join(self.user_home, ".mozilla", "firefox"),
            "Darwin": os.path.join(self.user_home, "Library", "Application Support", "Firefox"),
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
        profile_dirs = [d for d in os.listdir(self.user_data_path) if os.path.isdir(os.path.join(self.user_data_path, d))]
        for profile_dir in profile_dirs:
            if os.path.isfile(os.path.join(self.user_data_path, profile_dir, "prefs.js")):
                # Use o nome completo do perfil para seleção
                path = os.path.join(self.user_data_path, profile_dir)
                # Use apenas o nome da pasta para montar a URL
                name = profile_dir.split(".")[1]
                profiles.append({"name": name, "path": path})
                
        return profiles  

# Usage Example
if __name__ == '__main__':

    basic_example = True

    if basic_example:
        driver = Firefox().get_driver()
        driver.get("https://google.com")
        print(driver.title)

        # Wait for user input before closing the browser session
        input("Press Enter to close the browser...")

        # Close the browser session
        driver.quit()
        exit()
    
    # Create an instance of the Firefox browser
    browser = Firefox()

    # Select the preferred profile for the chosen browser by passing the profile name "default-release"
    # If it's not available, a selection will be presented.
    # Selecting a profile is optional
    profile = browser.select_profile("default-release")
    print(f"Selected profile: {profile['name']}")  # Print the name of the selected profile
    print(f"Selected profile folder: {profile['path']}")  # Print the path of the selected profile

    # Get the driver for the selected browser
    driver = browser.get_driver()
    print(f"Driver Path: {browser.driver_path}")  # Print the path of the driver
    print(f"Driver: {driver}")  # Print the driver object

    # Navigate to Google
    driver.get("https://google.com")
    print(driver.title)

    # Wait for user input before closing the browser session
    input("Press Enter to close the browser...")

    # Close the browser session
    driver.quit()