from setuptools import setup

setup(
	name='BlankColPruner',
	version='0.1',
	packages = ['blankcolpruner'],
	description='A commandline script to prune columns of tabular data with blank values.',
	url='https://github.com/pyeguy/BlankColPruner',
	author='Cameron Pye',
	install_requires=['pandas'],
	zip_safe=False,
	entry_points= {
		'console_scripts':['blankcolpruner=blankcolpruner.__main__:main']
		}
	
	)