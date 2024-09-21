from setuptools import find_packages, setup

setup(
    name="minecraft_resourcepack_indexer",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'argparse',
        'os',
        'shutil',
        'tempfile',
        'zipfile',
    ],
    entry_points={
        'console_scripts': [
            'minecraft_resourcepack_indexer=minecraft_resourcepack_indexer.main:main',
        ],
    },
)
