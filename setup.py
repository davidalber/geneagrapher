import setuptools

with open("README.md", "r") as fin:
    long_description = fin.read()

setuptools.setup(
    name="geneagrapher",
    version="1.0",
    author="David Alber",
    author_email="alber.david@gmail.com",
    description="Mathematical genealogy grapher.",
    entry_points={
        'console_scripts':
            ['ggrapher=geneagrapher.geneagrapher:ggrapher']
    },
    install_requires=['beautifulsoup4==4.6.3', 'lxml==4.2.5'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davidalber/geneagrapher",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
