from setuptools import setup, find_packages

setup(
    name='surveillance_project',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-contrib-python',
        'Pillow',
        'scipy',
    ],
)
