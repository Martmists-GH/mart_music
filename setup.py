# External Libraries
from setuptools import setup, find_packages

VERSION = "0.1.0"
DESCRIPTION = ""
README = ""


if __name__ == '__main__':
    setup(
        name="mart_music",
        author="martmists",
        author_email="mail@martmists.com",
        maintainer="martmists",
        maintainer_email="mail@martmists.com",
        license="MIT",
        zip_safe=False,
        version=VERSION,
        description=DESCRIPTION,
        long_description=README,
        url="https://github.com/martmists/mart_music",
        packages=find_packages(),
        extras_require={
            "sync": ["requests"],
            "async": ["aiohttp"]
        },
        keywords=[
            "music", "python", "API", "discord", "opus", "key"
        ],
        classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Console", "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Topic :: Software Development :: Libraries :: Python Modules"
        ]
    )
