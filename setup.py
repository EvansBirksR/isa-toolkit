from setuptools import setup, find_packages

setup(
    name="isa-toolkit",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "isa-toolkit=isa_toolkit.cli:main",
        ],
    },
    python_requires=">=3.8",
    description="A library providing international standard atmosphere tools for aerospace applications.",
    author="Rory Evans Birks",
    license="MIT",
)
