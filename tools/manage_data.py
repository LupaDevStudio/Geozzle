"""
Module for the settings of the applications.
"""


#################
### Constants ###
#################


from tools.basic_tools.image import (
    save_json_file
)
from tools.constants import (
    SETTINGS,
    PATH_SETTINGS
)


###############
### Classes ###
###############


class Achievements():
    def __init__(self) -> None:
        self.endings = SETTINGS["endings"]
        self.high_score = SETTINGS["high_score"]

    def update_high_score(self, score):
        if self.high_score < score:
            self.high_score = score
            SETTINGS["high_score"] = self.high_score
            save_json_file(PATH_SETTINGS, SETTINGS)


my_achievements = Achievements()
