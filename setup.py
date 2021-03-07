import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trading-algorithm-framework-devonindustries",
    version="0.0.3",
    author="Joshua Baker",
    author_email="jd.baker01@hotmail.co.nz",
    description="Framework for trading algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devonindustries/trading_algorithm_framework",
    project_urls={
        "Bug Tracker": "https://github.com/devonindustries/trading_algorithm_framework/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    # install_requires=[
    #     'pandas'
    # ],
    python_requires=">=3.6",
)

# Python release version syntax:
# 1.2.0.dev1   Development release
# 1.2.0a1      Alpha Release
# 1.2.0b1      Beta Release
# 1.2.0rc1     Release Candidate
# 1.2.0        Final Release
# 1.2.0.post1  Post Release
# 15.10        Date based release
# 23           Serial release