import os.path
import constants
import json

class Config:

    currentPageNumber = 0
    currentItemNumber = 0
    isRestartNeeded = False
    config_filename = ""

    def __init__(self):
        self.config_filename = f"./{constants.config_file_name}"
        if os.path.exists(self.config_filename):
            print("File exists")
            self.load()
        else:
            print("Config File Not exists")
            self.save()

    # def save(self):
    #     data = {
    #         constants.config_current_page_number: self.currentPageNumber,
    #         constants.config_current_item_number: self.currentItemNumber,
    #         constants.config_restart_needed: self.isRestartNeeded
    #     }
    #     with open(constants.config_file_name, 'w') as out_file:
    #         json.dump(data, out_file, sort_keys=True, indent=4, ensure_ascii=False)

    def save(self, currentPageNumber, currentItemNumber):
        self.currentPageNumber = currentPageNumber
        self.currentItemNumber = currentItemNumber
        data = {
            constants.config_current_page_number: self.currentPageNumber,
            constants.config_current_item_number: self.currentItemNumber,
            constants.config_restart_needed: self.isRestartNeeded
        }
        with open(constants.config_file_name, 'w') as out_file:
            json.dump(data, out_file, sort_keys=True, indent=4, ensure_ascii=False)

    def load(self):
        with open(constants.config_file_name) as config_file:
            config_json = json.load(config_file)
            self.isRestartNeeded = config_json[constants.config_restart_needed]
            self.currentItemNumber = config_json[constants.config_current_item_number]
            self.currentPageNumber = config_json[constants.config_current_page_number]
            if self.isRestartNeeded:
                self.currentPageNumber = 0
                self.currentItemNumber = 0
                self.isRestartNeeded = False