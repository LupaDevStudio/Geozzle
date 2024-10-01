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
from tools.game_tools import (
    DynamicMusicMixer,
    SoundMixer,
    load_sounds
)

MUSIC_DICT = load_sounds([MAIN_MUSIC_NAME + ".mp3"], PATH_MUSICS, 0.5)
SOUND_DICT = load_sounds(["click" + ".mp3"], PATH_SOUNDS, 0.5)

# Create the mixer
music_mixer = DynamicMusicMixer(MUSIC_DICT, 0.5)
sound_mixer = SoundMixer(SOUND_DICT, 0.5)
