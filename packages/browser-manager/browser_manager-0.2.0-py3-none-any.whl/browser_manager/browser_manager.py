import os
import platform
import subprocess
from browser_manager.browser import Chrome, Chromium, Firefox, IExplore, MSEdge, Opera, Safari

class BrowserManager:
    def __init__(self):
        self.installeds = None
        self.browser = None

    def get_installeds(self):
        if platform.system() == "Windows":
            return self._get_installeds_windows()
            
        if platform.system() == "Linux" or platform.system() == "Darwin":
            return self._get_installeds_linux()
    
    def _get_installeds_windows(self):
        installeds = []

        browser_mapping = {
            Chrome: [os.path.join("Google", "Chrome", "Application", "chrome.exe")],
            Chromium: [os.path.join("Chromium", "Application", "chrome.exe")],
            Firefox: [os.path.join("Mozilla Firefox", "firefox.exe")],
            IExplore: [os.path.join(program_files_dir, "Internet Explorer", "iexplore.exe")],
            MSEdge: [os.path.join("Microsoft", "Edge", "Application", "msedge.exe")],
            Opera: [os.path.join(program_files_dir, "Opera", "launcher.exe")],
            Safari: [os.path.join("Safari", "safari.exe")],
        }

        # Verifica o diretório do Program Files (x86)
        program_files_dirs = [os.environ.get("ProgramFiles(x86)"), os.environ.get("ProgramFiles")]

        for browser, browser_path in browser_mapping.items():
            for program_files_dir in program_files_dirs:
                if program_files_dir:
                    path = os.path.join(program_files_dir, browser_path)

                    if os.path.isfile(path):
                        installeds.append(browser)
        self.installeds = installeds
        return self.installeds
                    
    def _get_installeds_linux(self):
        installeds = []

        browser_mapping = {
            Chrome: ["google-chrome", "google-chrome-stable"],
            Chromium: ["chromium", "chromium-browser", "chromium-browser-laptop"],
            Firefox: ["firefox", "firefox-nightly"],
            IExplore: ["iexplore"],
            MSEdge: ["msedge", "MicrosoftEdge"],
            Opera: ["opera"],
            Safari: ["safari"],
        }


        for browser, commands in browser_mapping.items():
            if any(self._is_command_available(command) for command in commands):
                installeds.append(browser)

        self.installeds = installeds
        return self.installeds
    
    def _is_command_available(self, command):
        try:
            subprocess.check_output(["which", command], stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            return False
        
    def select_browser(self, browser = None):
        installeds = self.get_installeds()
        print()

        if not installeds:
            print("No installed browser found.")
            return None
        
        if browser:
            if browser in installeds:
                self.browser = browser
                return self.browser()
            
            print("Selected browser is not installed.")

        if len(installeds) == 1:
            self.browser = installeds[0]
            print(f"Only one browser detected: {self.browser().name}. It has been automatically selected.")
            return self.browser()

        while True:
            print("Installed browsers:")
            for i, name in enumerate(installeds, start=1):
                print(f"{i}. {name}")

            selected = input("Choose browser number:")
            print()

            try:
                selected = int(selected)
                if 1 <= selected <= len(installeds):
                    self.browser = installeds[selected - 1]
                    return self.browser()
                else:
                    print("Invalid browser number.")
            except ValueError:
                print("Invalid Input. Please enter a valid number.")


# Usage Example
if __name__ == '__main__':
    # Create an instance of the BrowserManager class
    browser_manager = BrowserManager()

    # Select the preferred browser by passing the desired browser class (Firefox)
    # If is not available, a selection will be presented.
    browser = browser_manager.select_browser(Firefox)
    print(f"Selected browser: {browser.name}")  # Print the name of the selected browser

    # Select the preferred profile for the chosen browser by passing the profile name "default-release"
    # If is not available, a selection will be presented.
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
