import setuptools
from setuptools.command.install import install


class CustomInstallCommand(install):
    """Customized setuptools install command - prints a friendly greeting. for now"""

    def run(self):
        install.run(self)
        print("Hello, developer, how are you? :)")


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
    version="1.1.2",
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
    },
    entry_points="""
    [console_scripts]
    meta-music=metamusic.app:run
    """,
)
