from setuptools import setup, find_packages

setup(
    name="Brick Game with tkinter",
    version="1.2",
    packages=find_packages(),
    author="marcantonio64",
    author_email="mafigueiredo08@gmail.com",
    description="An exercise project with GUIs using tkinter",
    url="https://github.com/marcantonio64/brickgame_tkinter",
    install_requires=[
        'Pillow>=5.3.0',
        'python_version >= "3.6.8"',
    ],
)
