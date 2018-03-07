import setuptools
import os


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
    version="1.0.3",
    url="https://github.com/unique1o1/Meta-Music",
    author="Yunik Maharjan",
    author_email="yunik.maharjan@icloud.com",
    license='MIT',
    description="Metamusic",
    platforms="Linux, MacOS, Windows",
    long_description=open('README.md').read(),
    include_package_data=True,
    install_requires=REQUIREMENTS,

    packages=setuptools.find_packages(),
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python :: 3.6'
    ],
    # download_url='https://github.com/unique1o1/ROI2TEXT/archive/v1.1.tar.gz',
    entry_points="""
    [console_scripts]
    meta-music=metamusic.app:run
    """,
)
