import sys
from pathlib import Path

import simplepbr
from direct.showbase.ShowBase import ShowBase
from panda3d.core import load_prc_file

load_prc_file(Path.cwd().parent / 'resources/Config.prc')


class TestBase(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        simplepbr.init()
        # Let's load the building model and save it as self.building.
        self.model = self.loader.loadModel("viking.glb")

        # Let's position the building further away from the camera.
        # To this end we must set the Y argument to a positive number.
        self.cam.setPos(0, -10, 0)

        # Finally, let's parent the building model to render so that we
        # can see it.
        self.model.reparentTo(self.render)

        self.accept('escape', sys.exit)


if __name__ == '__main__':
    app = TestBase()
    app.run()
