from setuptools import setup, find_packages

setup(
    name="packageGES",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "openpyxl"
    ],
    include_package_data=True,
    author="Ton Nom",
    author_email="ton.email@example.com",
    description="Un package Python pour calculer les GES",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ton-utilisateur/packageGES",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
