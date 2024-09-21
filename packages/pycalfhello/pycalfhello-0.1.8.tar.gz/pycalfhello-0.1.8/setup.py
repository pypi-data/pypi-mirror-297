from setuptools import setup, find_packages
from setuptools.command.install import install

class PostInstallCommand(install):
    def run(self):
        with open('post_install_log.txt', 'w') as f:
            f.write("Post-installation script executed successfully!")
        install.run(self)

setup(
    name='pycalfhello',
    version='0.1.8',
    packages=find_packages(),
    cmdclass={
        'install': PostInstallCommand,
    },
)