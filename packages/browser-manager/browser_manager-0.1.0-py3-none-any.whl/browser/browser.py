from abc import ABC, abstractmethod
import subprocess
import platform
import os
from selenium import webdriver

class Browser(ABC):
    def __init__(self):
        self.profile = None
        self.options = None
        self.driver_path = None
        self.binary_location = None

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def user_home(self):
        return os.path.expanduser("~")
    
    @property
    def system(self):
        return platform.system()
    
    @property
    def user_data_path(self):        
        if self.system in self.data_paths:
            return self.data_paths[self.system]
            

        raise ValueError("Unsupported browser or operating system: {} on {}".format(self.__class__.__name__, self.system))
    
    @property
    @abstractmethod
    def win_path(self):
        pass

    @property
    @abstractmethod
    def linux_commands(self):
        pass

    @property
    @abstractmethod
    def data_paths(self):
        pass

    @property
    @abstractmethod
    def driver_manager(self):
        pass

    @property
    @abstractmethod
    def service(self):
        pass

    @property
    @abstractmethod
    def _options(self):
        pass

    @property
    @abstractmethod
    def driver_class(self):
        pass

    @abstractmethod 
    def list_profiles(self):
        pass

    def is_installed(self):
        if platform.system() == "Windows":
            return self._is_installed_windows()
            
        if platform.system() == "Linux" or platform.system() == "Darwin":
            return self._is_installed_linux()
    
    def _is_installed_windows(self):
        # Verifica o diretório do Program Files (x86)
        program_files_dirs = [os.environ.get("ProgramFiles(x86)"), os.environ.get("ProgramFiles")]

        for program_files_dir in program_files_dirs:
            if program_files_dir:
                path = os.path.join(program_files_dir, self.win_path)
                if os.path.isfile(path):
                    return True
        return False

    def _is_installed_linux(self):
        if any(self._is_linux_command_available(command) for command in self.linux_commands):
                return True
        
        return False
    
    def _is_linux_command_available(self, command):
        try:
            command_path = subprocess.check_output(["which", command], stderr=subprocess.DEVNULL).decode().strip()
            self.binary_location = command_path
            return True
        except subprocess.CalledProcessError:
            return False

    def get_driver_path(self):

        if not self.driver_path:
            os.environ["WDM_LOG_LEVEL"] = "0"
            print("Downloading Browser Driver...")
            self.driver_path = self.driver_manager().install()
            print("Browser Driver downloaded Successfully!")

        return self.driver_path

    def set_options(self, options=None):
        if options:
            self.options = options
        else:
            self.options = self._options()
            
        if self.profile:
            self.options.profile = self.profile["path"]

    def get_driver(self, options=None):
        if self.is_installed():
            self.set_options(options)

            executable_path = self.get_driver_path()
            service = self.service(executable_path=executable_path)

            if self.options:
                if self.binary_location:
                    self.options.binary_location = self.binary_location

                self.driver = self.driver_class(
                    service=service,
                    options=self.options
                )

            else:
                self.driver = self.driver_class(
                    service=service
                )
        

            return self.driver
        else:
            raise ValueError("Browser is not installed.")

    def select_profile(self, profile = None):
        profiles = self.list_profiles()
        print()

        if not profiles:
            print("No profiles found in the specified directory.")
            return None
        
        if profile:
            matched_profile = next((item for item in profiles if item["name"] == profile or item["path"] == profile), None)
            if matched_profile:
                self.profile = matched_profile
                return self.profile
            
            print("Selected profile is not find.")

        if len(profiles) == 1:
            self.profile = profiles[0]
            print(f"Only one profile detected: {self.profile['name']}. It has been automatically selected.")
            return self.profile
        
        while True:
            print("Available profiles:")
            for i, profile in enumerate(profiles, start=1):
                print(f"{i}. {profile['name']}")

            selected = input("Choose the profile number you want to use: ")
            print()

            try:
                selected = int(selected)
                if 1 <= selected <= len(profiles):
                    self.profile = profiles[selected - 1]
                    return self.profile
                else:
                    print("Invalid profile number. Please choose a valid number.")
            except ValueError:
                print("Invalid Input. Please enter a valid number.")