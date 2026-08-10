import pandas as pd

class DataLoader:

    def __init__(self,):
        pass

    def load_evaluation_data_set_as_pd(self, file_path):
        return pd.read_csv(file_path)