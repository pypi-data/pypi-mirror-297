from setuptools import setup, find_packages

setup(
    name='encrypt666',
    version='0.1.5.4',
    packages=find_packages(where='encrypt'),
    package_dir={'': 'encrypt'},
    install_requires=[],
    description='A custom encryption package',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/encrypt666',
    entry_points={
        'console_scripts': [
            'encrypt666=encrypt.__main__:main',
        ],
    },
)
