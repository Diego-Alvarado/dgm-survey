import random
import pandas as pd

def load_mats(filepath: str) -> pd.DataFrame:
    df_materials = pd.read_csv(filepath, sep='\t')
    return df_materials

def load_seqs(filepath: str, seed: int) -> tuple[pd.DataFrame, dict]:
    df_sequences = pd.read_csv(filepath, sep='\t')
    df_sequences = df_sequences.fillna('')
    cols = ['A', 'B']
    random.seed(seed)
    random.shuffle(cols)
    df_sequences = df_sequences[cols]
    df_sequences.columns = ['A', 'B']
    df_sequences = df_sequences.reset_index()
    actual_values = {'actual': cols[0], 'generated': cols[1]}
    return df_sequences, actual_values

def load_df(file_names: dict, key: int) -> tuple[pd.DataFrame, dict]:
    df_materials = pd.read_csv(file_names[key]['materials'], sep='\t')
    # df_materials['structure'] = [file_names[key]["materials"][:-4] + f'_{id}.png' for id in df_materials['index']]
    
    df_sequences = pd.read_csv(file_names[key]["sequences"], sep='\t')
    df_sequences = df_sequences.fillna('')
    cols = ['A', 'B']
    random.seed(key)
    random.shuffle(cols)
    df_sequences = df_sequences[cols]
    df_sequences.columns = ['A', 'B']
    df_sequences = df_sequences.reset_index()
    actual_values = {'actual': cols[0], 'generated': cols[1]}
    return df_materials, df_sequences, actual_values