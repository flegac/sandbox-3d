from pathlib import Path

from loguru import logger

from python_ecs.ecs import sim
from sandbox_core._utils.ray.physic_ray import PhysicRay
from sandbox_core.assets.library import Query
from sandbox_core.display.display import Display
from sandbox_core.events.event_config import EventConfig
from sandbox_core.physics.phys_system import PhysSystem
from sandbox_core.transform import ETransform
from sandbox_gui.base.config.frame_size import FrameSize
from sandbox_gui.base.config.ui_config import UiConfig
from sandbox_gui.base.layout.layout_factory import L
from sandbox_gui.base.panel_list import PanelList
from sandbox_gui.base.widget.button import MyButton
from sandbox_gui.base.widget.entry import MyEntry
from sandbox_gui.base.widget.text import Text
from sandbox_gui.features.editor.item_placer import ItemPlacer
from sandbox_gui.features.editor.model_library import ModelLibrary
from sandbox_gui.features.panels.rigidbody_panel import RigidBodyPanel
from sandbox_gui.features.with_mouse_select import WithMouseSelect
from sandbox_lib.rooms.floor import Floor


class Builder:
    def __init__(self):
        self.placer = ItemPlacer(ModelLibrary(
            query=Query(
                pattern='*.fbx',
                name_include=' '.join([
                    'Env_Rock_',
                    # 'Grass_Patch',
                    # 'Grass_Large',
                    # 'Tree_Pine',
                    # 'CampFire',
                    # 'Wood_Pile',
                ]),
                name_exclude=' '.join([
                    'Snow',
                    'Round Grey Brown Large Alt'
                ])
            )
        ))
        self.to_build: Path | None = None
        self.ray = PhysicRay()
        self.selector = WithMouseSelect()

        EventConfig(mapping={
            'mouse1': self.selector.click_select,
            'mouse3': self.build_at,
            'delete': self.selector.delete,
            # 'g': self.grab,
            # 'r': self.rotate,
            # 's': self.scale
        })

    @property
    def library(self):
        return self.placer.library

    @property
    def selected(self):
        return self.selector.selected

    def build_at(self):
        phys = sim.find(PhysSystem)
        try:
            item = PhysicRay().mouse_ray(phys.groups.static)
            if item.node is None:
                return
            if not self.to_build:
                return

            model = self.placer.library.get_model(self.to_build)
            model.model_node().set_hpr(0, 90, 0)
            model.rescale(3)

            self.placer.place_item(
                Display(
                    model=model,
                    transform=ETransform(
                        position=item.pos
                    )
                )
            ).new_entity()
        except Exception as e:
            logger.warning(f'build error: {e}')

    def set_model(self, model_path: Path):
        self.to_build = model_path
        logger.info(f'model: {model_path}')


def builder_panel(floor: Floor, size: FrameSize):
    builder = Builder()
    library = builder.library

    def include_updater(text: str):
        library.query.name_include = text
        model_list.update(library.update_models())

    def exclude_updater(text: str):
        library.query.name_exclude = text
        model_list.update(library.update_models())

    model_list = PanelList(
        size=FrameSize(width=size.width, height=600),
        on_select=builder.set_model,
        namer=lambda x: f'{x.stem}'
    )
    model_list.update(library.model_paths)

    form = L.vertical(
        ui=UiConfig(name='builder', size=FrameSize(width=size.width, height=56)),
        children=[
            L.horizontal(
                ui=UiConfig(name='builder', size=FrameSize(width=size.width, height=24)),
                children=[Text.raw('include'), MyEntry(text=library.query.name_include, on_validation=include_updater)]
            ),
            L.horizontal(
                ui=UiConfig(name='builder', size=FrameSize(width=size.width, height=24)),
                children=[Text.raw('exclude'), MyEntry(text=library.query.name_exclude, on_validation=exclude_updater)]
            ),
        ])

    list_panel = L.vertical(
        ui=UiConfig(name='builder', size=FrameSize(width=size.width, height=665)),
        children=[
            form,
            model_list.panel
        ]
    )

    return L.vertical(
        ui=UiConfig(name='builder', size=size),
        children=[
            MyButton(text='generate', on_click=builder.placer.create_all),
            RigidBodyPanel(size=FrameSize(size.width, height=100)).panel,
            list_panel
        ]
    )
