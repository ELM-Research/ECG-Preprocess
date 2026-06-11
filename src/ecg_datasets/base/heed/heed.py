import pandas as pd
from glob import glob

from ecg_datasets.base.base_dataset import BaseDataset
from configs.constants import DATA_DIR

class HEED(BaseDataset):
    def __init__(self, args, logger):
        super().__init__(args, logger)
        self.heed_dir = f"{DATA_DIR}/HEED"
        dictionary = pd.concat([pd.read_csv(p) for p in glob(f"{self.heed_dir}/*/12SL_diagnoses/diagnoses_dictionary.csv")])
        self.code2dx = dict(zip(dictionary["codes"].astype(str), dictionary["diagnoses"]))

    def prepare_df(self,):
        paths = sorted(glob(f"{self.heed_dir}/*/12SL_diagnoses/diagnoses_acquisition.csv"))
        df = pd.concat([pd.read_csv(p)[["FileName", "codes_physician", "codes_software"]].assign(inst=p.split("/")[-3]) for p in paths])
        df.to_csv(f"{DATA_DIR}/{self.args.base}/{self.args.base}.csv", index=False)

    def map_codes(self, codes):
        return list(dict.fromkeys(self.code2dx[c] for c in str(codes).split(",") if c in self.code2dx))

    def open_ecg(self, row,):
        file_path = f"{self.heed_dir}/{row['inst']}/WFDB{row['FileName']}"
        ecg, sf = self.open_wfdb(file_path)
        return {"file_path": file_path, "ecg": ecg, "sf": sf,
                "file_name": "_".join([row["inst"], *row["FileName"].strip("/").split("/")]),
                "report": self.map_codes(row["codes_physician"]),
                "muse_report": self.map_codes(row["codes_software"])}
