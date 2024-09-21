from distutils.core import setup
from setuptools.command.install import install


class PostInstallCommand(install):
    def run(self):
        try:
            with open('/tmp/post_install_log-final.txt', 'w') as f:
                f.write("Post-installation script executed successfully!")
        except:
            print("An exception occurred") 
        install.run(self)

setup(
    name="pycalfhello",
    packages=["pycalfhello"],
    version="0.3",
    description="A harmless package to prevent exploitation",
    author="Paolo Raffini",
    author_email="test@test.com",
    cmdclass={
        "install": PostInstallCommand,
    },
    entry_points={
        "console_scripts": [
            "pycalfhello = pycalfhello.cli:cli",
        ],
    },
)
