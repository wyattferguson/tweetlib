import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wfprogressbar",
    version="0.0.1",
    author="Wyatt Ferguson",
    author_email="wyattf@gmail.com",
    description="A progress bar for terminal apps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wyattferguson/python-progressbar",
    packages=['wfprogressbar'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)