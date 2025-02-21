import pygame
import os

class SoundManager:
    def __init__(self, sound_folder="assets/sounds"):
        self.sound_folder = sound_folder
        self.sounds = {}  
        pygame.mixer.init()  

    def get_sound(self, sound_name):
        if sound_name in self.sounds:
            return self.sounds[sound_name]  

        sound_path = os.path.join(self.sound_folder, f"{sound_name}.wav") 
        if not os.path.exists(sound_path): 
            sound_path = os.path.join(self.sound_folder, f"{sound_name}.mp3")
            if not os.path.exists(sound_path):
                print(f"Fejl: Lydfil '{sound_name}' ikke fundet i '{self.sound_folder}'")
                return None

        sound = pygame.mixer.Sound(sound_path)  
        self.sounds[sound_name] = sound
        return sound

    def play_sound(self, sound_name):
        sound = self.get_sound(sound_name)
        if sound:
            sound.play()
