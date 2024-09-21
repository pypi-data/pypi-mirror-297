from setuptools import setup, find_packages

setup(
    name='duckgpt',
    version='1.0.0',
    author='github.com/tanmaysingh3856',
    description='A Python client for DuckGPT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tanmaysingh3856/duckgpt',
    packages=find_packages(),
    install_requires=[
        'requests',
        'googlesearch-python'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)