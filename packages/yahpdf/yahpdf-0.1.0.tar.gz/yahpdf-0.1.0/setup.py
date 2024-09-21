from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="yahpdf",
    version="0.1.0",
    author="Yahya Abulhaj",
    author_email="dev@yahya-abulhaj.dev",
    description="A CLI tool for analyzing PDF files",
    long_description="Tools I needed so I thought to ship them as a CLI",
    long_description_content_type="text/markdown",
    url="https://github.com/yaya2devops/yahpdf",
    packages=find_packages(),
    install_requires=[
        "PyPDF2",
        "matplotlib",
        "wordcloud",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "yahpdf=yahpdf.pdf_tool:main",
        ],
    },
    python_requires=">=3.6",
)