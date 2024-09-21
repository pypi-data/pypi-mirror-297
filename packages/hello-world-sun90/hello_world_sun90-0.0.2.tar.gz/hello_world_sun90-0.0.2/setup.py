from setuptools import setup, find_packages

setup(
    name='my_python_package',  # Replace with your package name
    version='0.0.2',  # Version of your package
    author='SD',
    description='A custom Python module for demonstrating publishing to PyPI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Sun9990/my_python_package', 
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
