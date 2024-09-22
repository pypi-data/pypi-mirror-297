from setuptools import setup, find_packages

setup(
    name='balboniprint',
    version='0.1.1',
    author='sud0luke',
    author_email='sud0luke@proton.me',
    description='An easy-to-use package for custom formatted printing.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/lukesudom/balboniprint',
    packages=find_packages(),
    install_requires=[
        'termcolor',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
