from setuptools import setup, find_packages

# with open('./requirements.txt') as f:
# 	requirements = f.readlines()

requirements = ['colorama==0.4.4\n', 'numpy==1.21.6\n', 'pandas==1.3.5']

with open("./README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
		name ='budget_system',
		version ='1.0.1',
		author ='carlosmperilla',
		author_email ='carlosperillaprogramacion@gmail.com',
		url ='https://github.com/carlosmperilla/budget-system',
		description ='Package to manage budgets for the year, month, store and date of purchase.',
		long_description = long_description,
		long_description_content_type ="text/markdown",
		license ='MIT',
		packages = find_packages(where="."),
        include_package_data=True,
        package_data= {
            "budget_system.validators" : ["months/months_by_lang.dat",
                                          "months/months_by_lang.bak",
                                          "months/months_by_lang.dir"],
            "budget_system.settings" : ["languages/*.ini"]
        },
		entry_points ={
			'console_scripts': [
				'budgetsys = budget_system.commandline_budget:main'
			]
		},
		classifiers =[
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
        ],
		keywords ='spent expenses purchase budget system python package carlosmperilla',
		install_requires = requirements,
		zip_safe = False
)


print(find_packages(where="."))
