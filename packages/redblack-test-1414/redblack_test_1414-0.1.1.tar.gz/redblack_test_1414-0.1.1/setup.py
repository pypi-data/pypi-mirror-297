from setuptools import setup, find_packages

setup(
    name='redblack_test_1414',
    version='0.1.1',
    description='A brief description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Use markdown for README
    author='redblack_test_1414',
    author_email='test.email@example.com',
    url='https://github.com/test/your-repo',
    packages=find_packages(),  # Automatically find sub-packages
    install_requires=[          # List dependencies here
        'requests',             # Example dependency
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
