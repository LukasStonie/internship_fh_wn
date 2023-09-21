import numpy as np
import pandas as pd
from werkzeug.datastructures import FileStorage

from app.external_libs.raman_lib.opus_converter import convert_opus
import tempfile

from app.external_libs.raman_lib.preprocessing import PeakPicker


def spectrum_to_df(file: FileStorage) -> pd.DataFrame:
    """
        Reads the contents of a file and returns the spectral data. Based on the type of the file, the function uses different methods to read the file. CSV, DPT, TSV and TXT files are read using numpy.loadtxt. OPUS files are read using the convert_opus function from app.external_libs.raman_lib.opus_converter

    Args:
        file (FileStorage): uploaded file

    Returns:
        pd.DataFrame: ready to use spectral data with wavenumbers as index and intensities as values
    """

    with tempfile.NamedTemporaryFile() as temp:
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

