from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='jje_cli',
    version='0.1.2',
    author='John Gbaya-kokoya Jr',
    author_email='gbayakokoyajohnjr@gmail.com',
    description='A simple to use CLI tool for creating a Vuejs project scaffold with Django as backend',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/jje_cli",
    packages=find_packages(),
    install_requires=[
        'click',
        'GitPython'
    ],
    entry_points='''
        [console_scripts]
        jje=jje_cli.cli:cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
