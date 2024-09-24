import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SPQRGames",
    version="0.0.1",
    author="CHUA某人",
    author_email="chua-x@outlook.com",
    description="SPQR Games",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CHUA-X/SPQRGames",
    packages=setuptools.find_packages(where='./src'),
    package_dir={"": "src"},
    keyword=['Python', 'python', 'SPQR', 'games', 'SLG'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6',
)
