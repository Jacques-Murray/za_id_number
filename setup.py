"""
Package setup file for za_id_number.
"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="za_id_number",
    version="0.1.0",
    author="Jacques Murray",
    author_email="jacquesmmurray@gmail.com",
    url="https://github.com/Jacques-Murray/za_id_number",
    description="A package to validate South African ID numbers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Natural Language :: English",
    ],
    install_requires=[],
    extras_require={
        "dev": [
            "pytest",
            "twine",
            "pipreqs",
            "pylint",
            "black",
            "flake8",
            "setuptools",
        ],
    },
    python_requires=">=3.11",
)
