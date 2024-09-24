"""Setup file for xcube_4d_viewer."""
import os

from setuptools import find_packages
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version_number = 'v1.1.0'  # default value when under development

setup(
    name='xcube_4d_viewer_vg',
    version=version_number,
    description='API extension to the xcube server allowing cubes to be viewed in the 4D viewer.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='',
    author_email='',
    python_requires=">=3.9",
    packages=find_packages(),
    license='MIT',
    # note requirements listed in install_requires should be the *minimum required*
    # in order to allow pip to resolve multiple installed packages properly.
    # requirements.txt should contain a specific known working version instead.
    install_requires=[
    ],
    entry_points={
        'xcube_plugins': [
            # This is xcube convention
            'xcube_4d_viewer = xcube_4d_viewer.plugin:init_plugin',
        ],
    }
)
