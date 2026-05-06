# Cleaning up construction of datasets:

## 1. Biomass-producing reactions datasets
def get_samples(path):
    # make one large list before using merge_samples when combining all 
    """"Returns a list of DataFrames, each df is the entire flux vector/shaadow price vector of a sample"""
    folder = Path(path)
    files = sorted(folder.glob("*.pkl"))
    dfs = [pd.read_pickle(pkl) for pkl in files]

    return dfs


def fix_col_names(samples_df, substrate):   
    c = 0
    for df in samples_df:
        df.rename(columns={'flux': f'{substrate}_sample_{c}'}, inplace=True)
        c+=1
    return samples_df
