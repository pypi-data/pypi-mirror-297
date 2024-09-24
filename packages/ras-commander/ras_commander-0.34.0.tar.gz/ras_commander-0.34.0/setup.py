from setuptools import setup, find_packages

setup(
    name="ras-commander",
    version="0.34.0",
    packages=["ras_commander"],
    include_package_data=True,
    install_requires=[
        'pandas>=1.0.0',
        'numpy>=1.18.0',
        'h5py>=3.1.0',
        'requests>=2.25.0',
        'pathlib>=1.0.1',
        'scipy>=1.5.0',  # for KDTree
        'matplotlib>=3.3.0',  # if you're using matplotlib for plotting
    ],
    extras_require={
        'dev': [
            'pytest>=6.2.0',
            'flake8>=3.9.0',
            'black>=21.5b1',
            'sphinx>=3.5.0',
            'sphinx-rtd-theme>=0.5.0',
            'twine>=3.3.0',
        ],
    },
    python_requires='>=3.9',
    author="William M. Katzenmeyer",
    author_email="billk@fenstermaker.com",
    description="A Python library for automating HEC-RAS operations",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/billk-FM/ras-commander",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

"""
ras-commander setup.py

This file is used to build and publish the ras-commander package to PyPI.

To build and publish this package, follow these steps:

1. Ensure you have the latest versions of setuptools, wheel, and twine installed:
   pip install --upgrade setuptools wheel twine

2. Update the version number in ras_commander/__init__.py (if not using automatic versioning)

3. Create source distribution and wheel:
   python setup.py sdist bdist_wheel

4. Check the distribution:
   twine check dist/*

5. Upload to Test PyPI (optional):
   twine upload --repository testpypi dist/*

6. Install from Test PyPI to verify (optional):
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple ras-commander

7. Upload to PyPI:
   twine upload dist/*

8. Install from PyPI to verify:
   pip install ras-commander

Note: Ensure you have the necessary credentials and access rights to upload to PyPI.
For more information, visit: https://packaging.python.org/tutorials/packaging-projects/

"""
