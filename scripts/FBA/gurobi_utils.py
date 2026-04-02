from cobrame.solve import algorithms


def run_substrate_gurobi(model, substrate):
    """Solves model with input substrate"""

    rxn = model.reactions.get_by_id(substrate)
    rxn.lower_bound = -1000

    solution = algorithms.binary_search(model, min_mu=0.1, max_mu=2.0, verbose=True, solver="gurobi", mu_accuracy=1e-6)

    return {"fluxes": solution.x_dict, 
            "shadow": solution.y_dict,
            "mu": solution.f}