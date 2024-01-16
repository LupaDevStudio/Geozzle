"""
Tools package of the application.

Modules
-------

"""

from tools.path import (
    PATH_MUSICS,
    PATH_MAIN_MUSIC
)

from tools.constants import (
    USER_DATA,
    MUSIC_VOLUME,
    SOUND_VOLUME,
    MAIN_MUSIC_NAME
)

from tools.game_tools import (
    MusicMixer,
    DynamicMusicMixer,
    SoundMixer,
    load_sounds
)

MUSIC_DICT = load_sounds([MAIN_MUSIC_NAME + ".mp3"], PATH_MUSICS, MUSIC_VOLUME)

# Create the mixer
music_mixer = DynamicMusicMixer(MUSIC_DICT, MUSIC_VOLUME)
sound_mixer = DynamicMusicMixer({}, SOUND_VOLUME)