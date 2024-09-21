from setuptools import setup, find_packages

setup(
    name='flaski',
    version='0.0.0.2',
    packages=['flask_crud'],
    # packages=find_packages(),
    description='Administra vistas con un enfoque diferente en flask.',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    # long_description=open('README.md').read(),
    author='Jodriz Dev',
    author_email='jrodriguez7603@utm.edu.ec',
    url='https://github.com/jrodre/flask_crud.git',
    install_requires=[
    "Flask"
    ],
)
