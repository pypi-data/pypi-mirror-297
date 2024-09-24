from setuptools import setup, find_packages

setup(
    name="CBZpliers",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "lxml",
    ],
    entry_points={
        'console_scripts': [
            'combine_cbz=src.main:main',
        ],
    },
    author="Szymon Sciegienka",
    author_email="szymon.sciegienka@gmail.com",
    description="A tool to combine multiple .cbz files into one.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Sigosu/CBZpliers",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version required
)