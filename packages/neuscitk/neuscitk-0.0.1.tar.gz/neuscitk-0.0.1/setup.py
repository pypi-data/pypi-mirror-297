from setuptools import setup, find_packages

with open('Readme.md', 'r') as f:
    read_me = f.read()


setup(
    name='neuscitk',
    version='0.0.1',
    description='Toolkit for companion course to UW Neusci 30x courses',
    long_description=read_me,
    packages=find_packages(include=['neuscitk', 'lasso_clusters']),
    long_description_content_type='text/markdown',
    url='https://github.com/jeremyschroeter/neuscitk',
    author='Jeremy Schroeter',
    author_email='jeremyschroeter@gmail.com',
    install_requires=[
        'numpy',
        'scipy',
        'scikit-learn',
        'matplotlib'
    ]
)