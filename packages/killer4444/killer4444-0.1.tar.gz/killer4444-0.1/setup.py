from setuptools import setup, find_packages

setup(
    name='killer4444',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'name=your_package.your_script:main',
        ],
    },
)

