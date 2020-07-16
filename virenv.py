import os.path as path
import subprocess
import time
import uuid
from shutil import rmtree


def virtual_environment_decorator(base):
	def wrapped_with_base(func):
		def wrapped_with_decorator(code=None, requirements=None):
			env = _VirtualEnvironment(base, requirements)
			result = env.execute(code)
			env.destroy()
			return result
		
		return wrapped_with_decorator
	
	return wrapped_with_base


class _VirtualEnvironment:
	""" represents python virtual environment"""
	
	def __init__(self, base, requirements=[]):
		self.__requirements = requirements
		self.__envname = uuid.uuid4().hex[:6].upper()
		self.__envpath = path.join(base, self.__envname)
		self.__create_time = int(round(time.time() * 1000))
		
		print("Created venv [envname:{} | envpath:{} | create_time:{} | requirements:{}]".format(self.__envname,
		                                                                                         self.__envpath,
		                                                                                         self.__create_time,
		                                                                                         self.__requirements))
		
		if path.exists(self.__envpath):
			raise Exception("Failed to create venv {}. Dir already exists".format(self.__envpath))
		
		self.__CREATE_ENV = "python -m venv {}".format(self.__envpath)
		self.__ACTIVATE_ENV = "cd {} && source bin/activate".format(self.__envpath)  # activate venv
		self.__INSTALL_REQUIREMENTS = "pip install {}".format(" ".join(self.__requirements)) if len(
			self.__requirements) > 0 else "echo"
		self.__DEACTIVATE_ENV = "deactivate"
		
		process = subprocess.Popen(
			"; ".join([self.__CREATE_ENV, self.__ACTIVATE_ENV, self.__INSTALL_REQUIREMENTS, self.__DEACTIVATE_ENV]),
			shell=True)
		process.communicate()  # wait for requirements to finish
	
	def execute(self, pycode):
		"""
		running code inside virtual environment
		:param pycode:
		:return: std output
		"""
		res = subprocess.Popen(
			"; ".join([self.__ACTIVATE_ENV, "python -c '''{}'''".format(pycode), self.__DEACTIVATE_ENV]), shell=True,
			stdout=subprocess.PIPE)
		return res.communicate()[0].strip()  # wait for shell process to finish
	
	def destroy(self):
		""" destroy virtual environment """
		rmtree(self.__envpath)
		pass
	
	def get_name(self):
		""" get the name of the virtual environment """
		return self.__envname
	
	def get_requirements(self):
		""" get list of requirements for the virtual environment"""
		return self.__requirements
