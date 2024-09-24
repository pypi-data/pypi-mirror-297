from setuptools import setup, find_packages

setup(
    name='binaexperts',  # Package name
    version='0.2.0',  # Version number
    description='A dataset conversion SDK for different Computer Vision formats',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Nastaran Dab',
    author_email='n.dab@binaexperts.com',
    license="MIT",
    packages=find_packages(),  # Automatically find and include all packages
    install_requires=[  # List dependencies here
        'PyYAML',  # Example dependency for YAML support
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version
)
