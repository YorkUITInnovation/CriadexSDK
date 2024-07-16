import setuptools

setuptools.setup(
    name="CriadexSDK",
    packages=setuptools.find_packages(),
    version="1.2.2",
    description="Criadex SDK Client",
    author="Isaac Kogan",
    author_email="koganisa@yorku.ca",
    url="https://github.com/CriaYU/Criadex.git",
    download_url="https://github.com/CriaYU/Criadex.git",
    keywords=["cria", "criadex", "criadexsdk", "sdk"],
    install_requires=[
        "httpx>=0.25.1",  # Make requests
        "pydantic>=2.5.1"  # Connecting to websocket server
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ]
)
