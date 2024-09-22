import setuptools

VERSION = "1.2.0.dev3"
PACKAGE_DIR = "."

setuptools.setup(
    name="streamdeck_sdk",
    version=VERSION,
    author="Grigoriy Gusev",
    author_email="thegrigus@gmail.com",
    description="Library for creating Stream Deck plugins in Python.",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/gri-gus/streamdeck-python-sdk",
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
        "annotated-types==0.7.0",
        "decohints==1.0.9",
        "pydantic==2.8.2",
        "pydantic_core==2.20.1",
        "typing_extensions==4.12.2",
        "websockets==13.0.1",
    ],
    extras_require={
        "dev": [
            "streamdeck-sdk-cli>=0.0.1.dev6,<0.0.2",
            "streamdeck-sdk-pi>=0.0.1.dev1,<0.0.2",
        ]
    },
)
