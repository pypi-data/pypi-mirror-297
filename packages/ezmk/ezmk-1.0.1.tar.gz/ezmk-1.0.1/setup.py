import pathlib
import setuptools

setuptools.setup(
    name="ezmk",
    version="1.0.1",
    description="Easy-to-use color coordination terminal library with simple custmization & function binding.",
    author="Elian Groff",
    author_email="elianbgroff@gmail.com",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/ElianGroff/ezmk", 
    license="MIT", 
    project_urls={
        "Bug Tracker": "https://github.com/ElianGroff/ezmk/issues",
        "Source": "https://github.com/ElianGroff/ezmk"
    },
    classifiers=[ 
        "Programming Language :: Python :: 3", "Programming Language :: Python", "Programming Language :: Python :: 3.12", 
        "Intended Audience :: Developers", "Topic :: Software Development :: Libraries :: Python Modules", "Environment :: Console",
        "Development Status :: 3 - Alpha", "Development Status :: 4 - Beta", "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
    ],
    packages=setuptools.find_packages(include=["ezmk"]),
    #?python_requires="", #! make sure this is correct
    install_requires=[], #? might use some of these?
    setup_requires=['pytest-runner'],
    extras_require={
        'test': ['pytest', 'pytest-cov'],
    },
    #*also could use extras_require = []
    include_package_data=True,
    #?entry_points={ #? I SHOULDNT NEED ANY OF THESE
    #?    "console_scripts": [
    #?        "ezmk bind = easymark:bind",
    #?    ] # ? RESEARCH THIS tooo
    #?}
)