from setuptools import setup, find_packages

setup(
    name='encrypt666',
    version='0.1.5',
    packages=find_packages(),  # This finds the 'encrypt666' package
    install_requires=[],
    description='A custom encryption package',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/encrypt666',
    entry_points={
        'console_scripts': [
            'encrypt666=encrypt666.encrypt666:main',  # Update to the new path
        ],
    },
)
