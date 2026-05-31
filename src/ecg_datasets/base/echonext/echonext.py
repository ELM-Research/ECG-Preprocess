import numpy as np
import pandas as pd

from ecg_datasets.base.base_dataset import BaseDataset
from configs.constants import DATA_DIR, PTB_ORDER

class EchoNext(BaseDataset):
    def __init__(self, args, logger):
        super().__init__(args, logger)

    def prepare_df(self,):
        self.logger.info("Preparing DF")
        root_dir_name = f"{DATA_DIR}/{self.args.base}/1.1.1"
        metadata = pd.read_csv(f"{root_dir_name}/echonext_metadata_100k.csv")
        print(metadata.columns)
        print(metadata.head())
        for split in ["train", "val", "test", "no_split"]:
            data = np.load(f"{root_dir_name}/EchoNext_{split}_waveforms.npy")
            print(data.shape)
            input("Hi")
        input("end")


    def open_ecg(self, row,):
        pass

    def reorder_indices(self, ecg):
        current_order = ["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"]
        order_mapping = {lead: index for index, lead in enumerate(current_order)}
        new_indices = [order_mapping[lead] for lead in PTB_ORDER]
        return ecg[:, new_indices]