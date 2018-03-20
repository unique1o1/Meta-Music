import setuptools
import sys
import os
from setuptools.command.install import install

from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
from pathlib import Path


class CustomInstallCommand(install):
    """Customized setuptools install command - prints a friendly greeting. for now"""

    def run(self):
        install.run(self)
        custom_command()


class CustomEggInfoCommand(egg_info):
    """Customized setuptools install command - prints a friendly greeting. for now"""

    def run(self):
        egg_info.run(self)
        custom_command()


class CustomDevelopCommand(develop):
    """Customized setuptools install command - prints a friendly greeting. for now"""

    def run(self):
        develop.run(self)
        custom_command()


def custom_command():
    if sys.platform == 'linux':
        home = os.path.join(Path.home(), '.metamusic')
        if not os.path.exists(home):
            os.mkdir(home)
        os.system(f'cp ./metamusic/metamusic.png {home}')
        desk = f'''\
[Desktop Entry]
Version=1.0
Type=Application
Terminal=false
Name=Meta-Music
Exec=meta-music
Icon={home}/metamusic.png
StartupNotify=true
Categories=Application;'''
        with open('./metamusic/meta-music.desktop', 'w') as f:
            f.write(desk)

        os.system(
            'sudo cp ./metamusic/meta-music.desktop /usr/share/applications/')
        print("Adding desktop icon....")


def parse_requirements(requirements):
    # load from requirements.txt
    with open(requirements) as f:
        lines = [l for l in f]
        # remove spaces
        stripped = map((lambda x: x.strip()), lines)
        # remove comments
        nocomments = filter((lambda x: not x.startswith('#')), stripped)
        # remove empty lines
        reqs = filter((lambda x: x), nocomments)
        return reqs


REQUIREMENTS = parse_requirements("requirements.txt")
setuptools.setup(
    name="MetaMusic",
    version="1.1.6",
    url="https://github.com/unique1o1/Meta-Music",
    author="Yunik Maharjan",
    author_email="yunik.maharjan@icloud.com",
    license='MIT',
    description="Metamusic",
    platforms="Linux, MacOS, Windows",
    long_description=open('README.md').read(),
    include_package_data=True,
    install_requires=[i for i in REQUIREMENTS],

    packages=setuptools.find_packages(),
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python :: 3.6'
    ],
    cmdclass={
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand,
        'egg_info': CustomEggInfoCommand
    },
    entry_points="""
    [console_scripts]
    meta-music=metamusic.app:run
    """,
)
