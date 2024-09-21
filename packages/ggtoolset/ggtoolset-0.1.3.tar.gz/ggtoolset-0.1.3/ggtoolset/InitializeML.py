#!/usr/bin/env python
import os
import argparse
import sys
import datetime
import typing

class InitializeML:
	def __init__(self, sys_argv:str=None)->None:
		if None==sys_argv:                                                   
			sys_argv = sys.argv[1:]
		self.args=self.parse(sys_argv)
		if None==self.args.project_name:
			raise ValueError("You must specify a project name (--project_name PROJECT_NAME)")
		self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
		self.project_name = self.args.project_name
		# Define the directory structure
		self.directories = [
			f"{self.project_name}/data/raw",
			f"{self.project_name}/data/processed",
			f"{self.project_name}/notebooks",
			f"{self.project_name}/src",
			f"{self.project_name}/models",
			f"{self.project_name}/reports"
		]

		# Define the files to be created
		self.files = [
			f"{self.project_name}/src/__init__.py",
			f"{self.project_name}/src/DataPreprocessing.py",
			f"{self.project_name}/src/FeatureEngineering.py",
			f"{self.project_name}/src/ModelTraining.py",
			f"{self.project_name}/src/ModelEvaluation.py",
			f"{self.project_name}/src/Model.py",
			f"{self.project_name}/src/Utils.py",
			f"{self.project_name}/requirements.txt",
			f"{self.project_name}/README.md",
			f"{self.project_name}/setup.py",
			f"{self.project_name}/version",
		]

	def parse(self,sys_argv:typing.List[str])->argparse.Namespace:
		self.parser=argparse.ArgumentParser()
		self.parser.add_argument('--project_name',
            help='The name of the project',
            default=None,
            type=str,
        )
		args = self.parser.parse_args(sys_argv)
		return args


	def process(self)->None:
		# Create directories
		for directory in self.directories:
			os.makedirs(directory, exist_ok=True)
		# Create files
		for file in self.files:
			if not os.path.exists(file):
				with open(file, 'w') as f:
					pass  # Create an empty file
		return

	
if "__main__" == __name__:
	init = InitializeML()
	init.process()
	print("Project initialized successfully!")