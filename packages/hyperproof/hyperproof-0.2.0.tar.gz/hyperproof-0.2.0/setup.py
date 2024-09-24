from setuptools import setup, find_packages

setup(
    name='hyperproof',                 # The name of your package
    version='0.2.0',                           # Version of your package
    description='A Python wrapper for all Hyperproof APIs',
    long_description=open('README.md').read(), # Include the README as a long description
    long_description_content_type='text/markdown',
    author='Virgil Vaduva',                        # Your name as the package author
    author_email='vvaduva@gmail.com',      # Your email
    url='https://github.com/booyasatoshi/hyperproof',  # URL to the project repo
    packages=find_packages(),                  # Automatically find the package
    install_requires=[                         # Any dependencies your project has
        'requests>=2.25.1',
    ],
    classifiers=[                              # Additional metadata
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',                   # Python version requirement
)
