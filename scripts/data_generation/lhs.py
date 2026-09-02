import numpy as np
import pickle
from skopt.sampler import Lhs
from skopt.space import Real
from qminospy.me1 import ME_NLP1
import csv
import fcntl

def generate_sample_space(source_range, oxygen_range=None, lo=False, n_samples=50, criterion='maximin'):
    """
    Generate Latin Hypercube Samples using skopt.sampler.Lhs.

    Parameters
    ----------
    source_range : list or tuple [min, max]
        Nutrient source uptake bounds
    oxygen_range : list or tuple [min, max] or None
        Oxygen uptake bounds; ignored if lo=True
    lo : bool
        Whether to generate 1D LO samples (True) or 2D plane (False)
    n_samples : int
        Number of LHS samples to generate
    criterion : str
        LHS criterion; 'maximin' is recommended

    Returns
    -------
    List of tuples
        Each tuple is (source,) for LO or (source, oxygen) for 2D.
    """

    lhs_sampler = Lhs(criterion=criterion, iterations=1000)

    if lo:
        # 1D LHS
        space = [Real(source_range[0], source_range[1])]
        samples = lhs_sampler.generate(space, n_samples)
        return [(c[0],) for c in samples]
    else:
        # 2D LHS
        space = [Real(source_range[0], source_range[1]), Real(oxygen_range[0], oxygen_range[1])]
        samples = lhs_sampler.generate(space, n_samples)
        return [tuple(s) for s in samples]
    

####################################################################################
def set_uptake_bounds(model, source_category, source, uptake, oxygen=None, lo_fixed=None, alt_C=None):
    """
    Sets uptake flux bounds for ME-model for PhPP sampling.

    Parameters
    -----------
    model: CobraME-Model\n
    source_category: C for carbon source or N for nitrogen source\n
    source: Exhcange reaction for carbon or nitrogen source\n
    uptake: float\n
        source uptake flux
    oxygen: float or None\n
        Oxygen uptake flux for 2D plane
    lo_fixed: float or None\n
        Fixed oxygen value for LO-line sampling
    alt_C: Alternative carbon source\n 
        if source_category=N, and glucose uptake is zero
    """

    # lock nitrogen or carbon uptake:
    if source_category == 'N':
         run_nitrogen(model, n_source=source, n_uptake=uptake)
    if source_category == 'C':
         run_carbon(model, c_source=source, c_uptake=uptake)
        
    # remove glucose if varying N-uptake with different C-source
    if alt_C !=None:
         model.reactions.get_by_id(alt_C).lower_bound = -1000
         model.reactions.get_by_id('EX_glc__D_e').lower_bound = 0

    # lock oxygen uptake if sampling sampling 2D PhPP, keep as None if only sampling LO
    if oxygen is not None:
         model.reactions.get_by_id('EX_o2_e').bounds = (oxygen, oxygen)
    # set high oxygen uptake when varying C-uptake for LO-sampling:
    elif lo_fixed is not None:
         model.reactions.get_by_id('EX_o2_e').lower_bound = lo_fixed #if None, remain -1000
        
####################################################################################
def run_nitrogen(model, n_source, n_uptake):
     if n_source != 'EX_nh4_e':
        model.reactions.get_by_id('EX_nh4_e').lower_bound = 0
     model.reactions.get_by_id(n_source).bounds = (n_uptake, n_uptake)

def run_carbon(model, c_source, c_uptake):
     if c_source != 'EX_glc__D_e':
          model.reactions.get_by_id('EX_glc__D_e').lower_bound = 0  
     model.reactions.get_by_id(c_source).bounds = (c_uptake, c_uptake)

####################################################################################
def solve_sample_point(model):
    """
    Solve a single ME-model optimization problem at fixed environmental conditions.

    Returns
    -------
    dict\n
        A dictionary containing the optimal solution at this grid point with
        the following entries:

        - "fluxes" : dict\n
            Dictionary mapping reaction IDs to their optimal flux values
            at optimal growth-rate.
        - "shadow" : dict
            Dictionary mapping metabolite IDs to their corresponding shadow prices
            from final solve.
    """

    me_nlp = ME_NLP1(model, growth_key='mu')
    muopt, hs, xopt, cache = me_nlp.bisectmu(precision=1e-6, mumax=2.0)

    solution = model.solution.x_dict
    model.solution.f = model.solution.x_dict['biomass_dilution']

    return {"fluxes": solution,
            "shadow": model.solution.y_dict}

################################################################################
def run_phpp_sampler(model, source_type, source, sample_point, lo_fixed=None, alt_C=None):
     
    # LO-line:
    if len(sample_point) == 1:
         uptake = sample_point[0]
         set_uptake_bounds(model, source_type, source, uptake, lo_fixed=lo_fixed, alt_C=alt_C)
         oxygen_uptake = lo_fixed

    else: # 2D plane:
         uptake, oxygen = sample_point
         set_uptake_bounds(model, source_type, source, uptake, oxygen=oxygen, alt_C=alt_C)
         oxygen_uptake = oxygen

    phenotype = solve_sample_point(model)
    if phenotype is not None:
         phenotype.update({
              "n_source": source,
              "n_uptake": uptake,
              "oxygen_uptake": oxygen_uptake
         })

    return phenotype
    
##################################################################################################

def load_me(path):
    with open(path, 'rb') as f:
        model = pickle.load(f)
    return model

######################################################################
def write_time(sample, sample_point, value, timing_csv):
    with open(timing_csv, "a", newline="") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        writer = csv.writer(f)
        writer.writerow([sample, sample_point, value])
        fcntl.flock(f, fcntl.LOCK_UN)
