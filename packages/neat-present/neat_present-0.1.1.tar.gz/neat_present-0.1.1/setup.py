import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="neat-present",
    version="0.1.1",
    author="Lluc Simo",
    author_email="lluc.simo@protonmail.com",
    description="An image presentation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/acrilique/neat-present",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        "PySide6",
    ],
    entry_points={
        "console_scripts": [
            "neat=neat:main",
        ],
    },
    package_data={
        "neat-present": ["icon.png"],
    },
    include_package_data=True,
)