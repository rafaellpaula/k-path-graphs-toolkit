from setuptools import setup, find_packages

setup(
    name="k-path-graphs-toolkit",
    version="0.1.0",
    description="Toolkit for generating, converting, and analyzing unlabeled k-path graphs, including Graph6 export and algebraic connectivity computation.",
    author="Rafael",
    author_email="",
    license="Pending",
    packages=find_packages(),
    install_requires=[
        "numpy>=2.0",
        "networkx>=3.6",
        "graphviz>=0.21",
        "matplotlib>=3.10",
        "scipy>=1.17",
    ],
    extras_require={
        "jupyter": ["jupyter>=1.1", "ipython>=9.0", "ipykernel>=7.0"],
        "dev": ["pytest", "black", "pylint"],
    },
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="graph theory path graphs algebraic connectivity optimization",
    project_urls={
        "Documentation": "https://github.com/",
        "Source": "https://github.com/",
    },
)
