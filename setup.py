from setuptools import setup

requirements = ['click', 'pyexcel']

setup(
    name='sheet2sql',
    version='1.0',
    packages=['sheet2sql'],
    install_requires=requirements,
    author='Gabriel Cruz',
    author_email='gabriel.cruz232@gmail.com',
    entry_points={
        'console_scripts': ['sheet2sql = sheet2sql.sheet2sql:sheet2sql']},
    license='MIT')
