"""
Package to manage the screens of the application
"""

###############
### Imports ###
###############

from screens.custom_widgets import (
    CustomButton,
    CustomSpinner,
    CircleIconButton,
    RoundedButtonImage,
    ColoredRoundedButton,
    ThreeLives,
    CircleProgressBar
)

from screens.home import HomeScreen
from screens.game_over import GameOverScreen
from screens.game_question import GameQuestionScreen
from screens.game_summary import GameSummaryScreen
from screens.settings import SettingsScreen
from screens.gallery import GalleryScreen
from screens.stats import StatsScreen
from screens.stats_continent import StatsContinentScreen
from screens.world_ranking import WorldRankingScreen
