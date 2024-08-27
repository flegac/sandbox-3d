from easy_kit.timing import time_func
from sandbox.my_base import base
from procedural_gen.region.region import Region


class Screen:
    @staticmethod
    def region():
        return Region.from_size(*base.win.get_size())

    @staticmethod
    @time_func
    def region(region: Region):
        screen = Screen.region()
        if region.x.start < 0:
            size = region.x.size
            region.x.end = screen.x.size + region.x.start
            region.x.start = region.x.end - size

        if region.y.start < 0:
            size = region.y.size
            region.y.end = screen.y.size + region.y.start
            region.y.start = region.y.end - size
        return region


