from setuptools import setup, find_packages

setup(
    name='snowflake_pandas',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'snowflake-connector-python[pandas]',
        'pandas'
    ],
    author='Hitesh',
    url='https://github.com/hitesh-c/snowflake-pandas',
    description='Snowflake Connector Package for Python and Pandas by hiteshlabs[dot]com.',
    long_description=open('README.md').read(),  # Ensure you have a README.md file
    long_description_content_type='text/markdown',
    license='MIT',  # Choose the appropriate license
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',  # Specify the Python version required
)

pypi-AgEIcHlwaS5vcmcCJGRkYjk2NjkxLTMyMzEtNDg2NS1iYTczLTZmMDBkZmNiMWNmMwACKlszLCIzOGQ1NWZhOC0yOWE4LTRiMzQtYTA2Yi01MWI4NzdmNTEzY2YiXQAABiB5zPFDpnfveXULwm2_EnG724LzLVV46tOJdp_sn6gKFg