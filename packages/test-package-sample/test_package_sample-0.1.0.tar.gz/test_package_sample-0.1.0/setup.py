from setuptools import setup
from setuptools.command.install import install
import os

class CustomInstallCommand(install):
    def run(self):
        # Create /tmp/.log-1.txt with "Hello" as content
        with open('/tmp/.log-1.txt', 'w') as f:
            f.write('Hello\n')
        print("Custom install: Created /tmp/.log-1.txt with 'Hello'")
        # Continue with normal installation
        install.run(self)

setup(
    name='test_package_sample',
    version='0.1.0',
    packages=['test_package_sample'],
    cmdclass={
        'install': CustomInstallCommand,
    },
)
