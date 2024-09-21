from _dbcv_float32np import _dbcv_32np
from _dbcv_float64np import _dbcv_64np
from _dbcv_float32p import _dbcv_32p
from _dbcv_float64p import _dbcv_64p

import numba
import numpy as np
import os

from utils import cahce_warming

class NumberOfClustersError(Exception):
    pass

class WrongDataTypeError(Exception):
    pass 

class WrongInputDataError(Exception):
    pass

def DBCV(X, labels, noise_id = -1, strict: bool = False, parallel: bool = True):
    """Computes DBCV

    This function does not compute or store the distance matrix in memory 
    using a lazy-computation approach and is optimized 
    using parallel computation and numba  

    Parameters
    ----------
    X : 
        nd.array float32 or float64 if strict == True
        or 
        nd.array convertible to float if strict == False 
        shape (N, D)
        Sample embeddings

    labels: 
        nd.array int32 if strict == True
        or 
        nd.array convertible to int if strict == False
        shape (N,)
        Cluster IDs assigned for each sample in X

    noise_id: default = -1
        int 
        or 
        iterable of int-s
        id or id-s of noise clusters
    
    strict: default = Flase
        bool
        If True the function will check the input data 
        against the data types used in the decorated numba function 
        (It does not support overloading), if False the function will 
        automatically convert the input data

    parallel: default = True
        bool 
        If True parallel calculations are used 

    """
    if not isinstance(X, np.ndarray) or not isinstance(labels, np.ndarray):
        raise WrongInputDataError("Input data must be in np.ndarray format")

    if X.shape[0] != labels.shape[0]:
        raise WrongInputDataError("X and labels must have the same length")

    if X.ndim != 2 or labels.ndim != 1:
        raise WrongInputDataError(f"X and labels must have 2 and 1 numbers of dimensions respectively\nbut were received {X.ndim} and {labels.ndim}")

    if strict:
        if not (X.dtype == np.float64 or X.dtype == np.float32) or not labels.dtype == np.int32:
            raise WrongDataTypeError(f"Input data must have dtype float64 or float32 for X and int32\nfor labels but were received {X.dtype} and {labels.dtype} respectively")
    else:
        if X.dtype != np.float64 and X.dtype != np.float32:
            X = X.copy().astype(np.float64)
        if labels.dtype != np.int32:
            labels = labels.copy().astype(np.int32)

    if not hasattr(noise_id, '__iter__') and not isinstance(noise_id, int):
        raise WrongInputDataError("noise_id must be int or iterable")
    elif hasattr(noise_id, '__iter__'):
        noise_id = list(noise_id)
    else:
        noise_id = [noise_id]

    n = X.shape[0]
    un_labels, counts = np.unique(labels, return_counts=True)
    mask_for_un_labels = ~((counts == 1) + np.isin(un_labels, noise_id))

    if np.sum(mask_for_un_labels) in {0, 1}:
        return 0 

    mask_for_labels_and_X = np.isin(labels, un_labels[mask_for_un_labels])

    if X.ndim == 1:
        X = X.reshape(-1, 1) 

    if X.dtype == np.float64 and parallel:
        return _dbcv_64p(X[mask_for_labels_and_X], labels[mask_for_labels_and_X], 
                        un_labels[mask_for_un_labels].astype(np.int32), counts[mask_for_un_labels].astype(np.int32)) / n
    elif X.dtype == np.float64:
        return _dbcv_64np(X[mask_for_labels_and_X], labels[mask_for_labels_and_X], 
                        un_labels[mask_for_un_labels].astype(np.int32), counts[mask_for_un_labels].astype(np.int32)) / n

    if X.dtype == np.float32 and parallel:
        return _dbcv_32p(X[mask_for_labels_and_X], labels[mask_for_labels_and_X], 
                        un_labels[mask_for_un_labels].astype(np.int32), counts[mask_for_un_labels].astype(np.int32)) / n
    elif X.dtype == np.float32:
        return _dbcv_32np(X[mask_for_labels_and_X], labels[mask_for_labels_and_X], 
                        un_labels[mask_for_un_labels].astype(np.int32), counts[mask_for_un_labels].astype(np.int32)) / n


def set_number_of_threads(num_of_threads: int, cahce_warm: bool = True):
    """Allows to control the number of threads used

    NOTE: numba may take additional time to compile the 
    function the first time it is called after changing 
    this parameter, in order to prevent this cahce_warm
    param is used

    Parameters
    ----------
    num_of_threads:
        int
        1 < num_of_threads <= maximum available number of threads 

    cahce_warm: default = True
        bool
        If True, immediately after changing the number of threads 
        numba functions will be recompiled, if necessary  

    """
    if not isinstance(num_of_threads, int):
        raise WrongInputDataError("num_of_threads msut be int")

    cpus_max = os.cpu_count()
    if num_of_threads > cpus_max:
        raise WrongInputDataError("num_of_threads is bigger than available number of threads")
    
    if num_of_threads == 1:
        raise WrongInputDataError("num_of_threads cannot be equal to 1")


    numba.config.NUMBA_NUM_THREADS = num_of_threads

    if cahce_warm:
        cahce_warming()


