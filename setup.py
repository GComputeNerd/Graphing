import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crosswind",
    version="4.0.0",
    author="GComputeNerd",
    description="A simple graphing module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GComputeNerd/Graphing-Calc",
    project_urls={
        "Bug Tracker": "https://github.com/GComputeNerd/Graphing-Calc/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "graphing"},
    packages=setuptools.find_packages(where="graphing"),
    python_requires=">=3.6",
)
