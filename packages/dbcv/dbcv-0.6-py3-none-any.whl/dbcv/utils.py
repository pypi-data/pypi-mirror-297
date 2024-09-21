def get_cache_warming_data():
    current_file_path = pathlib.Path(__file__).resolve()
    datasets_path = current_file_path.parent.parent / 'Test_datasets'
    path = datasets_path / 'Cache_warming.npy'
    data = np.load(path)
    X_float64 = data[:, :2]
    X_float32 = X_float64.copy().astype(np.float32)
    Y = data[:, 2].astype(np.int32)
    return X_float64, X_float32, Y


def cahce_warming():
    X_float64, X_float32, Y = get_cache_warming_data()
    DBCV(X_float64, Y, strict=True, parallel=True)
    DBCV(X_float64, Y, strict=True, parallel=False)
    DBCV(X_float32, Y, strict=True, parallel=True)
    DBCV(X_float32, Y, strict=True, parallel=False)