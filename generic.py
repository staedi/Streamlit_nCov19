# pylint: disable=unused-variable
# pylint: disable=anomalous-backslash-in-string

import pandas as pd
from datetime import datetime
import streamlit as st
# import pydeck as pdk

read_columns = {7:['Confirmed','Confirmed'],8:['r_Confirmed','Confirmed per 100K'],9:['i_Confirmed','Daily Confirmed'],10:['ri_Confirmed','Daily Confirmed per 100K'],11:['Tot_Confirmed','Total Confirmed'],12:['iTot_Confirmed','Daily Total Confirmed'],13:['rTot_Confirmed','Total Confirmed per 100K'],14:['riTot_Confirmed','Daily Total Confirmed per 100K'],15:['Deaths','Deaths'],16:['r_Deaths','Deaths per 100K'],17:['i_Deaths','Daily Deaths'],18:['ri_Deaths','Daily Deaths per 100K'],19:['Tot_Deaths','Total Deaths'],20:['iTot_Deaths','Daily Total Deaths'],21:['rTot_Deaths','Total Deaths per 100K'],22:['riTot_Deaths','Daily Total Deaths per 100K']}

# Load dataset
@st.cache
def read_dataset(filename):
    data = pd.read_csv(filename,parse_dates=['Date'])
    data['Date'] = data['Date'].apply(lambda x:x.date())
    data.rename(columns={'Lat':'lat','Long':'lon'},inplace=True)
    data['len_states'] = data.groupby(['adm0_a3','Country/Region','Date']).adm0_a3.transform('size')

    neg_keys = list(set(val[0] for val in read_columns.values() if val[0].startswith('i')))

    # No negative values
    for iter in neg_keys:
        data.loc[data[iter]<0,iter] = 0

    return data

# Pre-calculate candidating countries or states
def set_candidates(data,region,country,stat,date=None,cutoff=20):
    if not date:
        date = max(data['Date'])
    dataset = []

    if stat:
        stat_text = list(stat.values())[0]
        stat_keys = list(stat.keys())

        if region:
            data = data.loc[(data['Date']==date) & (data['adm0_a3']==region) & (data['Country/Region']==country) & (data['Province/State']!='Unknown'),['adm0_a3','Country/Region','Province/State',stat_keys[0],stat_keys[1]]].groupby(['adm0_a3','Country/Region','Province/State'])[[stat_keys[0],stat_keys[1]]].mean().reset_index()
        else:
            data = data.loc[(data['Date']==date),['adm0_a3','Country/Region',stat_keys[0],stat_keys[1]]].groupby(['adm0_a3','Country/Region'])[[stat_keys[0],stat_keys[1]]].mean().reset_index()

        for stat_key in stat_keys:
            if region:
                dataset.append( list(data.sort_values(by=stat_key,ascending=False)['Province/State'][:cutoff]))
            else:
                dataset.append( list(data.sort_values(by=stat_key,ascending=False)['adm0_a3'][:cutoff]))

        df_dataset = pd.DataFrame({stat_keys[0]:dataset[0],stat_keys[1]:dataset[1]}).reset_index()

    else:
        df_dataset = pd.DataFrame()

    return df_dataset
