# token = pypi-AgEIcHlwaS5vcmcCJGE0MDA5YTg1LTY5MzUtNGY3Yi1hZDY2LTJlYzdiMmNjMThkMgACKlszLCI3ZmZhZmUzOC05ZWZlLTRiOTYtODBhZC04MTI3MDQxN2RhOGEiXQAABiBz7PycmeZ22qlS5QdO1yIZBr0-uveVGfGnWr1wKjMp4g

import setuptools

with open('README.md','r',encoding = 'utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'ooon',
    version = '0.0.1',
    author = 'Ali Ayed',
    description = 'Libary For You To Know IF You are Online or Offline',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    classifier = [
        "Programing Language :: Python :: 3",
        "Operation System :: OS Independent",
        "License :: OS Approved :: MIT License"
    ],
    package_dir = {'':'src'},
    packages = setuptools.find_packages(where = 'src'),
    install_requires = ['requests']
)
