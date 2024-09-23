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
    MUSIC_VOLUME,
    SOUND_VOLUME,
    MAIN_MUSIC_NAME
)
from tools.game_tools import (
    DynamicMusicMixer,
    SoundMixer,
    load_sounds
)

MUSIC_DICT = load_sounds([MAIN_MUSIC_NAME + ".mp3"], PATH_MUSICS, MUSIC_VOLUME)
SOUND_DICT = load_sounds(["click" + ".mp3"], PATH_SOUNDS, SOUND_VOLUME)

# Create the mixer
music_mixer = DynamicMusicMixer(MUSIC_DICT, MUSIC_VOLUME)
sound_mixer = SoundMixer(SOUND_DICT, SOUND_VOLUME)
