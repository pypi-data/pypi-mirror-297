import streamlit as st
from __init__ import dot_plot
from data import data_

st.set_page_config(layout="wide")

Legends = [
    {
      "index": 0, "label": "Player level active", "color": "#000000a8", "border": "white"
    },
    {
      "index": 1, "label": "Player level inactive", "color": "white", "border": "black"
    },
    {
      "index": 2, "label": "Player level upgraded", "color": "white", "border": "black", "inner": "black"
    }

]

columnTitle="Hero Level"
indexTitle="Skill level"
firstCategoryTitle="Skill 1"
secondCategoryTitle="Skill 2"


# with st.columns([1,8,1])[1]:
dot_plot(activeLvlColor="pink", data=data_, indexTitle=indexTitle, columnTitle=columnTitle, Legends=Legends)



