from functools import lru_cache

from direct.showbase import Audio3DManager
from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, NodePath


class Audio:
    def __init__(self, show_base: ShowBase):
        show_base.cTrav = CollisionTraverser()

        self.music = show_base.musicManager
        self.sfx = show_base.sfxManagerList[0]

        self.music3d = Audio3DManager.Audio3DManager(self.music, show_base.cam)
        self.music3d.setListenerVelocityAuto()

        self.audio3d = Audio3DManager.Audio3DManager(self.sfx, show_base.cam)
        self.audio3d.setListenerVelocityAuto()
        # self.audio3d.setConcurrentSoundLimit(20)
        # self.audio3d.setCacheLimit(20)
        # self.audio3d.setDistanceFactor(1.)
        # self.audio3d.setDropOffFactor(.2)

        self.cache = {}

    def set_sfx_volume(self, value: float):
        self.sfx.setVolume(value)

    def set_music_volume(self, value: float):
        self.music.setVolume(value)

    def play_music(self, name: str):
        from sandbox.my_base import base

        self.music.stopAllSounds()

        sound = self.load_music(name)
        base.playMusic(sound, looping=True)

    def play_sfx(self, sound: str, target: NodePath, volume: float = None):
        sound = self.load_sfx(sound)
        if volume is not None:
            sound.set_volume(volume)
        # sound.setPlayRate(1.)
        # sound.setLoop(False)
        sound.play()

        # self.audio3d.setSoundVelocityAuto(sound)
        self.audio3d.attachSoundToObject(sound, target)

    @lru_cache
    def load_sfx(self, name: str):
        return self.audio3d.load_sfx(name)

    @lru_cache
    def load_music(self, name: str):
        return self.music3d.load_sfx(name)
