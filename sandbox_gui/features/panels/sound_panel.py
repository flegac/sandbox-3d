from pathlib import Path

from sandbox.my_base import base
from sandbox_core.assets.library import Library, Query
from sandbox_gui.base.config.frame_size import FrameSize
from sandbox_gui.base.config.ui_config import UiConfig
from sandbox_gui.base.layout.layout_factory import L
from sandbox_gui.base.panel_list import PanelList
from sandbox_gui.base.widget.slider import Slider

MUSIC_ROOT = Path.home() / 'Documents/Music'


def sound_panel(size: FrameSize):
    musics = Library(MUSIC_ROOT.resolve() / 'Cool')

    search_list = PanelList(
        size=FrameSize(width=size.width, height=450),
        on_select=base.audio.play_music,
        namer=lambda x: f'{x.stem}'
    )
    search_list.update(musics.search(Query(pattern='*Main*.wav')))

    return L.vertical(
        ui=UiConfig(name='sound', size=size),
        children=[
            Slider(name='music', value=.1, updater=lambda vol: base.audio.set_music_volume(vol)),
            Slider(name='sfx', value=.1, updater=lambda vol: base.audio.set_sfx_volume(vol)),
            search_list.panel
        ]
    )
