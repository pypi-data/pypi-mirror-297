from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="az_index_maker",
    version="0.1.0",
    author="Ronak Verma",
    author_email="ronakvermagpt@gmail.com",
    description="A package to extract data from PDFs and upload to Azure Cognitive Search",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pandas",
        "PyPDF2",
        "openai",
        "azure-core",
        "azure-ai-formrecognizer",
        "azure-search-documents",
        "requests",
    ]
)

