import pandas as pd


def set_env(model, aerobic, source):
    if aerobic == False:
        model.reactions.EX_o2_e.lower_bound = 0

    get_input(model, source)


def set_default_env(model, aerobic):
    if aerobic == False:
        model.reactions.EX_o2_e.lower_bound = 0


def get_source_list(model, source):
    source_dict = filter_sources(model)
    source_list = source_dict[source]
    return source_list


def set_source_list(source, source_list):
    filter_sources[source] = source_list


def get_input(model, source):
    """Sets default source uptake flux to 0"""
    if source == "C":
        model.reactions.get_by_id('EX_glc__D_e').lower_bound = 0
    if source == "N":
        model.reactions.get_by_id('EX_nh4_e').lower_bound = 0
    if source == "S":
        model.reactions.get_by_id('EX_so4_e').lower_bound = 0
    if source == "P":
        model.reactions.get_by_id('EX_pi_e').lower_bound = 0



def filter_sources(model):
    sources = {"C":[], "N":[], "S":[], "P":[]}
    ex_rxns = get_exchanges(model)

    for r in ex_rxns:
        met = r.id.replace('EX_', '')
        element = model.metabolites.get_by_id(met).elements

        for e in sources:
            if e in element:
                sources[e].append(r.id)

    return sources


def get_exchanges(model):
    ex_rxns = []

    for r in model.reactions.query('EX_'):
        if not r.id.startswith('EX_'):
            continue
        ex_rxns.append(r)
    return ex_rxns
