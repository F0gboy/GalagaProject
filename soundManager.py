import pygame
import os

class SoundManager:
    def __init__(self, sound_folder="assets/sounds"):
        self.sound_folder = sound_folder
        self.sounds = {}
        self.volume = 0.5
        self.currently_playing = []
        pygame.mixer.init()

    def get_sound(self, sound_name):
        if sound_name in self.sounds:
            return self.sounds[sound_name]

        sound_path = os.path.join(self.sound_folder, f"{sound_name}.wav")
        if not os.path.exists(sound_path):
            sound_path = os.path.join(self.sound_folder, f"{sound_name}.mp3")
            if not os.path.exists(sound_path):
                print(f"Error: Sound file '{sound_name}' not found in '{self.sound_folder}'")
                return None

        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(self.volume)
        self.sounds[sound_name] = sound
        return sound

    def play_sound(self, sound_name):
        sound = self.get_sound(sound_name)
        if sound:
            sound.set_volume(self.volume)
            sound.play()
            self.currently_playing.append(sound)

    def stop_sound(self):
        pygame.mixer.stop()
        self.currently_playing.clear()

    def increase_volume(self):
        self.volume = min(1.0, self.volume + 0.03)
        self.update_currently_playing_volume()

    def decrease_volume(self):
        self.volume = max(0.0, self.volume - 0.03)
        self.update_currently_playing_volume()

    def update_currently_playing_volume(self):
        for sound in self.currently_playing:
            sound.set_volume(self.volume)
