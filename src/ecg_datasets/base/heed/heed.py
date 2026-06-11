import pandas as pd

from ecg_datasets.base.base_dataset import BaseDataset
from configs.constants import DATA_DIR

class HEED(BaseDataset):
    def __init__(self, args, logger):
        super().__init__(args, logger)

    def prepare_df(self,):
        diagnoses_acquisition = pd.read_csv(f"{DATA_DIR}/HEED/I0001/12SL_diagnoses/diagnoses_acquisition.csv")
        print(len(diagnoses_acquisition))
        print(diagnoses_acquisition.head())
        print(diagnoses_acquisition.columns)
        print(diagnoses_acquisition["FileName"])
        print(diagnoses_acquisition["codes_physician"])
        print(diagnoses_acquisition["codes_software"])
        diagnoses_dic = pd.read_csv(f"{DATA_DIR}/HEED/I0001/12SL_diagnoses/diagnoses_dictionary.csv")
        print(len(diagnoses_dic))
        print(diagnoses_dic.head())
        print(diagnoses_dic.columns)
        input("hihi")
        pass

    def open_ecg(self, row):
        pass