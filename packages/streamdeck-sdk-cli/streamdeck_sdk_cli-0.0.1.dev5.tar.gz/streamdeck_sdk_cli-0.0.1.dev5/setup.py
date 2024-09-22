import setuptools

VERSION = "0.0.1.dev5"
PACKAGE_DIR = "."

setuptools.setup(
    name="streamdeck_sdk_cli",
    version=VERSION,
    author="Grigoriy Gusev",
    author_email="thegrigus@gmail.com",
    description="Command Line Interface for streamdeck-sdk.",
    long_description="",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where=PACKAGE_DIR),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    license="Apache Software License",
    keywords=[
        "streamdeck sdk cli",
        "streamdeck test project",
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
    entry_points={
        'console_scripts': [
            'streamdeck_sdk=streamdeck_sdk_cli.executable.executable:main',
        ],
    },
)
