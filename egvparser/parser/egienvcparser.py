#!/usr/bin/env python
__version__ = '0.1'
__author__ = 'Jaganadh Gopinadhan'
__contact__ = "https://www.linkedin.com/in/jaganadhg/"

import scipy.io as sio


def egienvec_parser(data_path : str,dkey : str = "LAMDATA") -> dict:
    """ Parse the eigenvector LAM Etch Data and return the vaues as dictionary
        Source of Data https://www.eigenvector.com/data/Etch/
        The data is in a Matlab struct file. Varibles in the files are
        INFORMATION: [ 29x63 char]  
        calibration: {108x1  cell}  The normal or calibration wafers
        calib_names: [108x9  char]  Names of the calibration wafers
        test: { 21x1  cell}  The test or faulty wafers
        test_names: [ 21x9  char]  Names of the test wafers
        fault_names: [ 21x9  char]  Names of the specific faults
        variables: [ 21x14 char]  Names of the variables
        :param data_apth: Path to individual .mat file
        :param dkey: Key for the data LAMDATA for MACHINE_Data.mat,
         OESDATA for OES_DATA.mat and RFMDATA for RFM_DATA.mat
        :returns data_dict: A dictonery encding the data ready for use in Python
    """

    data_dict = dict()
    var_names = ['information','calibration','calib_names','test','test_names',
    'fault_names','variables']
    base_data = sio.loadmat(data_path)

    try:
        lam_data = base_data[dkey]
        for idx, var_name in enumerate(var_names):
            data_dict[var_name] = lam_data[0,0][idx]
    except KeyError:
        print(f"The specified key {dkey} not found in the data!")

    return data_dict



if __name__ == "__main__":
    machine = egienvec_parser("RFM_DATA.mat", dkey="RFMDATA")
    print(machine['variables'])