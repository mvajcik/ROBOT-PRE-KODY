import pandas as pd
from src.transform import transform_block  # už ho máš v projekte

def test_transform_contract_min():
    # mini vstup (môžeš použiť aj prázdny DF – ide o kontrakt výstupu)
    raw = pd.DataFrame()

    out_df, *_ = transform_block(raw)  # prvá položka = DataFrame

    # očakávané stĺpce v správnom poradí
    expected_cols = ["Country", "Week", "Metric", "Value"]
    assert list(out_df.columns[:4]) == expected_cols

    # typy: Week int, Value number
    assert pd.api.types.is_integer_dtype(out_df["Week"])
    assert pd.api.types.is_numeric_dtype(out_df["Value"])