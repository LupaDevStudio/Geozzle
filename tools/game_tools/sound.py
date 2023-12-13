"""
Module to manage musics and sound effects
"""

###############
### Imports ###
###############

### Python imports ###
from math import exp
from typing import Literal

### Kivy imports ###
from kivy.core.audio import SoundLoader, Sound

### Local imports ###
from tools.constants import FPS


###############
### Classes ###
###############


class MusicMixer():
    """
    Class to play music, only one sound can be played at the time.
    """

    def __init__(self, dict_music):
        self.musics = dict_music

    def change_volume(self, new_volume: float, name: str = None):
        """
        Change the volume of a single sound or all the sounds.

        Parameters
        ----------
        new_volume : float
            New volume to use.
        name : str, optional
            Name of the sound for which to change the volume, if None, applies to all the sounds,
            by default None
        """
        if name is not None:
            self.musics[name].volume = new_volume
        else:
            for key in self.musics:
                self.musics[key].volume = new_volume

    def play(self, name: str, loop: bool = False, timecode: float = 0, stop_other_sounds: bool = True):
        """
        Play the choosen sound.

        Parameters
        ----------
        name : str
            Name of the sound to play.
        loop : bool, optional
            Boolean to trigger the loop of the sound, by default False
        timecode : float, optional
            Start timecode of the sound, by default 0
        stop_other_sounds : bool, optional
            Boolean to stop all other sound currently playing before playing the new sound, by default True
        """
        if stop_other_sounds:
            self.stop()
        self.musics[name].play()
        if timecode != 0:
            # TODO: Does not work for now
            self.musics[name].seek(timecode)
        self.musics[name].loop = loop

    def stop(self):
        """
        Stop all sounds currently playing.
        """
        for key in self.musics:
            if self.musics[key].state == "play":
                self.musics[key].stop()


class DynamicMusicMixer(MusicMixer):
    """
    Class to play sound effects and musics that require dynamic management.
    """

    def __init__(self, dict_music, volume):
        super().__init__(dict_music)
        self.instructions = []
        dico_frame_state = {}
        for key in dict_music:
            dico_frame_state[key] = 0
        self.dico_frame_state = dico_frame_state
        self.volume = volume

    def add_sounds(self, sound_dict: dict):
        """
        Add all sounds contained in a dictionnary to the mixer.

        Parameters
        ----------
        sound_dict : dict
            Dictionnary containing the sounds to add.
        """
        for sound_name in sound_dict:
            self.dico_frame_state[sound_name] = 0
            self.musics[sound_name] = sound_dict[sound_name]
            self.musics[sound_name].volume = self.volume

    def add_sound(self, sound: Sound, sound_name: str):
        """
        Add a new sound to the mixer

        Parameters
        ----------
        sound : Sound
            Sound to add.
        sound_name : str
            Name of the sound to add.
        """
        self.dico_frame_state[sound_name] = 0
        self.musics[sound_name] = sound
        self.musics[sound_name].volume = self.volume

    def fade_out(self, name: str, duration: float, mode: Literal["linear", "exp"] = "linear"):
        """
        Apply a fade out effect to a sound

        Parameters
        ----------
        name : str
            Name of the sound to fade out.
        duration : float
            Fade out duration in seconds.
        mode : Literal["linear", "exp"], optional
            Fade out mode, by default "linear"
        """
        if mode == "exp":
            self.instructions.append(("exp_fade_out", name, duration))
        else:
            self.instructions.append(("fade_out", name, duration))

    def recursive_update(self):
        """
        Update to call at each time unit of the screen to update the sound effects.
        """
        pop_list = []
        # Iterate over the instructions to execute
        for instruction in self.instructions:
            new_volume = None
            # Execute the instruction
            if instruction[0] == "fade_out":
                key, duration = instruction[1], instruction[2]
                volume = self.musics[key].volume
                frame_to_fade = FPS * duration
                fade_diff = self.volume / frame_to_fade
                new_volume = volume - fade_diff
            elif instruction[0] == "exp_fade_out":
                key, duration = instruction[1], instruction[2]
                frame_to_fade = FPS * duration
                t = 60 * self.dico_frame_state[key] / frame_to_fade
                self.dico_frame_state[key] += 1
                new_volume = exp_fade_out(t) * self.volume
            # Apply the volume change
            if new_volume is not None:
                if new_volume > 0:
                    self.musics[key].volume = new_volume
                else:
                    self.musics[key].volume = 0
                    self.musics[key].stop()
                    self.musics[key].volume = self.volume
                    self.dico_frame_state[key] = 0
                    pop_list.append(instruction)
        # Remove executed instruction
        for el in pop_list:
            self.instructions.remove(el)


class SoundMixer():
    """
    Manager for the sound effects of the game.

    It is able to play several times the same sound simultaneously.
    """

    def __init__(self, dict_sound, volume, channel_number=10):
        self.sounds = {}
        self.channel_number = channel_number
        for key in dict_sound:
            self.sounds[key] = [SoundLoader.load(dict_sound[key])
                                for i in range(channel_number)]
            for i in range(channel_number):
                self.sounds[key][i].volume = volume

    def play(self, name: str, volume: float = None):
        """
        Play the selected sound.

        Parameters
        ----------
        name : str
            Name of the sound to play.
        volume : float, optional
            Volume to use to play the sound, default volume if None,
            by default None
        """
        i = 0
        while i < self.channel_number and self.sounds[name][i].state == "play":
            i += 1
        if i < self.channel_number:
            if volume is not None:
                self.sounds[name][i].volume = volume
            self.sounds[name][i].play()
        else:
            print("Unable to play the desired sound due to channel saturation")

    def change_volume(self, new_volume: float, name: str = None):
        """
        Change the volume of a single sound or all the sounds.

        Parameters
        ----------
        new_volume : float
            New volume to use.
        name : str, optional
            Name of the sound for which to change the volume, if None, applies to all the sounds,
            by default None
        """
        if name is not None:
            for i in range(self.channel_number):
                self.sounds[name][i].volume = new_volume
        else:
            for key in self.musics:
                for i in range(self.channel_number):
                    self.sounds[key][i].volume = new_volume

#################
### Functions ###
#################


def exp_fade_out(t):
    """
    Amplitude function of time for an exponential fade out.
    """
    return 1 - exp((t - 60) * 0.15)


def load_sounds(music_list: str, foldername: str, volume: float) -> dict:
    """
    Load all sounds of a folder at once.

    Parameters
    ----------
    foldername : str
        Name of the folder where the sounds are stored.

    volume : float
        Volume to use to play the sounds by default.

    Returns
    -------
    dict
        Dictionnary with the loaded sounds.
    """
    sound_dict = {}
    for file in music_list:
        name_file = file.split(".")[0]
        sound_dict[name_file] = SoundLoader.load(foldername + file)
        sound_dict[name_file].volume = volume
    return sound_dict
