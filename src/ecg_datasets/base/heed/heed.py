import pandas as pd

from ecg_datasets.base.base_dataset import BaseDataset
from configs.constants import DATA_DIR

class HEED(BaseDataset):
    def __init__(self, args, logger):
        super().__init__(args, logger)
        self.diag_dir = f"{DATA_DIR}/HEED/I0001/12SL_diagnoses"
        diagnoses_dic = pd.read_csv(f"{self.diag_dir}/diagnoses_dictionary.csv")
        self.code_to_diagnosis = dict(zip(diagnoses_dic["codes"], diagnoses_dic["diagnoses"]))

    def prepare_df(self,):
        cols = ["FileName", "codes_physician", "codes_software"]
        df = pd.read_csv(f"{self.diag_dir}/diagnoses_acquisition.csv").dropna(subset=cols)[cols]
        df.to_csv(f"{DATA_DIR}/{self.args.base}/{self.args.base}.csv", index=False)

    def map_codes(self, codes):
        return [self.code_to_diagnosis[int(c)] for c in codes.split(",") if int(c) in self.code_to_diagnosis]

    def open_ecg(self, row,):
        file_path = f"{DATA_DIR}/HEED{row['FileName']}"
        ecg, sf = self.open_wfdb(file_path)
        return {"file_path": file_path, "ecg" : ecg,
                "sf" : sf, "file_name" : "_".join(row["FileName"].strip("/").split("/")),
                "report": self.map_codes(row["codes_physician"]),
                "muse_report": self.map_codes(row["codes_software"])}
