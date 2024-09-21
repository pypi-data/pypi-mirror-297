from setuptools import setup, find_packages

def readme() -> str:
    with open('README.md') as f:
        README = f.read()
    return README

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='tes_package',
    version='0.0.2', 
    description='A simple package for testing purposes',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/aansyawaluddin/tes_package.git', 
    author='aan',
    author_email='aasyawaluddin2003@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['testing', 'example', 'simple'],
    packages=find_packages(),
    install_requires=[]
)