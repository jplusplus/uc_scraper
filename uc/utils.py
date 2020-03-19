# encoding:utf-8
import pandas as pd

def parse_int(val):
    """Parse int from str."""
    return int(float(val))


def parse_result_page(html):
    """
    """
    dfs = []
    for df in pd.read_html(html, thousands=' '):
        grouper = df.columns[0]
        value_cols = df.columns[1:].tolist()
        df.columns = ["group"] + value_cols

        df_long = pd.melt(df, id_vars="group", value_vars=df.columns[1:], var_name="dimension")
        df_long["value"] = df_long["value"].apply(pct_to_float)
        df_long["grouper"] = grouper
        dfs.append(df_long)
    df = pd.concat(dfs, sort=False).drop_duplicates().to_dict("records")

    return df

def pct_to_float(x):
    try:
        return float(x.strip('%'))/100
    except:
        return x
