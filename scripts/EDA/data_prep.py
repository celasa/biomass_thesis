# Cleaning up construction of datasets:

## 1. Biomass-producing reactions datasets



def fix_col_names(samples_df, substrate):   
    c = 0
    for df in samples_df:
        df.rename(columns={'flux': f'{substrate}_sample_{c}'}, inplace=True)
        c+=1
    return samples_df
