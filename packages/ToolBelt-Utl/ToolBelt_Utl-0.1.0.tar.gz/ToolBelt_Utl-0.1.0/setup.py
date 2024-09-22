from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name = 'ToolBelt_Utl',
    version = '0.1.0',
    author = 'Wyatt Bramblett',
    author_email = 'wbramblett1@gmail.com',
    license = 'MIT',
    description = 'Cache commonly used commands',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = '',
    py_modules = ['commands','toolbelt'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        toolbelt=toolbelt:cli
    '''
)
