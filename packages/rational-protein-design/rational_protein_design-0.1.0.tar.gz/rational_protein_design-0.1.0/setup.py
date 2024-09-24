from setuptools import setup, find_packages

setup(
    name="rational_protein_design",
    version="0.1.0",
    description="A package for rational protein binder design using Biopython",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Rohit Satija",
    author_email="rohitsatija0092@gmail.com",
    url="https://github.com/rohitium/rational_protein_design",
    packages=find_packages(where="src"),  # Specify the 'src' directory
    package_dir={"": "src"},              # Tell setuptools to look for packages in 'src'
    install_requires=[
        "biopython>=1.79",
        "numpy>=1.21.0",
        "setuptools>=49.6.0"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    license="MIT",
    include_package_data=True,
)
