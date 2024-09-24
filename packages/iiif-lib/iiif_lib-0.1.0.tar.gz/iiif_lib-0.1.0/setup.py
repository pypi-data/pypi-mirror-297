from setuptools import setup, find_packages

setup(
    name="iiif-lib",
    version="0.1.0",
    description="Library to generate IIIF 2.1 and 3.0 manifests",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Pedro Urra",
    author_email="urrape@gmail.com",
    url="https://gitlab.com/urrape/iiif_lib.git",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
    ],
)