from setuptools import setup, find_packages

setup(
    name='enjoysport',
    version='0.1.6',  # or your latest version
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'enjoy-sport-cli = enjoysport.main:run',
        ],
    },
)
