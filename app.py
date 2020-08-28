# pylint: disable=unused-variable
# pylint: disable=anomalous-backslash-in-string

'''
app.py: Frontend runner file for nCovid_19 Streamlit application

Dependencies
data: data/time_series_covid19.csv
modules:
frontend.py: Front-end works
generic.py: Load necessary files (infections, map)
'''

import streamlit as st
import pandas as pd
import generic
import frontend
import pydeck as pdk
import math

filename = 'data/time_series_covid19.csv'

################################################################
# Header and preprocessing

# Set Title
st.title('Covid 19 Status Dashboard')

# Initial data load
update_status = st.markdown("Loading latest data...")
covid = generic.read_dataset(filename)
update_status.markdown('Load complete!')

################################################################
# Sidebar section (Only multi-states country can be chosen)
sel_region, sel_country, chosen_stat, sel_map = frontend.display_sidebar(covid)


################################################################
# Main section
cand = generic.set_candidates(covid,sel_region,sel_country,chosen_stat)
frontend.show_stats(covid,sel_region,sel_country,chosen_stat,cand,sel_map)
