"""
Tools package of the application.

Modules
-------

"""

from tools.path import (
    PATH_MUSICS,
    PATH_SOUNDS
)
from tools.constants import (
    MAIN_MUSIC_NAME
)
from tools.geozzle import (
    USER_DATA
)
from tools.game_tools import (
    DynamicMusicMixer,
    SoundMixer,
    load_sounds
)

MUSIC_DICT = load_sounds([MAIN_MUSIC_NAME + ".mp3"], PATH_MUSICS, USER_DATA.music_volume)
SOUND_DICT = load_sounds(["click" + ".mp3"], PATH_SOUNDS, USER_DATA.sound_volume)

# Create the mixer
music_mixer = DynamicMusicMixer(MUSIC_DICT, USER_DATA.music_volume)
sound_mixer = SoundMixer(SOUND_DICT, USER_DATA.sound_volume)
