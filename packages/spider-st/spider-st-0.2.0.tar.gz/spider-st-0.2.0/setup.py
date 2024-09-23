import setuptools
import os
# os.system("SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=TRUE")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spider-st",
    version="0.2.0",
    author="Li Shiying",
    author_email="shiyingli7-c@my.cityu.edu.hk",
    description="Identifying spatially variable interactions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deepomicslab/SPIDER",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    package_data={'lrdb': ['*.tsv'],
                 'R_script': ['*.R']},
    include_package_data=True,
    install_requires=[
        'anndata>=0.8.0',
        'numpy',
        'Cython',
        'cellrank',
        'fa2',
        'gseapy',
        'h5py',
        'igraph',
        'leidenalg',
        'louvain',
        'matplotlib',
        'matplotlib-venn',
        'networkx',
        'numba',
        'numpy',
        'pandas',
        'plotly',
        'pygco',
        'scanpy',
        'scgco',
        'scikit-learn',
        'scipy',
        'scvelo',
        'seaborn',
        'somde',
        'somoclu',
        'spatialde',
        'stlearn',
        'umap-learn',
        'statsmodels',
        'scprep',
        'squidpy',
        'magic-impute',
        'NaiveDE',
        'gpflow',
        'statannotations',
        'tensorflow>=2.12',
        'holoviews'
    ],
)