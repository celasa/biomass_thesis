from pathlib import Path
import pandas as pd

def get_shadow_prices2(shadow_dfs, metabolites):
    rows = []

    for df in shadow_dfs:
        row = {}

        for met in metabolites:
            match = df.loc[df["metabolite"] == met, "shadow_price"]

            col = "o2_e_shadow" if met == "o2_e" else "source_shadow"
            row[col] = match.iloc[0] if not match.empty else None

        rows.append(row)

    return pd.DataFrame(rows)

def add_shadow_prices2(formatted_df, shadow_dfs, metabolites):
    shadow_df = get_shadow_prices2(shadow_dfs, metabolites)

    for col in shadow_df.columns:
        formatted_df[col] = shadow_df[col].values

    return formatted_df

def build_substrate_df(sample_path, shadow_path, template_path, substrate, metabolites):
    sample_dfs = get_samples(sample_path)
    shadow_dfs = get_samples(shadow_path)

    merged = merge_samples(sample_dfs, template_path, substrate)
    formatted = format_sample_df(merged, substrate)
    formatted = add_shadow_prices2(formatted, shadow_dfs, metabolites)

    return formatted

def get_samples(path):
    # make one large list before using merge_samples when combining all 
    """"Returns a list of DataFrames, each df is the entire flux vector/shaadow price vector of a sample"""
    folder = Path(path)
    files = sorted(folder.glob("*.pkl"))
    dfs = [pd.read_pickle(pkl) for pkl in files]

    return dfs


    # use balanced_template.csv
def merge_samples(sample_dfs, template_path, substrate):
    """"Merges all samples together in one dataframe, based on template"""
    template = pd.read_csv(template_path)
    dfs = sample_dfs

    c=0
    for df in dfs:
        df.rename(columns={'flux': f'{substrate}_sample_{c}'}, inplace=True)
        c+=1
    
    # merge with template:
    merged_all = template.copy()
    # merged_all['source'] = substrate

    for df in dfs:
        merged_all = pd.merge(merged_all, df, on='reaction',  how='inner')

    return merged_all


def format_sample_df(merged_df, substrate):
    """
    Transposes the merged sample dataframe so samples become rows
    and reactions become columns.
    """
    formatted = merged_df.set_index('reaction', drop=True).T
    formatted = formatted.reset_index().rename(columns={'index': 'sample'}) # make sample names a column instead of index
    formatted['env'] = substrate
    return formatted

def fix_col_names(samples_df, substrate):   
    c = 0
    for df in samples_df:
        df.rename(columns={'flux': f'{substrate}_sample_{c}'}, inplace=True)
        c+=1
    return samples_df