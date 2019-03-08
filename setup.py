import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='rozee_scraper',
    version='0.1',
    scripts=['rozee_scraper'],
    author="Adnan Iqbal Khan",
    author_email="hafizadnaniqbalkhan@gmail.com",
    description="A scraper for rozee.pk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AdnanIqbalKhan/rozee_scraper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
)
