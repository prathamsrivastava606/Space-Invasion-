import pygame


class Audio:

    def __init__(self):

        pygame.mixer.init()

        self.music_path = "assets/music/background_music.mp3"

        pygame.mixer.music.load(
            self.music_path
        )

        pygame.mixer.music.set_volume(
            0.35
        )

    def play_music(self):

        pygame.mixer.music.play(-1)

    def stop_music(self):

        pygame.mixer.music.stop()