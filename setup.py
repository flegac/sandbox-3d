from setuptools import find_packages, setup

setup(
    name='sandbox-3d',
    version='0.1.0',
    packages=find_packages(),
    author='flo',
    description='Playing with 3D',
    install_requires=[line for line in open('requirements.txt')],
    include_package_data=True,
    options={
        'build_apps': {
            'gui_apps': {
                'sandbox': 'sandbox/main.py',
            },

            # Set up output logging, important for GUI apps!
            'log_filename': '$USER_APPDATA/sandbox/output.log',
            'log_append': False,

            # Specify which files are included with the distribution
            'include_patterns': [
                '**/*.png',
                '**/*.jpg',
                '**/*.egg',
            ],

            # Include the OpenGL renderer and OpenAL audio plug-in
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
        }
    }
)
