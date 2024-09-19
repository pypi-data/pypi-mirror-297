##########################################################
## OncoMerge:  ccAFv2.py                                ##
##  ______     ______     __  __                        ##
## /\  __ \   /\  ___\   /\ \/\ \                       ##
## \ \  __ \  \ \___  \  \ \ \_\ \                      ##
##  \ \_\ \_\  \/\_____\  \ \_____\                     ##
##   \/_/\/_/   \/_____/   \/_____/                     ##
## @Developed by: Plaisier Lab                          ##
##   (https://plaisierlab.engineering.asu.edu/)         ##
##   Arizona State University                           ##
##   242 ISTB1, 550 E Orange St                         ##
##   Tempe, AZ  85281                                   ##
## @Author:  Chris Plaisier, Samantha O'Connor          ##
## @License:  GNU GPLv3                                 ##
##                                                      ##
## If this program is used in your analysis please      ##
## mention who built it. Thanks. :-)                    ##
##########################################################

##########################################
## Load Python packages for classifiers ##
##########################################

# General
from importlib.resources import path
import numpy as np
import pandas as pd
import os
from scipy.sparse import isspmatrix
import scanpy as sc
sc.settings.verbosity = 0
from sklearn.preprocessing import StandardScaler

# Stop warning messages for cudart
import logging
logging.disable(logging.WARNING)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = "3"
logging.getLogger('tensorflow').disabled = True

# Neural network
import tensorflow as tf
from tensorflow import keras


################
## Load model ##
################
with path('ccAFv2', 'ccAFv2_model.h5') as inPath:
    _classifier = keras.models.load_model(inPath)
with path('ccAFv2', 'ccAFv2_genes.csv') as inPath:
    _genes_all = pd.read_csv(inPath, index_col=0, header=0)
with path('ccAFv2', 'ccAFv2_classes.txt') as inPath:
    _classes = list(pd.read_csv(inPath, header=None)[0])


###############
## Functions ##
###############

# Scale data for classification
def _scale(data):
    """
    Standardize or normalize numeric data using scikit-learn's StandardScaler.

    Parameters:
    - data: 2D NumPy array or list of lists

    Returns:
    - Scaled data (NumPy array)
    """
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    return scaled_data

# Prepare test data for predicting
def _prep_predict_data(data, genes):
    """
    prep_predict_data takes in a pandas dataframe and the trained ccAFv2 model.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame of scRNA-seq data to be classified.
    model : keras.models.sequential
        Trained ccAFv2 sequential keras model.

    Returns
    -------
    pd.Series
        Series of labels for each single cell.

    """
    print('    Preparing data for classification...')
    # Remove all genes with zero counts
    data.var_names_make_unique()
    sc.pp.filter_genes(data, min_cells=1)
    # Restrict to classifier genes
    in_both = list(set(genes).intersection(data.var_names))
    if(len(in_both)>0):
        print('    Marker genes present in this dataset: '+str(len(in_both)))
        print('    Missing marker genes in this dataset: '+str(len(set(genes))-len(in_both)))
        data2 = data[:,in_both]
        # Scale data
        if isspmatrix(data.X):
            data2 = pd.DataFrame(data2.X.todense(), index = data2.obs_names, columns = data2.var_names)
        else:
            data2 = pd.DataFrame(data2.X, index = data2.obs_names, columns = data2.var_names)
        data3 = pd.DataFrame(_scale(data2), index = data2.index, columns = data2.columns)
        # Add minimum values for missing genes
        missing = set(genes).difference(data3.columns)
        if len(missing)>0:
            data4 = pd.concat([data3, pd.DataFrame(data3.values.min(), index=data3.index, columns = missing)], axis=1)
            return data4[list(genes)]
        else:
            return data3
    else:
        raise RuntimeError('Check species and gene_id, because there is no overlap between input genes and classifier genes!')

# Predict labels with rejection
def predict_labels(new_data, species='human', gene_id='ensembl', cutoff=0.5, classifier=_classifier, genes_all=_genes_all, classes=_classes):
    """
    predict_new_data takes in a pandas dataframe and the trained ccAFv2 model.

    Parameters
    ----------
    new_data : annData object
         New scRNA-seq dataset to be classified.
    species: string
         Species of the cells to be classified, currently supports 'human' and 'mouse'.
    gene_id: string
         Gene IDs for the scRNA-seq dataset, currently supports 'ensembl' and 'symbol'.
    cutoff : float
        The cutoff for likelihoods from the neural network classifier model.

    Returns
    -------
    pd.Series
        Series of labels for each single cell.

    """
    print('Running ccAFv2:')
    genes = genes_all[species+'_'+gene_id]
    pred_data = _prep_predict_data(new_data, genes)
    probabilities = _predict_new_data(pred_data, classifier)
    print('  Choosing cell cycle state...')
    labels = np.array([classes[np.argmax(i)] for i in probabilities])
    labels[np.where([np.max(i) < cutoff for i in probabilities])] = 'Unknown'
    print('Done.')
    return labels, probabilities

# Predict ccAFv2 labels for new data
def _predict_new_data(new_data, classifier):
    """
    predict_new_data takes in a pandas dataframe and the trained ccAFv2 model.

    Parameters
    ----------
    new_data : pd.DataFrame
        DataFrame of scRNA-seq data to be classified.
    model : keras.models.sequential
        Trained ccAFv2 sequential keras model.

    Returns
    -------
    pd.Series
        Series of labels for each single cell.

    """
    print('  Predicting cell cycle state probabilities...')
    return classifier.predict(new_data)

