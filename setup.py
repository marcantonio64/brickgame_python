from setuptools import setup, find_packages

setup(
    name="Brick Game with Python",
    version="1.2",
    packages=find_packages(),
    author="marcantonio64",
    author_email="mafigueiredo08@gmail.com",
    description="An exercise project with GUIs using python",
    url="https://github.com/marcantonio64/brickgame_python",
    install_requires=[
        'Pillow>=5.3.0',
        'python_version >= "3.6.8"',
    ],
)
