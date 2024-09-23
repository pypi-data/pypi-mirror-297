from setuptools import find_packages, setup

version = "1.0.0"

install_requires = [
    "cmd2==1.5.0",
]

dev_extras = [
    "pep8",
    "pypandoc",
    "pre-commit",
    "mypy",
    "pytest",
]

docs_extras = [
    "Sphinx>=1.0",  # autodoc_member_order = 'bysource', autodoc_default_flags
    "sphinx_rtd_theme",
    "sphinxcontrib-programoutput",
]

try:
    import pypandoc

    long_description = pypandoc.convert_file("README.md", "rst")
    long_description = long_description.replace("\r", "")

except (IOError, ImportError, AttributeError):
    import io

    with io.open("README.md", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="ph4-acmd2",
    version=version,
    description="Cmd2 extension for async programs",
    long_description=long_description,
    url="https://github.com/ph4r05/ph4-acmd2",
    author="Dusan Klinec",
    author_email="dusan.klinec@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        "dev": dev_extras,
        "docs": docs_extras,
    },
    entry_points={
        "console_scripts": [],
    },
)
