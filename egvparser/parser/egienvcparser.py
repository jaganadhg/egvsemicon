#!/usr/bin/env python
__version__ = '0.1'
__author__ = 'Jaganadh Gopinadhan'
__contact__ = "https://www.linkedin.com/in/jaganadhg/"

import pandas as pd
import numpy as np
import scipy.io as sio
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s :: %(levelname)s :: %(message)s')


def raw_data_to_df(calibration: np.ndarray,
                   calib_names: np.ndarray,
                   colnames: list,
                   fault_names: np.ndarray = None) -> pd.DataFrame:
    """ Create a pandas DataFrame from the calibration data
        :params calibration: All calib_names sensor data as numpy.ndarray
        :params calib_names: calibration wafer names as np.array
        :params colnames: column names
        :returns calib_frame: a pandas DataFrame with clibration data
    """

    calib_frame = None
    calib_frame_list = list()

    try:
        colnames = [cname.strip() for cname in colnames]
    except:
        #If the Data OES colanumn names are Prak of Wavelength
        colnames = colnames[0].tolist()

    calib_data_range = list(range(0, calibration.shape[0]))

    for idx in calib_data_range:
        byte_adjusted_data = np.array(
            calibration[idx, :][0]).byteswap().newbyteorder()
        """
        To overcome
        ValueError: Big-endian buffer not supported on little-endian compiler
        pandas error
        """
        curr_df = pd.DataFrame(byte_adjusted_data,
                               columns=colnames)
        curr_df['wafer_names'] = calib_names[idx]

        if fault_names is not None:
            curr_df['fault_name'] = fault_names[idx]
        else:
            curr_df['fault_name'] = "calibration"

        calib_frame_list.append(curr_df)

    try:
        calib_frame = pd.concat(calib_frame_list)
    except BaseException:
        logging.error("Error in stacking the DataFrames")

    return calib_frame


def egienvec_parser(data_path: str, dkey: str = "LAMDATA") -> pd.DataFrame:
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
        :returns data_set: a pandas DataFrame contaning both calibration and test data

    """
    data_set = None
    data_dict = dict()
    var_names = ['information', 'calibration', 'calib_names', 'test', 'test_names',
                 'fault_names', 'variables']

    base_data = sio.loadmat(data_path)


    logging.info(f"Keys in the data are {base_data.keys()}")

    try:
        lam_data = base_data[dkey]

        for idx, var_name in enumerate(var_names):
            data_dict[var_name] = lam_data[0, 0][idx]
    except KeyError:
        logging.error(f"The specified key {dkey} not found in the data!")

    sensor_names = list(data_dict['variables'])
    logging.info(f"The sensor names are {sensor_names}")

    logging.info(f"Processing calibration data for {dkey}")

    calibration_data = raw_data_to_df(data_dict['calibration'],
                                      data_dict['calib_names'],
                                      sensor_names)
    logging.info(f"Processed calibration data for {dkey}")

    logging.info(f"Processing test data for {dkey}")
    test_data = raw_data_to_df(data_dict['test'],
                               data_dict['test_names'],
                               sensor_names,
                               data_dict['fault_names'])
    logging.info(f"Processed test data for {dkey}")

    try:
        data_set = pd.concat([calibration_data,
                              test_data])
        logging.info(
            f"Total sensor values in the data {dkey} is {data_set.shape[0]}")
    except BaseException:
        logging.error("May be empty data in the DataFrames!")

    return data_set


if __name__ == "__main__":
    matlab_data = "/home/jaganadhg/AI_RND/Semiconductor/eigenvector/MACHINE_Data.mat"
    machine = egienvec_parser(matlab_data,
                              dkey="LAMDATA")
    print(machine.head())
