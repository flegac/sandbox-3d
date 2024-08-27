from direct.gui.DirectButton import DirectButton
from direct.gui.DirectCheckButton import DirectCheckButton
from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectOptionMenu import DirectOptionMenu
from direct.gui.DirectRadioButton import DirectRadioButton
from direct.gui.DirectSlider import DirectSlider
from direct.gui.DirectWaitBar import DirectWaitBar

from sandbox.my_base import base


def init_demo(scale: float = .05):
    DirectButton(text='ok', scale=scale, pos=(0, 0, .8))
    DirectCheckButton(text="CheckButton", scale=scale, pos=(0, 0, .6))

    def action(message: str):
        def action(arg: str = message):
            print(arg)
            entry.enterText(arg)

        return action

    entry = DirectEntry(
        # text="coucou",
        scale=scale,
        pos=(0, 0, .4),
        # width=5,
        initialText="Type Something",
        numLines=3,
        cursorKeys=True,
        obscured=False,
        focus=False,
        command=action('command'),
        focusInCommand=action('focusInCommand'),
        focusOutCommand=action('focusOutCommand')
    )
    DirectOptionMenu(
        text="options",
        scale=scale,
        pos=(0, 0, .2),

        command=action('option_menu'),
        items=[f"item{i}" for i in range(100)],
        initialitem=2,
        highlightColor=(0.65, 0.65, 0.65, 1),
    )

    v = [0]
    buttons = [
        DirectRadioButton(text='RadioButton0', variable=v, value=[0], scale=scale, pos=(-0.4, 0, 0)),
        DirectRadioButton(text='RadioButton1', variable=v, value=[1], scale=scale, pos=(0, 0, 0)),
        DirectRadioButton(text='RadioButton2', variable=v, value=[2], scale=scale, pos=(0.4, 0, 0))
    ]
    for button in buttons:
        button.setOthers(buttons)

    bar = DirectWaitBar(
        text="",
        pos=(0, 0, -.2)
    )
    def set_val():
        bar['value'] = slider['value']
    slider = DirectSlider(
        range=(0, 100),
        value=50,
        pageSize=100,
        pos=(0, 0, -.2),
        command=set_val,
        thumb_frameSize=(0,0,0,0)
    )


if __name__ == '__main__':
    init_demo()
    base.run()
