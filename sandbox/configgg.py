from pathlib import Path

from sandbox_core.assets.library import Library

ROOT_PATH = Path('C:/Users/Flo/Documents/')

DATA_ROOT = ROOT_PATH / 'Data/model3d'

LIBRARY = Library(DATA_ROOT)
GESTURE_ROOT = Path.cwd().parent / 'sandbox_lib/humanoid/assets'
