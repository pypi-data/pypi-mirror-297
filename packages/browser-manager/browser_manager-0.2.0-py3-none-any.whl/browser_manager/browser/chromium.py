import os
from . import Chrome
from webdriver_manager.chrome import ChromeType

class Chromium(Chrome):
    @property
    def win_path(self):
        return os.path.join("Chromium", "Application", "chrome.exe")

    @property
    def linux_commands(self):
        return ["chromium", "chromium-browser", "chromium-browser-laptop"]

    @property
    def data_paths(self):
        return {
                "Windows": None,  # Chromium não é suportado no Windows por padrão
                "Linux": os.path.join(self.user_home, ".config", "chromium"),
                "Darwin": None,  # Chromium não é suportado no macOS por padrão
            },

    def get_driver_path(self):

        if not self.driver_path:
            os.environ["WDM_LOG_LEVEL"] = "0"
            print("Downloading Browser Driver...")
            self.driver_path = self.driver_manager(chrome_type=ChromeType.CHROMIUM).install()
            print("Browser Driver downloaded Successfully!")

        return self.driver_path