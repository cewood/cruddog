from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='cruddog',
    version='0.1',
    py_modules=['cruddog'],
    include_package_data=True,
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        inout=cruddog:main
    ''',
)
