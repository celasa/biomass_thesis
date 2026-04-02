import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# For merging datasets for ML-pipeline, only biomass-vectors

#TODO: get_samples
def get_samples(path):
    # make one large list before using merge_samples when combining all 
    """"Returns a list of DataFrames, each df is the entire flux vector/shaadow price vector of a sample"""
    folder = Path(path)
    files = sorted(folder.glob("*.pkl"))
    dfs = [pd.read_pickle(pkl) for pkl in files]

    return dfs

#TODO: merge_samples
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

#TODO: Format merged_all ()
def format_sample_df(merged_df, substrate):
    """
    Transposes the merged sample dataframe so samples become rows
    and reactions become columns.
    """
    formatted = merged_df.set_index('reaction', drop=True).T
    formatted = formatted.reset_index().rename(columns={'index': 'sample'}) # make sample names a column instead of index
    formatted['source'] = substrate
    return formatted

def make_dataset(dfs_list):    
    combined_data = pd.concat(dfs_list, ignore_index=True, sort=False).fillna(0)
    drop_cols = [col for col in combined_data.columns if '_shadow' in col or col == 'phase']
    combined_data.drop(columns=drop_cols, inplace=True)

    return combined_data

def build_substrate_df(sample_path, shadow_path, template_path, substrate, met1, met2):
    sample_dfs = get_samples(sample_path)
    shadow_dfs = get_samples(shadow_path)

    merged = merge_samples(sample_dfs, template_path, substrate)
    formatted = format_sample_df(merged, substrate)
    formatted = add_shadow_prices(formatted, shadow_dfs, met1, met2)

    return formatted

############################################################### Preprocessing dataset before features are made
# AFTER FORMATTING:
def remove_noise(df, zero_tol):
    df = df.copy()

    num_cols = df.select_dtypes(include="number").columns
    df[num_cols] = df[num_cols].mask(df[num_cols].abs() < zero_tol, 0)
    return df


def balance_sampling(df, phase, n_remove):
    """"To reduce overweight of one phase, use sub_df['phase].value_counts() to decide n_remove. Removes at random."""
    df = df.copy()
    phase_rows = df[df['phase'] == phase]
    n_remove = min(n_remove, len(phase_rows))    #don't try to remove more than exist
    drop_idx = phase_rows.sample(n=n_remove).index
    df_balanced = df.drop(drop_idx)

    return df_balanced


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


# def compute_shadow_ratios(df, met_x, met_y):
#     ratio = -(df[f'{met_x}_shadow']/df[f'{met_y}_shadow'])
#     df['phase'] = ratio.apply(classify_phase)
#     return df

def compute_shadow_ratios(df, met_x, met_y, phase_tol=1e-6):
    num = df[f'{met_x}_shadow']
    den = df[f'{met_y}_shadow']

    alpha = -(num / den)

    den_small = den.abs() < phase_tol
    num_small = num.abs() < phase_tol

    alpha.loc[den_small] = np.inf
    alpha.loc[~den_small & num_small] = 0.0

    df['alpha'] = alpha
    df['phase'] = alpha.apply(classify_phase)
    return df


# def classify_phase(row, inf_threshold=130, zero_threshold=0.002):
#     """"inf_threshold: alpha is very large, single-substrate limited
#         zero_threshold: alpha~0, single-substrate limited (x_shadow is 0)"""
#     r = row
#     if r > inf_threshold:   # extreme case, reset ratio
#         # return r'$\alpha$ $\rightarrow$ $\infty$'
#         return 'single_lim_inf'
#     elif zero_threshold >= r >= 0:  # glucose shadow is zero
#         # return r'$\alpha$ = 0'
#         return 'single_lim_zero'
#     elif r < 0:
#         #return r'$\alpha$<1' #dual
#         return 'dual_lim'
#     elif abs(r) < 1:
#         # return r'|$\alpha$|<1'
#         return 'abs_alpha<1'
#     else:
#         # return r'$\alpha$>0'
#         return 'futile'

def classify_phase(alpha):
    if alpha == np.inf:
        # return r'$\alpha$ $\rightarrow$ $\infty$'
        return 'single_lim_inf'
    elif alpha == 0:
        # return r'$\alpha$ = 0'
        return 'single_lim_zero'
    elif alpha < 0:
        #return r'$\alpha$<1' #dual
        return 'dual_lim'
    elif abs(alpha) < 1:
        # return r'|$\alpha$|<1'
        return 'abs_alpha<1'
    else:
        # return r'$\alpha$>0'
        return 'futile'
    
def get_phases(shadow_dfs, met1, met2): # hvis jeg skal bruke på output til get_samples
    for i in shadow_dfs:
        compute_shadow_ratios(i, met1, met2)
    return shadow_dfs

############################### OUTLIER DETECTION ##############################
import math
import matplotlib.pyplot as plt

def plot_biomass_fractions(df, source_name, x_col='biomass_dilution', title=None, n_cols=4):
    """
    Funksjon for å plotte biomasse-fraksjoner for en spesifikk kilde.
    
    Parameters:
    - df: Hele DataFrame (bm)
    - source_name: Streng som matcher 'source' kolonnen (f.ex. 'ac', 'glc')
    - x_col: Kolonnenavn for x-aksen
    - title: Overskrift for hele figuren (suptitle)
    - n_cols: Antall kolonner i subplot-gridet
    """
    
    # 1. Filtrer data basert på kilde
    filtered_df = df[df['source'] == source_name].copy()
    
    if filtered_df.empty:
        print(f"Advarsel: Ingen data funnet for kilde '{source_name}'")
        return

    # 2. Identifiser kolonner som skal plottes (alle unntatt x_col og source)
    y_cols = [col for col in filtered_df.columns if col not in [x_col, 'source']]
    
    n_plots = len(y_cols)
    n_rows = math.ceil(n_plots / n_cols)

    # 3. Opprett figur
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 4 * n_rows))
    axes = axes.flatten()

    for i, y_col in enumerate(y_cols):
        # Plotting
        axes[i].scatter(filtered_df[x_col], filtered_df[y_col], alpha=0.6, s=15)
        
        # Formatering av titler og akser
        short_label = y_col.split('_')[0]
        axes[i].set_title(f"{short_label} vs {x_col.split('_')[0]}", fontsize=12)
        axes[i].set_xlabel(x_col)
        axes[i].set_ylabel(f'{short_label} biomass fraction')
        axes[i].grid(True, linestyle='--', alpha=0.5)

    # 4. Fjern ubrukte subplots
    for j in range(n_plots, len(axes)):
        fig.delaxes(axes[j])

    # 5. Tittel og layout
    if title:
        plt.suptitle(title, fontsize=22, y=1.02)
    else:
        plt.suptitle(f'Source: {source_name}', fontsize=22, y=1.02)
        
    plt.tight_layout()
    plt.show()

