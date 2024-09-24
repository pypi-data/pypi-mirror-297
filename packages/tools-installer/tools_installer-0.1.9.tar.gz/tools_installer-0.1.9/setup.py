from setuptools import setup, find_packages

VERSION = '0.1.9'
DESCRIPTION = 'tools-shutil-installer for copy files to other or Doing stuff'
LONG_DESCRIPTION = 'My first Python package with tools-installer that require shutil'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="tools_installer",
        version=VERSION,
        author="Raiz Apps",
        author_email="raizhaikal82@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that
        # needs to be installed along with your package. Eg: 'caer'
        keywords=['python', 'first package'],
        classifiers= [
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)