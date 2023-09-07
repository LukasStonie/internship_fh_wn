import numpy as np
import pandas as pd
from werkzeug.datastructures import FileStorage

from app.external_libs.raman_lib.opus_converter import convert_opus
import tempfile


def spectrum_to_df(file: FileStorage) -> pd.DataFrame:
    with tempfile.NamedTemporaryFile() as temp:
        print(temp.name)
        print(file.filename)
        file.save(temp.name)
        if file.filename.lower().endswith(".csv") or \
                file.filename.lower().endswith(".dpt"):
            spectrum = np.loadtxt(temp, delimiter=",")
        elif file.filename.lower().endswith(".tsv"):
            spectrum = np.loadtxt(temp, delimiter="\t")
        elif file.filename.lower().endswith(".txt"):
            spectrum = np.loadtxt(temp, delimiter=",")
        else:
            try:
                spectrum = convert_opus(temp)
            except:
                print(f"File {file} does not match any inplemented file format. Skipping...")
                spectrum = None

        spectrum = np.asarray(spectrum, dtype=float)
    return pd.DataFrame(spectrum[:, :], columns=spectrum[0, :])
