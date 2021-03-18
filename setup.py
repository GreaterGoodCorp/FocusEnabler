from setuptools import setup, find_packages

with open("README.md") as fp:
    long_desc = fp.read()

setup(
    name="FocusEnabler",
    version="1.2.0",
    author="Nguyen Thai Binh",
    author_email="binhnt.mdev@gmail.com",
    description="A program to enable focus by blocking websites and more",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/GreaterGoodCorp/FocusEnabler",
    project_urls={
        "Bug Tracker": "https://github.com/GreaterGoodCorp/FocusEnabler/issues",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Home Automation",
        "Topic :: Office/Business",
        "Topic :: Utilities",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        "console_scripts": ["focus = FocusEnabler.core:run_core"],
    },
    install_requires=[
        "click",
        "colorama",
    ],
    python_requires=">=3.6",
)
