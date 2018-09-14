import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="geneagrapher",
    version="1.0c2",
    author="David Alber",
    author_email="alber.david@gmail.com",
    description="Mathematical genealogy grapher.",
    entry_points={
        'console_scripts':
            ['ggrapher=geneagrapher.geneagrapher:ggrapher']
    },
    install_requires=['beautifulsoup4', 'lxml'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davidalber/Geneagrapher",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
