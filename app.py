# pylint: disable=unused-variable
# pylint: disable=anomalous-backslash-in-string

'''
app.py: Frontend runner file for nCovid_19 Streamlit application

Dependencies
data: data/time_series_covid19_infections.csv, data/time_series_covid19_vaccines.csv
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


file_dict = {'infections':'https://github.com/staedi/nCOV-summary/raw/master/time_series_covid19_infections.csv','vaccines':'https://github.com/staedi/nCOV-summary/raw/master/time_series_covid19_vaccines.csv'}
filename = 'https://github.com/staedi/nCOV-summary/raw/master/time_series_covid19_infections.csv'

################################################################
# Header and preprocessing

# Set Title
st.title('nCOV-19 Status (Infections, Vaccinations)')

# Initial data load
# update_status = st.markdown("Loading infections data...")
data = generic.read_dataset(file_dict)
# update_status.markdown('Load complete!')

################################################################
# Sidebar section (Only multi-states country can be chosen)
sel_region, sel_country, chosen_stat, sel_map = frontend.display_sidebar(data)

################################################################
# Main section
# update_status.markdown("Finding top districts...")
cand = generic.set_candidates(data,sel_region,sel_country,chosen_stat)


# update_status.markdown("Calculation complete!")
#
# update_status.markdown("Drawing charts")
# if sel_map:
#     update_status.markdown("Drawing charts & maps...")
# else:
#     update_status.markdown("Drawing charts...")
frontend.show_stats(data,sel_region,sel_country,chosen_stat,cand,sel_map)
# update_status.markdown("Job Complete!")

# Caption for credits
st.subheader('Credits')
infections = f'\n* Global and US: Johns Hopkins University CSSE GitHub'
infections += f'\n* South Korea: South Korean CDC'

# vaccinations = f'\n* Global and US: Johns Hopkins University GoVex GitHub'
# vaccinations += f'\n* South Korea: South Korean CDC'
# vaccinations += f'\n* Australia: COVID Live'
# vaccinations += f'\n* Canada: COVID-19 Tracker Project'
# vaccinations += f'\n* UK: Public Health England'

st.write('Infections data source ' + infections)
# st.write('Vaccinations data source ' + vaccinations)
st.write('Map shapedata: Natural Earth')
st.write('Map provider: Carto')
