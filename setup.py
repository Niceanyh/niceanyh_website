from setuptools import find_packages, setup

setup(
    name='niceanyh2focus',
    version='1.0.0',
    author = "Niceanyh",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)