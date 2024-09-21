import pygame

from mlgame.view.audio_model import MusicInitSchema, SoundInitSchema


def sound_enabled(func):
    def wrapper(self, *args, **kwargs):
        if self._is_sound_on:
            return func(self, *args, **kwargs)

    return wrapper


class SoundController:
    def __init__(self, is_sound_on: bool, music_objs: list[MusicInitSchema], sound_objs: [SoundInitSchema]):
        self._is_sound_on = is_sound_on

        self._music_path_dict = {}
        self._sound_dict = {}
        try:
            pygame.mixer.init()
            # store music obj
            for music in music_objs:
                self._music_path_dict[music.music_id] = music.file_path
                # self.play_music(music.music_id)

            # store sound obj
            for sound in sound_objs:
                self._sound_dict[sound.sound_id] = pygame.mixer.Sound(sound.file_path)

        except Exception as e:
            self._is_sound_on = False

    @sound_enabled
    def play_music(self, music_id):
        music_path = self._music_path_dict.get(music_id, None)
        if music_path:
            pygame.mixer.music.load(self._music_path_dict[music_id])
            pygame.mixer.music.set_volume(60)
            pygame.mixer.music.play(-1)

        pass

    @sound_enabled
    def play_sound(self, sound_id):
        sound_obj = self._sound_dict.get(sound_id, None)
        if sound_obj:
            self._sound_dict[sound_id].play()
        pass
