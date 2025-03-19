from setuptools import setup, find_packages

setup(
    name="packageGES",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[ # les packages nécéssaire au code
        "pandas",
        "openpyxl"
    ],
    include_package_data=True, # Permet d'inclure des fichiers non-Python
    author="Julia",
    description="Un package Python pour calculer les GES",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Hazelya/packageGES",
    python_requires=">=3.7",
)


