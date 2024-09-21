from setuptools import setup, find_packages

setup(
    name="Sasho-Neural-Network",  # The name of your package
    version='0.1.0',  # Initial release version
    author='Aleksandar Georgiev',
    author_email='aleksandargevarna@gamil.com',
    description='Simple neural network model module',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Sash0G/neural-network',
    packages=find_packages(),  # Automatically find packages in your module
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)