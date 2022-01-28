#!/usr/bin/env python
__version__ = '0.1'
__author__ = 'Jaganadh Gopinadhan'
__contact__ = "https://www.linkedin.com/in/jaganadhg/"

import scipy.io as sio
import numpy as np 
import pandas as pd


def ndarry_todf(sensor_data : np.ndarray, colnames : list) -> pd.DataFrame:
    """ Convert a nympy nd array to a Pandas DataFrame
        :params sensor_data: numpy ndarray data with sensor data
        :params colnames: column names
        :returns sensor_frame: converted pandas dataframe
    """
    sensor_frame = None 

    try:
        sensor_frame = pd.DataFrame(sensor_data,
                                    columns=colnames)
    except:
        print("The data is not in numpy.ndarray format")

    return sensor_frame


def data_to_df(calibration : np.ndarray,
                        calib_names : np.ndarray,
                        colnames : list,
                        fault_names : np.ndarray = None) -> pd.DataFrame:
    """ Create a pandas DataFrame from the calibration data
        :params calibration: All calib_names sensor data as numpy.ndarray
        :params calib_names: calibration wafer names as np.array
        :params colnames: column names
        :returns calib_frame: a pandas DataFrame with clibration data
    """

    calib_frame = None 
    calib_frame_list = list()
    
    calib_data_range = list(range(0,calibration.shape[0]))

    for idx in calib_data_range:
        byte_adjusted_data = np.array(calibration[idx,:][0]).byteswap().newbyteorder()
        """
        To overcome 
        ValueError: Big-endian buffer not supported on little-endian compiler 
        pandas error
        """
        curr_df = pd.DataFrame(byte_adjusted_data,
                                columns = colnames)
        curr_df['wafer_names'] = calib_names[idx]

        if fault_names is not None:
            curr_df['fault_name'] = fault_names[idx]

        calib_frame_list.append(curr_df)

    try:
        calib_frame = pd.concat(calib_frame_list)
    except:
        print("Error in stacking the DataFrames")

    return calib_frame


def egienvec_parser(data_path : str,dkey : str = "LAMDATA") -> dict:
    """ Parse the eigenvector LAM Etch Data and return the vaues as dictionary
        Source of Data https://www.eigenvector.com/data/Etch/
        The data is in a Matlab struct file. Varibles in the files are
        INFORMATION: [ 29x63 char]  - 0 
        calibration: {108x1  cell}  The normal or calibration wafers - 1
        calib_names: [108x9  char]  Names of the calibration wafers - 2
        test: { 21x1  cell}  The test or faulty wafers - 3
        test_names: [ 21x9  char]  Names of the test wafers - 4
        fault_names: [ 21x9  char]  Names of the specific faults - 5
        variables: [ 21x14 char]  Names of the variables -6 
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