from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ColabKit',
    version='0.0.1',
    author='Wipodev',
    author_email='ajwipo@gmail.com',
    description='ColabKit: A Python library with essential tools to streamline your work in Google Colab, including functions for managing media, recording audio, generating interactive widgets, and performing common operations in the Colab environment.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/wipodev/ColabKit',
    project_urls={
        'Documentation': 'https://github.com/wipodev/ColabKit/blob/main/README.md',
        'Source': 'https://github.com/wipodev/ColabKit',
        'Bug Tracker': 'https://github.com/wipodev/ColabKit/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    license='MIT',
    keywords='google colaboratory ColabKit wipo wipodev functions Audio Recording Widgets Media Video Colab Python Tools',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'ipywidgets',
        'ffmpeg-python',
        'scipy',
    ],
)
