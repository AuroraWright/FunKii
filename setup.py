from setuptools import setup, find_packages

setup(
    name='FunKii',
    version='1.0',
    url='https://github.com/llakssz/FunKiiU',
    author='cearp/the cerea1killer/AuroraWright',
    license='GPLv3',
    description='Download Wii titles from the CDN',
    install_requires=[''],
    packages=find_packages(),
    entry_points={'console_scripts': ['FunKii=FunKii.__main__:main']},
)
