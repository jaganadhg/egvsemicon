
[![licence](https://img.shields.io/badge/licence-Apache-blue.svg?style=flat)](https://github.com/jaganadhg/egvsemicon/blob/main/LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5919197.svg)](https://zenodo.org/record/5919197#.YfXMGLpKjg5)

# Eigenvector Metal Etch Data Parser - Python

The Eigenvector Etch Data Parser is developed to read Matlab data files published by Eigenvector[1]. The data is from a LAM 9600 Metal Etching Machine and was collected in 1995's. The data is available as three individual .mat files MACHINE_Data.mat, OES_DATA.mat, and RFM_DATA.mat. The parser reads each file and converts the calibration data (sensor data) and test data (sensor data) into a single DataFrame. The parser introduced an additional field in the data 'fault_name', which helps the user identify the normal/calibration wafers and test wafers(with defects). We tested the parser in Python3 environments only; if you are looking for Python2 compatibility, please test and create a bug/pull request as applicable. The source code is released under Apache 2.0 license and is available at https://github.com/jaganadhg/egvsemicon.

A detailed note on the data and usage of the parser is available at https://github.com/jaganadhg/egvsemicon/blob/main/EGV_Data_exploreer.ipynb. 

[1] https://eigenvector.com/resources/data-sets/ 
[2] https://github.com/jaganadhg/egvsemicon/blob/main/EGV_Data_exploreer.ipynb 

# Cite as
[1]Jaganadh Gopinadhan, “Eigenvector Metal Etch Data Parser - Python”. Zenodo, Jan. 29, 2022. doi: 10.5281/zenodo.5919197.
