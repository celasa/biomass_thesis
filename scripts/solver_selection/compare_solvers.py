# Scripts to analyse and compare sovlers
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

########################################### SUMMARY FUNCTIONS #################################################################
totals = {"C": 286, "N": 179, "P": 64, "S": 28}

def count_by_source(df):
    return {
        "C": sum(col.endswith("_C") for col in df.columns),
        "N": sum(col.endswith("_N") for col in df.columns),
        "P": sum(col.endswith("_P") for col in df.columns),
        "S": sum(col.endswith("_S") for col in df.columns),
    }

def summarize(df, solver, condition):
    counts = count_by_source(df)

    row = {
        "condition": condition,
        "solver": solver,
    }

    for source in ["C", "N", "P", "S"]:
        solved = counts[source]
        total = totals[source]

        row[f"{source}_solved"] = solved
        row[f"{source}_total"] = total
        row[f"{source}_success_rate"] = solved / total

    return row

def total_summary(df, solver, condition):
    solved = len(df.columns)
    total = 557

    return {
        "solver": solver,
        "condition": condition,
        "source": "ALL",
        "total": total,
        "solved": solved,
        "success_rate": solved / total,
    }


def common_columns(df_gurobi, df_qminos):

    # Compare number of columns
    print(f'Gurobi columns: {len(df_gurobi.columns)}')
    print(f'qMINOS columns: {len(df_qminos.columns)}')
    print('-------------------------')

    # Convert columns to sets
    gurobi_cols = set(df_gurobi.columns)
    qminos_cols = set(df_qminos.columns)

    # Columns only in Gurobi
    only_in_gurobi = gurobi_cols - qminos_cols

    # Columns only in qMINOS
    only_in_qminos = qminos_cols - gurobi_cols

    print(f"Only in Gurobi ({len(only_in_gurobi)}): {only_in_gurobi}")
    print(f"Only in Qminos ({len(only_in_qminos)}):  {only_in_qminos}")

