from setuptools import setup, find_packages

setup(
    name='telegraph_uploader',
    version='1.0',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=['requests'],
    author='viendi',
    author_email='viendii@gmail.com',
    description='A Python library for interacting with the Telegraph API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/lunaticsm/Telegraph',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)