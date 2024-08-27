import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
from typing import Callable

from direct.filter.CommonFilters import CommonFilters
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from direct.task import Task
from loguru import logger
from panda3d.core import loadPrcFile, NodePath, PandaNode, LightRampAttrib, PandaSystem, ClockObject

from easy_kit.timing import show_timing
from sandbox_core.assets.audio import Audio

loadPrcFile(Path.cwd().parent / "resources/Config.prc")


@dataclass
class Status:
    title: str

    panda3d: str = f'{PandaSystem.getVersionString()} '
    platform: str = f'{PandaSystem.get_platform()}'
    shader: bool = False


class KeyboardAutorepeat:

    @staticmethod
    def disable():
        if sys.platform != 'win32':
            subprocess.run('xset r off', shell=True)

    @staticmethod
    def enable():
        if sys.platform != 'win32':
            subprocess.run('xset r on', shell=True)


class GraphicConfig:

    def setup(self, node: NodePath, ):
        # simplepbr.init(
        #     render_node=node,
        #     # use_emission_maps=False,
        #     # enable_shadows=True
        # )
        node.setShaderAuto()


class MyBase(ShowBase):
    def __init__(self):
        super().__init__()
        KeyboardAutorepeat.disable()
        self.audio = Audio(self)
        self.updaters: list[Callable[[...], ...]] = []
        pprint(self.get_status())

        fps = 60
        logger.warning(f'setting max FPS: {fps}')
        globalClock.setMode(ClockObject.MLimited)
        globalClock.setFrameRate(fps)

    def add_updater(self, updater: Callable[[], ...]):
        def _updater(task: Task):
            updater()
            return task.cont

        self.task_mgr.add(_updater)

    def status(self):
        return Status(
            title=self.win.properties.title,

            shader=self.win.getGsg().getSupportsBasicShaders()
        )

    def get_status(self):
        return {
            'SupportsBasicShaders': self.win.getGsg().getSupportsBasicShaders(),
            'SupportsDepthTexture': self.win.getGsg().getSupportsDepthTexture(),
            'SupportsShadowFilter': self.win.getGsg().getSupportsShadowFilter(),
        }

    def cartoon(self):
        tempnode = NodePath(PandaNode("temp node"))
        tempnode.setAttrib(LightRampAttrib.makeSingleThreshold(0.5, 0.4))
        tempnode.setShaderAuto()
        self.cam.node().setInitialState(tempnode.getState())

        self.separation = 1  # Pixels
        self.filters = CommonFilters(self.win, self.cam)
        self.filters.setCartoonInk(separation=self.separation)

    def userExit(self):
        KeyboardAutorepeat.enable()
        show_timing()
        super().userExit()


base = MyBase()
