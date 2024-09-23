from setuptools import setup, find_packages

setup(
    name='Dido_pkg',  # Name of your package
    version='0.2',  # Package version
    packages=find_packages(),  # Automatically find sub-packages
    install_requires=[],  # List your dependencies here
    author='MathGhost',
    author_email='ghosal.chitran@gmail.com',
    description='Test Package',
    url='https://github.com/yourusername/my_package',  # Your package's URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
