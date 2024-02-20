import random
import pandas as pd

def load_df(file_names: dict, key: int) -> tuple[pd.DataFrame]:
    df_materials = pd.read_csv(f'data/sample_cvae/{file_names[key]["materials"]}', sep='\t')
    df_materials['structure'] = [file_names[key]["materials"][:-4] + f'_{id}.png' for id in df_materials['index']]
    
    df_sequences = pd.read_csv(f'data/sample_cvae/{file_names[key]["sequences"]}', sep='\t')
    df_sequences = df_sequences.fillna('')
    cols = ['A', 'B']
    random.seed(key)
    random.shuffle(cols)
    df_sequences = df_sequences[cols]
    df_sequences.columns = ['A', 'B']
    df_sequences = df_sequences.reset_index()
    return df_materials, df_sequences