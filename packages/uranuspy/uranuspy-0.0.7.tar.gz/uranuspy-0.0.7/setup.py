from setuptools import setup, find_packages
from setuptools import setup, Extension
import io
from os import path

this_directory = path.abspath(path.dirname(__file__))
with io.open(path.join(this_directory, "readme.md"), encoding="utf-8") as f:
    long_description = f.read()


version_file = "uranuspy/version.py"


def get_version():
    with open(version_file, "r") as f:
        exec(compile(f.read(), version_file, "exec"))
    return locals()["__version__"]


setup(
    name="uranuspy",
    version=get_version(),
    keywords=["AI Bot", "LLM", "chatbot", "chatting"],
    description="uranuspy is the python SDK in Tianmu client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPL-3.0",
    classifiers=[
        # Operation system
        "Operating System :: OS Independent",
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        # Topics
        "Topic :: Education",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        # Pick your license as you wish
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    package_dir={"uranuspy": "uranuspy"},
    packages=find_packages(),
    include_package_data=True,
    author="Strange AI",
    author_email="strangeai2019@163.com",
    url="https://github.com/ManaAI/uranuspy",
    platforms="any",
    install_requires=[
        "websocket-client",
        "paho-mqtt",
        "validators",
        "pydantic",
        "loguru",
        "lsb_release_ex",
    ],
)
