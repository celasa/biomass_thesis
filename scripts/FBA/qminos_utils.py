from qminospy.me1 import ME_NLP1

def run_substrate_qminos(model, substrate):
    """Solves model with input substrate"""
    rxn = model.reactions.get_by_id(substrate)
    rxn.lower_bound = -1000

    me_nlp = ME_NLP1(model, growth_key='mu')
    muopt, hs, xopt, cache = me_nlp.bisectmu(precision=1e-6, mumax=1.5)

    solution = model.solution.x_dict
    model.solution.f = model.solution.x_dict['biomass_dilution']

    return {"fluxes": solution,
            "shadow": model.solution.y_dict,
            "mu": model.solution.f}
