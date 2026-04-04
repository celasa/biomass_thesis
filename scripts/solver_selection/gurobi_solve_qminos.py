from cobrame.solve import algorithms
import pandas as pd
########################################### FUNCTIONS FOR qMINOS-FBA OUTPUT AS GUROBI-FBA INPUT########################################

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
