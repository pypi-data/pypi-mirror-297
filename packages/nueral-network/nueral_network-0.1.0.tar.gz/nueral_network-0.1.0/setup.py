from setuptools import setup, find_packages

setup(
    name='nueral_network',  # The name of your package
    version='0.1.0',  # Initial release version
    author='Aleksandar Georgiev',
    author_email='aleksandargevarna@gmail.com',
    description='neural netwrok basic operations',
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
