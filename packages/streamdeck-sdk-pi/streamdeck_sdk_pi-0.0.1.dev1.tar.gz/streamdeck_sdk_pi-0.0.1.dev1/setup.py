import setuptools

VERSION = "0.0.1dev1"
PACKAGE_DIR = "."

setuptools.setup(
    name="streamdeck_sdk_pi",
    version=VERSION,
    author="Grigoriy Gusev",
    author_email="thegrigus@gmail.com",
    description="Library for creating Stream Deck Property Inspector in Python.",
    long_description="",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where=PACKAGE_DIR),
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    license="Apache Software License",
    keywords=[
        "property inspector",
        "property inspector generator",
        "streamdeck property inspector generator",
        "streamdeck property inspector",
        "streamdeck pi",
        "python",
        "sdk",
        "streamdeck",
        "streamdeck-sdk",
        "streamdeck_sdk",
        "stream deck sdk",
        "stream deck",
        "elgato",
        "elgato sdk",
        "elgato stream deck",
        "streamdeck-python-sdk",
        "streamdeck_python_sdk",
        "streamdeck python sdk",
    ],
    install_requires=[
    ],
)
