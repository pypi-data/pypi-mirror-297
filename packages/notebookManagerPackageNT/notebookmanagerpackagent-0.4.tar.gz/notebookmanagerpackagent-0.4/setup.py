from setuptools import setup, find_packages

setup(
    name="notebookManagerPackageNT",  # The name of your package
    version="0.4",
    packages=find_packages(),
    install_requires=[],
    author="Shashank",
    author_email="shashank.b@hoonartek.com",
    description="A package to manage the execution of multiple notebooks",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
