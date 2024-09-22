# setup.py

from setuptools import setup, find_packages

setup(
    name='vehicle_lib',
    version='0.5',
    packages=find_packages(),
    install_requires=[
        'torch',
        'opencv-python',
        'ultralytics'  # Add other dependencies as needed
    ],
)

