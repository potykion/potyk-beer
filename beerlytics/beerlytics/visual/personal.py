import streamlit as st
import pandas as pd

df = pd.read_json(
    "my-beers.json"
)
df
