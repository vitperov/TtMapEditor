import json
import os

class ApplicationSettingsModel:
    def __init__(self, settings_file="settings/application.json"):
        self.settings_file = settings_file
        self.settings = {}

        # Load settings from file if it exists
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as f:
                try:
                    self.settings = json.load(f)
                except json.JSONDecodeError:
                    print(f"Error: Could not decode JSON from {self.settings_file}")
                    self.settings = {}
        else:
            print(f"Settings file {self.settings_file} not found. Using default settings.")

    # Getter and Setter for additionalMapObjectsDir
    def getAdditionalMapObjectsDir(self):
        return self.settings.get("additionalMapObjectsDir", "")

    def setAdditionalMapObjectsDir(self, value):
        self.settings["additionalMapObjectsDir"] = value
        self._saveSettings()

    # Getter and Setter for additionalGeneratorsDir
    def getAdditionalGeneratorsDir(self):
        return self.settings.get("additionalGeneratorsDir", "")

    def setAdditionalGeneratorsDir(self, value):
        self.settings["additionalGeneratorsDir"] = value
        self._saveSettings()

    def _saveSettings(self):
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        # Write updated settings to file
        with open(self.settings_file, "w") as f:
            json.dump(self.settings, f, indent=4)


