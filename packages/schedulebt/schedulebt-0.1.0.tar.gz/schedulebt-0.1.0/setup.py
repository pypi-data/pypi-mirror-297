from setuptools import setup, find_packages

setup(
    name='schedulebt',
    version='0.1.0',
    author='',
    # author_email='your.email@example.com',
    description='A simple tools to optimize work schedule and estimate finish duration distribution',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
        'cvxpy',
        'pyscipopt'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
