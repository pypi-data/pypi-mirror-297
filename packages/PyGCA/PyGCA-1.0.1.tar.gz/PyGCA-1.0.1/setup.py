from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
long_description = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="PyGCA",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "PyGithub==2.4.0",
        "pytest==8.3.3",
        "requests==2.32.3",
        "certifi==2024.8.30",
        "cffi==1.17.1",
        "charset-normalizer==3.3.2",
        "cryptography==43.0.1",
        "Deprecated==1.2.14",
        "idna==3.10",
        "iniconfig==2.0.0",
        "Jinja2==3.1.4",
        "MarkupSafe==2.1.5",
        "packaging==24.1",
        "pluggy==1.5.0",
        "pycparser==2.22",
        "PyJWT==2.9.0",
        "PyNaCl==1.5.0",
        "typing_extensions==4.12.2",
        "urllib3==2.2.3",
        "wrapt==1.16.0",
    ],
    description="A tool for detecting and analyzing Python operators like arithmetic, bitwise, comparison, and more.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Clintaire",
    author_email="clintaire@gmail.com",
    url="https://github.com/clintaire/PyGCA",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
