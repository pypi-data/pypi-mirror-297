import setuptools
from pathlib import Path

long_desc = Path("README.md").read_text(encoding="utf-8")
setuptools.setup(
    name="holamundoplayerrbardalp",  # package name in Pypi
    version="0.0.1",
    long_description=long_desc,  # package description which will be shown in pypi
    packages=setuptools.find_packages(
        exclude=["mocks", "tests"]  # excluding packages
    )
)
