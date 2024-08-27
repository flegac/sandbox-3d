import shutil
import sys
import zipfile
from pathlib import Path

from easy_kit.timing import time_func
from loguru import logger
from pydantic import Field

from easy_config.my_model import MyModel

SANDBOX_ROOT = Path.home() / '.sandbox'
TEMP_FOLDER = SANDBOX_ROOT / 'temp'
MODEL_ROOT = SANDBOX_ROOT / 'models'


class Query(MyModel):
    pattern: str = '*'
    path_include: str = Field(default='')
    path_exclude: str = Field(default='')
    name_include: str = Field(default='')
    name_exclude: str = Field(default='')

    def match(self, name: Path):
        path_include = not self.path_include or any([
            _ in str(name)
            for _ in self.path_include.split()
        ])
        path_exclude = all([
            _ not in str(name)
            for _ in self.path_exclude.split()
        ])
        name_include = not self.name_include or any([
            _ in name.stem
            for _ in self.name_include.split()
        ])
        name_exclude = all([
            _ not in name.stem
            for _ in self.name_exclude.split()
        ])
        return all([
            path_include,
            name_include,
            path_exclude,
            name_exclude
        ])


class Library:
    def __init__(self, root: Path):
        self.root = root

    def extensions(self, pattern: str = '*', root: Path = None):
        res = set()
        for _ in self.search(Query(pattern=pattern), root):
            res.add(_.suffix)
        return list(sorted(res))

    @time_func
    def search(self, query: Query = None, root: Path = None) -> list[Path]:
        if root is None:
            root = self.root
        if query is None:
            query = Query()
        paths = list(root.glob(f'**/{query.pattern}'))
        names = [_.name for _ in sorted(paths) if 'Knight' in str(_)]
        return list(sorted(filter(query.match, paths)))

    def load_eggs(self):
        for path in self.search(Query(pattern='*egg.zip')):
            unzip_path = TEMP_FOLDER / path.stem
            if not unzip_path.exists():
                logger.debug(f'{path.name:30} -> {unzip_path}')
                with zipfile.ZipFile(path, 'r') as zip_ref:
                    zip_ref.extractall(unzip_path)

        for path in self.search(Query(pattern='*.egg'), root=TEMP_FOLDER):
            final_path = MODEL_ROOT / path.stem
            if not final_path.exists():
                logger.debug(f'{path.name:30} -> {final_path}')
                shutil.copytree(path.parent, final_path)
            logger.debug(f'{path.name:30} -> skipped')


logger.remove()
logger.add(sys.stdout, level="INFO")


MUSIC_ROOT = Path.home() / 'Documents/Music/Cool'


if __name__ == '__main__':
    musics = Library(MUSIC_ROOT)
    sounds = musics.search(Query(pattern='*Main*.wav'))
    for _ in sounds[10:20]:
        print(_)

    library = Library(Path('/home/flo/Téléchargements/art-gallery'))
    library.load_eggs()

    for _ in library.extensions('*'):
        print(_)

    models = library.search(Query(pattern='*.egg'), MODEL_ROOT)
    for _ in models[10:20]:
        print(_)
