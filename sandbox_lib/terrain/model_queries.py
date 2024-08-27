from sandbox_core.assets.library import Query
from sandbox_gui.features.editor.item_placer import ItemPlacer
from sandbox_gui.features.editor.model_library import ModelLibrary

GRASS_QUERY = Query(
    pattern='*.fbx',
    name_include=' '.join(['Grass_Patch', ]),
    name_exclude=' '.join(['Snow', ])
)
ROCK_QUERY = Query(
    pattern='*.fbx',
    name_include=' '.join(['Env_Rock_', ]),
    name_exclude=' '.join(['Snow', 'Round Grey Brown Large Alt'])
)
PINE_TREE_HIGH = Query(
    pattern='*.fbx',
    name_include=' '.join([
        'Tree_Pine',
    ]),
    path_include='POLYGON_Vikings_Source_Files_v2',
    name_exclude=' '.join([
        'Snow',
    ])
)
PINE_TREE_LOW = Query(
    pattern='*.fbx',
    name_include=' '.join([
        'SM_Env_Tree_',
    ]),
    path_include='Simple_Trains_Source_Files',
    name_exclude=' '.join([
        'Snow',
    ])
)
TREES = ItemPlacer(ModelLibrary(
    query=PINE_TREE_HIGH
))
GRASS = ItemPlacer(ModelLibrary(
    query=GRASS_QUERY
))
ROCKS = ItemPlacer(ModelLibrary(
    query=ROCK_QUERY
))
ROCKS.item_map = GRASS.item_map = TREES.item_map
