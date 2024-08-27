from sandbox.my_base import base
from procedural_gen.region.vec import Vec


class Viewport:
    # https://discourse.panda3d.org/t/multi-viewport-in-panda3d/3138/7

    def __init__(self, model1):
        self.camera1 = self.createCamera(Vec.at(-5,-5,5),(0, .5, 0, 1))
        self.camera1.reparentTo(model1)
        self.camera1.lookAt(model1)
        self.camera2 = self.createCamera(Vec.at(5,-5,5), (.5, 1, 0, 1))
        self.camera2.reparentTo(model1)
        self.camera2.lookAt(model1)
        base.camNode.setActive(False)  # disable default cam

    def createCamera(self, pos: Vec, dispRegion):
        camera = base.makeCamera(base.win, displayRegion=dispRegion)
        camera.node().getLens().setAspectRatio(3.0 / 4.0)
        camera.node().getLens().setFov(45)  # optional.
        camera.setPos(*pos.vec)
        return camera
