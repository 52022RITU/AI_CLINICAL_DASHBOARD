from setuptools import setup, find_packages

setup(
    name="sql_compiler",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pytest",
    ],
    entry_points={
        'console_scripts': [
            'sqlcompile=sql_compiler.cli:main',
        ],
    },
    author="52022RITU",
    author_email="rj2599648@gmail.com",
    description="A SQL query compiler implemented in Python",
)
