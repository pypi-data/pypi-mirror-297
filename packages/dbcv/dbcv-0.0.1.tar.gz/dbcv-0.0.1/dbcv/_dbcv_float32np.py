from numba import float32, float64, int32, int64, njit, prange
import numpy as np
from numba.typed import Dict


@njit((float32[:,:], ), cache=True)
def calculate_core_dist_32np(data):
    n, d = data.shape
    core_dist = np.zeros(n, dtype=np.float64)

    for i in range(n):
        dist = np.sum((data - data[i]) ** 2, axis=1)
        dist[i] = np.inf
        dist = dist ** -(d + 0.0)
        core_dist[i] = np.sum(dist) / (n - 1)

    return core_dist ** -(1.0 / d)


@njit((float32[:, :], float64[:],), cache=True)
def _prim_mst_32np(observations, core_dist):
    n = observations.shape[0]
    in_tree = np.zeros(n, dtype=np.bool_)
    min_weight = np.full(n, np.inf, np.float64)
    previous = np.full(n, -1, dtype=np.int32)
    start_vertex = 0
    min_weight[start_vertex] = 0
    for _ in range(n):
        u = np.argmin(np.where(in_tree, np.inf, min_weight))
        in_tree[u] = True

        not_in_tree = np.flatnonzero(~in_tree)

        distances = np.sum((observations[not_in_tree] - observations[u]) ** 2, axis=1)
        distances = np.maximum(distances, core_dist[not_in_tree])
        distances = np.maximum(distances, core_dist[u])
        
        
        mask = distances < min_weight[not_in_tree]
        previous[not_in_tree[mask]] = u 
        min_weight[not_in_tree[mask]] = distances[mask]



    return np.arange(1, n, dtype=np.int32), previous[1:]


@njit((float32[:, :], float32[:, :], float64[:], float64[:]), cache=True)
def dens_sep_32np(data_i, data_j, inter_core_dists_i, inter_core_dists_j):
    if not data_i.size or not data_j.size:
        return np.inf

    min_values = np.full(data_i.shape[0], np.inf, dtype=np.float64)
    for i in range(data_i.shape[0]):
        l = np.sum((data_i[i] - data_j) ** 2, axis=1)
        l = np.maximum(l, inter_core_dists_j)
        l = np.maximum(l, inter_core_dists_i[i])
        min_values[i] = np.min(l)

    return np.min(min_values)


@njit((float32[:, :], int32[:], int32[:], int32[:]), cache=True)
def _dbcv_32np(X, labels, uniqal, counts_for_uniq):

    dsbcs = np.zeros(uniqal.size, dtype=np.float64)

    internal_obj = Dict.empty(key_type=int32, value_type=int64[:])
    internal_core_dist = Dict.empty(key_type=int32, value_type=float64[:])


    min_dspcs = np.full((uniqal.size - 1, uniqal.size), np.inf, dtype=np.float64)

    for i in range(uniqal.size):
        index = np.flatnonzero(labels == uniqal[i]).astype(np.int64)
        
        core_dists = calculate_core_dist_32np(X[index])
        row, col = _prim_mst_32np(X[index], core_dists)
        columns = np.flatnonzero(np.bincount(np.hstack((row, col))) > 1)
        columns_set = set(columns)
        val = np.zeros(row.size, dtype=np.float64)
        for j in range(row.size):
            if row[j] in columns_set and col[j] in columns_set:
                val[j] = np.maximum(np.sum((X[index[row[j]]] - X[index[col[j]]]) ** 2), np.maximum(core_dists[col[j]], core_dists[row[j]]))
   
        dsbcs[i] = np.max(val)
        internal_obj[i] = index[columns]
        internal_core_dist[i] = core_dists[columns]

    for i in range(uniqal.size):
        for j in range(i + 1, uniqal.size):
            index_i = internal_obj[i]
            index_j = internal_obj[j]
            core_dists_i = internal_core_dist[i]
            core_dists_j = internal_core_dist[j]

            dspc_ij = dens_sep_32np(X[index_i], X[index_j], core_dists_i, core_dists_j)

            min_dspcs[j - 1][i] = dspc_ij
            min_dspcs[i][j] = dspc_ij

    min_dspcs = np.array([min(el) for el in min_dspcs.T], dtype=np.float64)
    np.nan_to_num(min_dspcs, copy=False)
    vcs = (min_dspcs - dsbcs) / (1e-12 + np.maximum(min_dspcs, dsbcs))
    np.nan_to_num(vcs, copy=False, nan=0.0)
    return np.sum(vcs * counts_for_uniq)

