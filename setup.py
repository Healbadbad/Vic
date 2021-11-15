import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vic",
    version="0.0.1",
    author="Healbadbad",
    author_email="Healbadbad@yahoo.com",
    description="A simple visual debugging tool with minimal dependencies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Healbadbad/Vic",
    project_urls={
        "Bug Tracker": "https://github.com/Healbadbad/Vic/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires="PySimpleGUI",
)