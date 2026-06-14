from pathlib import Path
import numpy as np


from ecg_datasets.map.map_dataset import MapDataset

class HEED(MapDataset):
    def __init__(self, args):
        super().__init__(args)
        self.save_dir_json = f"src/ecg_datasets/map/{self.args.map}/{self.args.map}_hf.json"

    def get_map_data(self,):
        data = []
        saved_dir = f"/batch_data/heed/preprocessed_{self.args.segment_len}"
        self.available_ecgs.update(f.stem for f in Path(saved_dir).glob("*"))
        data.extend(Path(saved_dir).glob("*"))
        return data

    def process_instance(self, instance):
        np_instance = np.load(instance, allow_pickle=True).item()
        return {"ecg_path": "_".join(str(instance.stem).split("_")[:-1]), "text": "; ".join(np_instance["report"]),
                "saved_dir" : "/".join(str(instance).split("/")[:-1]), "name": "None"}
