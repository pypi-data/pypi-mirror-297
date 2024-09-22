from setuptools import setup, find_packages

setup(
    name='MatQ',
    version='0.0.1',
    packages=find_packages(),
    description='A simple math library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Rovren Inc,',
    author_email='asheemak@gmail.com',
    # url='https://github.com/Rovren/DataQ',  # optional
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
