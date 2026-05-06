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

## 2. Macromolecular dataset with shadow prices
def make_dataset(dfs_list):    
    combined_data = pd.concat(dfs_list, ignore_index=True, sort=False).fillna(0)
    #drop_cols = [col for col in combined_data.columns if '_shadow' in col] # hvis det funker, prøvde å endre i formatted (se 'HER')...
    combined_data.drop(columns=drop_cols, inplace=True)
    
    return combined_data

def build_substrate_df(sample_path, shadow_path, template_path, substrate, met1, met2):
    #The function does four things: (1) merges the substrate flux vectors according to the template, 
    #(2) transposes the merged DataFrame so samples are rows and the template rows become columns, 
    #(3) adds a "source" column which is defined by the limiting nutrient source, 
    #and (4) adds the shadow prices of the limiting nutrient source and oxygen.
    sample_dfs = get_samples(sample_path)
    shadow_dfs = get_samples(shadow_path)

    merged = merge_samples(sample_dfs, template_path, substrate)
    formatted = format_sample_df(merged, substrate)
    formatted = add_shadow_prices(formatted, shadow_dfs, met1, met2)
    formatted[f"{met1}_shadow"] = formatted["source_shadow"] #HER

    return formatted

def format_sample_df(merged_df, substrate):
    """
    Transposes the merged sample dataframe so samples become rows
    and reactions become columns.
    """
    formatted = merged_df.set_index('reaction', drop=True).T
    formatted = formatted.reset_index().rename(columns={'index': 'sample'}) # make sample names a column instead of index
    formatted['source'] = substrate
    return formatted

def add_shadow_prices(formatted_df, shadow_dfs, met1, met2):
    shadow_df = get_shadow_prices(shadow_dfs, met1, met2)

    formatted_df[f"{met1}_shadow"] = shadow_df[f"{met1}_shadow"]
    formatted_df[f"{met2}_shadow"] = shadow_df[f"{met2}_shadow"]
    # formatted_df = compute_shadow_ratios(formatted_df, met1, met2)
    return formatted_df

def get_shadow_prices(shadow_dfs, met1, met2):
    met_x = []
    met_y = []

    for i in shadow_dfs:
        m1 = i.loc[i["metabolite"]==met1, "shadow_price"].iloc[0]
        m2 = i.loc[i["metabolite"]==met2, "shadow_price"].iloc[0] 

        met_x.append(m1)
        met_y.append(m2)

    df = pd.DataFrame({f"{met1}_shadow": met_x, f"{met2}_shadow": met_y})
    return df
