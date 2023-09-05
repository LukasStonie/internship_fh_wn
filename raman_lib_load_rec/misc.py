import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from opus_converter import convert_opus


def str_subtract(a, b):
    #subtract the string b from a starting from the left
    return a.replace(b, "", 1)

def mode(x):
    values, counts = np.unique(x, return_counts=True)
    i = counts.argmax()
    return values[i]


def load_data_rec(dir, path, data, labels, files):
    if path.lower().endswith(".csv") or \
            path.lower().endswith(".txt") or \
            path.lower().endswith(".tsv"):
        data = pd.read_csv(path)
    elif all([os.path.isfile(os.path.join(path, x)) for x in os.listdir(path)]):
        for file in os.listdir(path):
            filepath = os.path.join(path, file)
            # data, labels, files = load_data_rec(filepath)

            if filepath.lower().endswith(".csv"):
                spectrum = np.loadtxt(filepath, delimiter=",")
            elif filepath.lower().endswith(".tsv"):
                spectrum = np.loadtxt(filepath, delimiter="\t")
            elif filepath.lower().endswith(".txt"):
                spectrum = np.loadtxt(filepath, delimiter=",")
            else:
                try:
                    spectrum = convert_opus(filepath)
                except:
                    print(f"File {file} does not match any implemented file format. Skipping...")
                    continue


            filename = str_subtract(filepath, dir)
            label_list = str.split(str.lstrip(filename, "/"), "/")
            data.append(spectrum)
            files.append(filename)
            for i, label in enumerate(label_list[:-1]):
                if not len(labels)>i:
                    labels.append([])
                labels[i].append(label_list[i])

    elif all([os.path.isdir(os.path.join(path, x)) for x in os.listdir(path)]):
        for path_inner in os.listdir(path):
            #for file in os.listdir(os.path.join(path, path_inner)):
                filepath = os.path.join(path, path_inner)
                data, labels, files = load_data_rec(dir, filepath, data, labels, files)



    else:
        print("Received unclear directory structure.")
        return None, None, None
    return data, labels, files


def load_data(path):
    data = []
    labels = []
    files = []
    data, labels, files = load_data_rec(path, path, data, labels, files)
    try:
        data = np.asarray(data, dtype=float)
    except ValueError:
        print("Data could not be combined into a single array. Perhaps some spectra cover different wave-number ranges?")
        return None, None, None
    data = pd.DataFrame(data[:, :, 1], columns=data[0, :, 0])
    for i, label in enumerate(labels):
        data.insert(0, "label_"+str(i), label)
    if files:
        data.insert(len(labels), "file", files)

    #X = data.drop(columns=[, "file"])
    lose_labels = [x for x in data.columns if str(x).startswith("label_")]
    lose_labels.append("file")
    X = data.drop(columns=lose_labels)

    wns = np.asarray(X.columns.astype(float))
    X = np.asarray(X)

    y = np.asarray(data.label_0)
    y, y_key = pd.factorize(y, sort=True)

    for i, label in enumerate(y_key):
        print(f"{label}: {i}")

    for i in range(len(y_key)):
        plt.plot(wns, X[y == i].mean(axis=0), label=y_key[i])
    plt.margins(x=0)
    plt.legend()

    plt.xticks(range(500, 1801, 100))

    plt.grid()
    plt.xlabel("Wavenumber ($cm^{-1}$)")
    plt.ylabel("Intensity (-)")
    plt.show()
    return data
