# ccAFv2: Cell cycle classifier for Python and scanpy
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

This repository is for the Python package for the cell cycle classifier ccAFv2. The input for the ccAFv2 classifier is single cell or nuclei, or spatial RNA-seq data.  The features of this classifier are that it classifies six cell cycle states (G1, Late G1, S, S/G2, G2/M, and M/Early G1) and a quiescent-like G0 state, and it incorporates a tunable parameter to filter out less certain classifications. This package is implemented in Python so that it can be used in [scanpy](https://scanpy.readthedocs.io/en/stable/) analysis workflows. We provide examples of how to install, run ccAFv2 on scanpy objects (sc/snRNA-seq), and plot and use results.

## Table of Contents

- [Install](#install)
    - [Requirements](#requirements)
        - [Dependencies](#dependencies)
        - [Docker image](#docker-image)
    - [Installing ccAFv2](#installing-ccafv2)
- [Classifying single cell or nuclei RNA-seq](#classifying-single-cell-or-nuclei-rna-seq)
    - [Input for classification](#input-for-classification)
    - [Test data](#test-data)
	- [Cell cycle classification](#cell-cycle-classification)
    - [Plotting cell cycle states](#plotting-cell-cycle-states)
        - [Plotting a UMAP with cell cycle states](#plotting-a-umap-with-cell-cycle-states)
- [Maintainers](#maintainers)
- [Contributing](#contributing)

## Install

### Requirements

It is strongly suggested that users utilize the docker images we provide on DockerHub as they contain all dependencies needed to run ccAFv2.

#### Dependencies
There are four dependencies that must be met for ccAF to classify cell cycle states:
1. [numpy](https://numpy.org/) - ([install](https://numpy.org/install/))
2. [scipy](https://www.scipy.org/index.html) - ([install](https://www.scipy.org/install.html))
3. [scanpy](https://scanpy.readthedocs.io/en/latest/) - ([install](https://scanpy.readthedocs.io/en/latest/installation.html))
4. [tensorflow](https://www.tensorflow.org/) - ([install](https://www.tensorflow.org/install))
5. [keras](https://keras.io/) - ([install](https://keras.io/getting_started/))

##### Python dependency installation commands
> **NOTE!**  pip may need to be replaced with pip3 depending upon your setup.

```sh
pip install numpy scipy scanpy tensorflow keras
```

#### Installation of ccAF classifier
The ccAFv2 classifier can be installed with the following command:

```sh
pip install ccAFv2
```

#### Docker image

We facilitate the use of ccAFv2 by providing a Docker Hub container [cplaisier/ccafv2](https://hub.docker.com/r/cplaisier/ccafv2) which has all the dependencies and libraries required to run the ccAF classifier. To see how the Docker container is configured plaese refer to the [Dockerfile](https://github.com/plaisier-lab/docker_ccafv2/blob/master/Dockerfile). Please [install Docker](https://docs.docker.com/get-docker/) and then from the command line run:

```sh
docker pull cplaisier/ccafv2_py
```

Then run the Docker container using the following command (replace <path to scRNA-seq profiles directory> with the directory where you have the scRNA-seq data to be classified):

```sh
docker run -it -v '<path to scRNA-seq profiles directory>:/files' cplaisier/ccafv2_py
```

This will start the Docker container in interactive mode and will leave you at a command prompt. You will then want to change directory to where you have your scRNA-seq or trasncriptome profiling data.

## Classifying single cell or nuclei RNA-seq

### Input for classification

It is expected that the input for the ccAFv2 classifier will be a scanpy AnnData object that has been thorougly quality controlled. Is is preferred that the data in the object be SCTransformed, however, the standard approach for normalization only applies to the highly variable genes. This can exclude genes needed for the accurate classification of the cell cycle. During the running of the ccAFv2 classifier it will tell you how many genes overlap with the classifier marker genes.

### Test data

The human neural stem cells (hNSCs) from a human fetus 8 weeks post-conception (PCW8) [(Zeng et al., 2023)](https://pubmed-ncbi-nlm-nih-gov.ezproxy1.lib.asu.edu/37192616/) is available for use as a testing dataset:
- [PCW8 hNSCs h5ad file](https://zenodo.org/records/10968634/files/W8-1_normalized_ensembl.h5ad?download=1)

Download this file and place it into the directory in which you wish to run the ccAFv2 tutorial below. This data has been QC'd and normalized using SCTransform in Seurat following our best practices [here](https://github.com/plaisier-lab/ccafv2_R/blob/main/README.md#input-for-classification).

### Cell cycle classification

Classification is as easy as two lines that can be added to any Seurat workflow. First the library must be loaded and then the PredictCellCycle function is run:

```python
# Load packages
import pandas as pd
import scanpy as sc
import ccAFv2

# Load up test dataset
PCW8 = sc.read_h5ad('W8-1_normalized_ensembl.h5ad')

# Run ccAFv2 to predict cell labels
PCW8_labels = ccAFv2.predict_labels(PCW8, species='human', gene_id='ensembl')
```
When the classifier is running it should look something like this:

```python
Running ccAFv2:
    Preparing data for classification...
    Marker genes present in this dataset: 845
    Missing marker genes in this dataset: 16
  Predicting cell cycle state probabilities...
  Choosing cell cycle state...
Done.
```

It is important to look at how many marker genes were present in the dataset. We found that when less than 689 marker genes (or 80%) were found in the dataset that this led significantly less accurate predictions. And some of the later values for the timing and 93/93 may differ for your dataset, which is perfectly fine.

There are several options that can be passed to the PredictCellCycle function:

```python
ccAFv2.predict_labels(scanpy_obj,
                      cutoff=0.5, 
                      species='human',
                      gene_id='ensembl') 
```
- **scanpy_obj**: a scanpy object must be supplied to classify, no default
- **cutoff**: the value used to threchold the likelihoods, default is 0.5
- **assay**: which seurat_obj assay to use for classification, helpful if data is prenormalized, default is 'SCT'
- **species**: from which species did the samples originate, either 'human' or 'mouse', defaults to 'human'
- **gene_id**: what type of gene ID is used, either 'ensembl' or 'symbol', defaults to 'ensembl'

### Cell cycle classification results

The results of the cell cycle classification ares stored in the first element of the 'ccAFv2.predict_labels' output, and the likelihoods are stored in the second element.

```python
PCW8_labels
```

Which returns the following:

```python
(array(['G1', 'S', 'Neural G0', ..., 'Late G1', 'Neural G0', 'S'],
      dtype='<U10'), array([[9.96540964e-01, 2.77950567e-05, 1.62392517e-03, ...,
        1.12998277e-04, 1.34928769e-03, 3.37415549e-04],
       [2.38446728e-03, 9.58865421e-05, 4.40378720e-03, ...,
        1.25416279e-01, 7.62154996e-01, 1.05463535e-01],
       [3.09040988e-05, 1.47282879e-06, 3.99237297e-06, ...,
        9.99962687e-01, 1.65011215e-07, 8.85220061e-07],
       ...,
       [2.72926106e-03, 3.59202386e-03, 9.85045612e-01, ...,
        8.02930258e-03, 1.00778125e-04, 4.46247839e-04],
       [1.43443659e-01, 1.61317177e-03, 2.99169007e-03, ...,
        8.51489604e-01, 1.09878434e-04, 3.27764486e-04],
       [7.05660739e-07, 1.27422639e-09, 1.13804369e-07, ...,
        1.86515393e-07, 9.99996066e-01, 2.80967629e-06]], dtype=float32))
```

In the code Below we demonstrate how the classifications can be added to the metadata. After adding the column to the .obs metadata, the classification for each cell would then found in the column 'ccAFv2', and is a categorical variable which helps with plotting.

```python
# Save into scanpy object
PCW8.obs['ccAFv2'] = pd.Categorical(PCW8_labels[0], categories=['Neural G0', 'G1', 'Late G1', 'S', 'S/G2', 'G2/M', 'M/Early G1', 'Unknown'], ordered=True)
```

### Plotting cell cycle states

We provide plotting functions that colorize the cell cycle states in the way used in our manuscripts. We strongly suggest using these functions when plotting if possible.

#### Plotting a UMAP with cell cycle states

Plotting cells using ther first two dimensions from a dimensionality reduction method (e.g., PCA, tSNE, or UMAP) is a common way to represent single cell or nuclei RNA-seq data. Below we provide code to plot the cells colorized based on their called cell cycle state.

```r
# Run UMAP of U5 hNSCs
sc.pp.highly_variable_genes(PCW8, n_top_genes=2000)
sc.tl.pca(PCW8)
sc.pp.neighbors(PCW8)
sc.tl.umap(PCW8)

# Prepare a color mapping dictionary
cmap1 = {"Neural G0": "#d9a428", "G1": "#f37f73", "Late G1": "#1fb1a9",  "S": "#8571b2", "S/G2": "#db7092", "G2/M": "#3db270" ,"M/Early G1": "#6d90ca",  "Unknown": "#d3d3d3"}

# Plot UMAP of U5 hNSCs
sc.pl.umap(PCW8, color=['ccAFv2'], palette=cmap1, save='ccAFv2_UMAP_PCW8.pdf')
```

In the figures folder you will find the PDF 'umapccAFv2_UMAP_PCW8.pdf'. Below is the UMAP for the hNSCs from a human fetus 8 weeks post-conception colorized using the cell cycle states. The expected flow of the cell cycle states can be seen in the UMAP.

![UMAP DimPlot colorized with ccAFv2 cell cycle states](https://github.com/plaisier-lab/ccAFv2_py/blob/main/figs/ccAFv2_UMAP_PCW8.png?raw=true)

## Maintainers

For issues or comments please contact:  [Chris Plaisier](mailto:plaisier@asu.edu)

And for other great packages from the Plaisier Lab please check here:  [@plaisier-lab](https://github.com/plaisier-lab).

## Contributing

Feel free to dive in! [Open an issue](https://github.com/plaisier-lab/ccAFv2_R/issues/new) or submit PRs.

## Citation

1. **Citation for ccAFv2 (version 2)**:

> *Citation for ccAFv2 coming soon!*

2. **Citation for ccAF (version 1)**:

[Neural G0: a quiescent-like state found in neuroepithelial-derived cells and glioma.](https://doi.org/10.1101/446344) Samantha A. O'Connor, Heather M. Feldman, Chad M. Toledo, Sonali Arora, Pia Hoellerbauer, Philip Corrin, Lucas Carter, Megan Kufeld, Hamid Bolouri, Ryan Basom, Jeffrey Delrow, Jose L. McFaline-Figueroa, Cole Trapnell, Steven M. Pollard, Anoop Patel, Patrick J. Paddison, Christopher L. Plaisier. bioRxiv 446344; doi: [https://doi.org/10.1101/446344](https://doi.org/10.1101/446344)
