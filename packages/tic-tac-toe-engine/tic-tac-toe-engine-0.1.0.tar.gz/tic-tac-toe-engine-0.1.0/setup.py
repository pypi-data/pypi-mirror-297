from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.1.0'
DESCRIPTION = 'An implementation of the Tic Tac Toe game rules'
# LONG_DESCRIPTION = 'An engine that provides full implementation of the Tic Tac Toe Game'

# Setting up
setup(
	name="tic-tac-toe-engine",
	version=VERSION,
	author="Sebastian Mendoza",
	author_email="<sebastian.mendoza.clases@gmail.com>",
	description=DESCRIPTION,
	long_description_content_type="text/markdown",
	long_description=long_description,
	packages=find_packages(),
	install_requires=[],
	keywords=['python', 'tic-tac-toe', 'tictactoe', 'game', 'engine'],
	classifiers=[
		"Development Status :: 2 - Pre-Alpha",
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 3",
		"Operating System :: Unix",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: Microsoft :: Windows",
	],
	project_urls={
	  'Source': 'https://github.com/Sebastian-0110/Tic-Tac-Toe-Engine/',
	}

)
