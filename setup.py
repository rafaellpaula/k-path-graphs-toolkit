from setuptools import setup, find_packages

setup(
    name="k-path-graphs-toolkit",
    version="0.1.0",
    description="Toolkit para gerar, converter e analisar grafos k-caminhos nao rotulados, incluindo exportacao Graph6 e calculo de conectividade algebrica.",
    author="Rafael",
    author_email="",
    license="Pendente",
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
    keywords="teoria dos grafos grafos de caminhos conectividade algebrica otimizacao",
    project_urls={
        "Documentation": "https://github.com/",
        "Source": "https://github.com/",
    },
)
