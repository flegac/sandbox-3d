from panda3d.core import *
from direct.gui.DirectGui import *
from direct.showbase.ShowBase import ShowBase

class Demo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.frame = DirectScrolledFrame(
            canvasSize = (-1, 1, -2, 1),
            frameSize = (-1, 1, -1, 1),
            horizontalScroll_frameSize=(0, 0, 0, 0),
            parent=aspect2d,
        )
        DirectLabel(
            text = "I scroll",
            scale = 0.1,
            pos = (0, 0, 0),
            parent = self.frame.getCanvas(),
        )

        DirectLabel(
            text = "I don't",
            scale = 0.1,
            pos = (0, 0, -0.4),
            parent = self.frame,
        )

        self.accept('wheel_up', self.scroll_menu, [False])
        self.accept('wheel_down', self.scroll_menu, [True])


    def scroll_menu(self, down):
        scroll_bar = self.frame.verticalScroll
        modifier = -1 if down else 1
        scroll_bar.setValue(scroll_bar.getValue() - modifier*scroll_bar['pageSize'])


demo = Demo()
demo.run()