from setuptools import setup, find_packages

setup(
    name='ee_multi',
    version='0.1.0',
    description='A library to distribute Google Earth Engine processing across multiple accounts.',
    author='Hakimali Datardi',
    author_email='datardihakim440@gmail.com',
    packages=find_packages(),
    install_requires=[
        'earthengine-api',
    ],
)
