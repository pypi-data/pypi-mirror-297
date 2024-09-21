from setuptools import setup

setup(
    name="ALine",
    version="1.0.0",
    description="Line Analyser",
    long_description="A library for analyse lines and debug",
    author="BOXER",
    author_email="vagabonwalybi@gmail.com",
    maintainer="BOXER",
    maintainer_email="vagabonwalybi@gmail.com",
    url="https://github.com/BOXERRMD/ALine_module",
    project_urls={
        'Documentation': 'https://github.com/BOXERRMD/ALine_module/wiki',
        'GitHub': 'https://github.com/BOXERRMD/ALine_module',
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        "Operating System :: Microsoft :: Windows :: Windows 10"
    ],
    install_requires=[
        "immutable-Python-type==1.1.0"
    ],

    packages=['ALine'],
    python_requires=">=3.9",
    include_package_data=True,
)