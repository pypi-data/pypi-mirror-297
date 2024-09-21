from setuptools import setup, find_packages


with open('post_install_log.txt', 'w') as f:
    f.write("Post-installation script executed successfully!")

setup(
    name='pycalfhello',
    version='0.1.7',
    packages=find_packages(),
)
