### PROGRAM FOR Å KJØRE FVA MED GUROBI VS QMINOS; ALLE ULIKE IMPLEMENTATIONS!#########
import pickle
import pandas as pd
from cobrame.solve import algorithms
from qminospy.me1 import ME_NLP1
import gurobipy as gp
import matplotlib.pyplot as plt

########################################### FVA FUNCTIONS FOR qMINOS-FBA OUTPUT AS GUROBI-FVA INPUT########################################

#FVA 1.0

def load_df_from_file(env, source, path_to_csv):

    flux_file_name = f'flux_EX_{env}_e_{source}_aerobic.csv'
    flux_df = pd.read_csv(path_to_csv)
    flux_df = flux_df.iloc[1:]

    return flux_df


# def set_fluxes_from_df(df, model):
#     """"Fix upper bound to be exactly as qMINOS"""
#     for row in df.itertuples(index=False):
#         rxn_id = row.reaction
#         flux = row.flux
#         rxn = model.reactions.get_by_id(rxn_id)
        
#         rxn.bounds = (flux, flux)

def set_bounds_from_df(df, model):
#   """Relax the boundaries since Gurobi struggles"""
    for row in df.itertuples(index=False):
        rxn_id = row.reaction
        flux = row.flux
        rxn = model.reactions.get_by_id(rxn_id)
        
        if flux < 0:
            rxn.bounds = (flux, 0)
        elif flux > 0:
            rxn.bounds = (0, flux)
        else:
            rxn.bounds = (0,0)

def run_flux_input(source_dict, env):
    
    env_df = source_dict[env]
    set_bounds_from_df(env_df, model)
    print(f'Trying to solve with qMINOS soluton in {env}...')

    try:
        solution = algorithms.binary_search(model, solver='gurobi', 
                                            mu_accuracy=1e-6,  max_mu=1.5, 
                                            min_mu=0.1, verbose=False)
        return solution.f
    
    except Exception as e:
        print(f'Failed for {env}: {e}')
        return None


########################################### FVA FUNCTIONS AFTER STABILITY TEST (FVA 3.0) ########################################
def get_row(df, rxn):
    row = df[df['reaction']==rxn]
    return row

def get_fva_reactions(model, rxns):
    """returns indexes of reactions to run FVA\n
    Takes reaction list (rxns) as input"""
    indexes = {rxn: model.reactions.index(model.reactions.get_by_id(rxn)) 
           for rxn in rxns}
    
    return model.reactions[min(indexes.values()):max(indexes.values())+1]

def get_fba_gr(df, input_substrate, env):
    # returns objective value of FBA with input_substrate in provided environment (env)
    gr = df.loc[df['Reaction']=='biomass_dilution', f'{input_substrate}_{env}'].values[0]
    
    return gr


def run_fva_dict(model, growth_dict, solver):

    fva_results = {}
    for input, gr in growth_dict.items():

        if solver == 'gurobi':
            if gr > 0.835: # FVA 3.0, 2.0 is the same without this step!
                continue
            
            print(f'Starting FVA for {input}...')
            fva = algorithms.fva(model, gr, model.reactions[45:55], solver='gurobi')
            # fva_results[input] = (fva[input]['minimum'], fva[input]['maximum'])
            fva_results[input] = fva

        
        elif solver == 'qminos':
            me_nlp = ME_NLP1(model, 'mu')
            print(f'Starting FVA for {input}...')
            fva = me_nlp.varyme(mu_fixed=gr, rxns_fva0=model.reactions[45:55], basis=None)
            fva = fva[0]
            # fva_results[input] = (fva[input]['minimum'], fva[input]['maximum'])
            fva_results[input] = fva
        
    return fva_results



def plot_fva(df, title, figsize=(12,6)):
    """
    Plot FVA flux spans (min to max) for all metabolites in the dataframe.
    Bars are grouped by reaction, each metabolite in a different color.
    
    Parameters:
    - df: DataFrame with columns ['metabolite', 'reaction', 'minimum', 'maximum']
    - figsize: tuple for figure size
    """
    df_plot = df.copy()
    
    # Shorten reaction names to first word
    df_plot['reaction_short'] = df_plot['reaction'].apply(lambda x: x.split('_')[0])
    
    # Unique reactions and metabolites
    reactions = df_plot['reaction_short'].unique()
    metabolites = df_plot['metabolite'].unique()
    n_metab = len(metabolites)
    
    # Set up positions for grouped bars
    x_pos = np.arange(len(reactions))
    bar_width = 0.8 / n_metab  # divide space for metabolites
    colors = plt.cm.tab10.colors  # color palette
    
    plt.figure(figsize=figsize)
    
    for i, metab in enumerate(metabolites):
        df_metab = df_plot[df_plot['metabolite'] == metab]
        # Align bars: shift by i*bar_width
        plt.bar(
            x=x_pos - 0.4 + i*bar_width + bar_width/2,
            height=df_metab['maximum'] - df_metab['minimum'],
            bottom=df_metab['minimum'],
            width=bar_width,
            color=colors[i % len(colors)],
            label=metab
        )
    
    plt.xticks(x_pos, reactions, rotation=45)
    plt.ylabel("Flux range (log)")
    plt.yscale('log')
    # plt.xlabel("Reaction")
    plt.title(title)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title="Metabolite")
    plt.tight_layout()
    plt.show()