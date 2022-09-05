from setuptools import setup, find_packages

setup(
    name="fu",
    version="0.2",
    install_requires=['pyquery', 'requests'],
    packages=find_packages(),
    include_package_data=True,
)
