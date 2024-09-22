from setuptools import setup, find_packages

setup(
    name='tdg_sdk',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    description='SDK for interacting with TDG API',
    author='Raj Verma',
    author_email='raj.verma@mindmapdigital.ai',
    url='https://github.com/rajvermamd/tdg_sdk',  # Update with your GitHub URL
)