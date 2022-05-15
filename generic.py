# pylint: disable=unused-variable
# pylint: disable=anomalous-backslash-in-string

import pandas as pd
from datetime import datetime
import streamlit as st
# import pydeck as pdk

read_columns = {'infections':{7:['confirmed','Confirmed'],8:['r_confirmed','Confirmed per 100K'],9:['i_confirmed','Daily Confirmed'],10:['ri_confirmed','Daily Confirmed per 100K'],11:['Tot_confirmed','Total Confirmed'],12:['iTot_confirmed','Daily Total Confirmed'],13:['rTot_confirmed','Total Confirmed per 100K'],14:['riTot_confirmed','Daily Total Confirmed per 100K'],15:['deaths','Deaths'],16:['r_deaths','Deaths per 100K'],17:['i_deaths','Daily Deaths'],18:['ri_deaths','Daily Deaths per 100K'],19:['Tot_deaths','Total Deaths'],20:['iTot_deaths','Daily Total Deaths'],21:['rTot_deaths','Total Deaths per 100K'],22:['riTot_deaths','Daily Total Deaths per 100K']},'vaccines':{7:['admin','Administered'],8:['r_admin','Administered per 100K'],9:['i_admin','Daily Administered'],10:['ri_admin','Daily Administered per 100K'],11:['Tot_admin','Total Administered'],12:['iTot_admin','Daily Total Administered'],13:['rTot_admin','Total Administered per 100K'],14:['riTot_admin','Daily Total Administered per 100K'],15:['full','Fully Vaccinated'],16:['r_full','Fully Vaccinated per 100K'],17:['i_full','Daily Fully Vaccinated'],18:['ri_full','Daily Fully Vaccinated per 100K'],19:['Tot_full','Total Fully Vaccinated'],20:['iTot_full','Daily Total Fully Vaccinated'],21:['rTot_full','Total Fully Vaccinated per 100K'],22:['riTot_full','Daily Total Fully Vaccinated per 100K']}}
# read_columns = {7:['confirmed','Confirmed'],8:['r_confirmed','Confirmed per 100K'],9:['i_confirmed','Daily Confirmed'],10:['ri_confirmed','Daily Confirmed per 100K'],11:['Tot_confirmed','Total Confirmed'],12:['iTot_confirmed','Daily Total Confirmed'],13:['rTot_confirmed','Total Confirmed per 100K'],14:['riTot_confirmed','Daily Total Confirmed per 100K'],15:['deaths','Deaths'],16:['r_deaths','Deaths per 100K'],17:['i_deaths','Daily Deaths'],18:['ri_deaths','Daily Deaths per 100K'],19:['Tot_deaths','Total Deaths'],20:['iTot_deaths','Daily Total Deaths'],21:['rTot_deaths','Total Deaths per 100K'],22:['riTot_deaths','Daily Total Deaths per 100K']}

# Load dataset
@st.cache
# def read_dataset(filename):
def read_dataset(file_dict):
    data_dict = {}

    for key, filename in file_dict.items():
        data_dict[key] = pd.read_csv(filename,parse_dates=['Date'])
        data_dict[key]['Date'] = data_dict[key]['Date'].apply(lambda x:x.date())
        data_dict[key].rename(columns={'Lat':'lat','Long':'lon'},inplace=True)
        data_dict[key]['len_states'] = data_dict[key].groupby(['adm0_a3','Country/Region','Date']).adm0_a3.transform('size')

        neg_keys = list(set(val[0] for val in read_columns[key].values() if val[0].startswith('i')))

    return data_dict

# Pre-calculate candidating countries or states
def set_candidates(data,region,country,stat,date=None,cutoff=20):
    # if not date:
    #     date = max(data['Date'])

    if not date:
        date = max([max(data[key]['Date']) for key in data.keys()])
    dataset = []

    # if stat:
    stat_len = min([len(val) for val in stat.values()])

    if stat_len > 0:
        for key, stat_key in stat.items():
            if region:
                dataset.append(data[key].loc[(data[key]['Date']==date) & (data[key]['adm0_a3']==region) & (data[key]['Country/Region']==country) & (data[key]['Province/State']!='Unknown'),['adm0_a3','Country/Region','Province/State']+stat_key].groupby(['adm0_a3','Country/Region','Province/State'])[stat_key].mean().reset_index().dropna())
            else:
                dataset.append(data[key].loc[(data[key]['Date']==date),['adm0_a3','Country/Region']+stat_key].groupby(['adm0_a3','Country/Region'])[stat_key].mean().reset_index().dropna())

        dataset_dict = {}

        for idx, key in enumerate(stat):
            # st.write(idx,key,stat[key])
            for stat_idx, stat_key in enumerate(stat[key]):
                if region:
                    if 'Tot' not in stat_key:
                        dataset_dict[stat_key] = list(dataset[idx].sort_values(by=stat_key,ascending=False)['Province/State'][:cutoff])
                    else:
                        dataset_dict[stat_key] = list(dataset[idx].sort_values(by=stat_key,ascending=False)['adm0_a3'][:cutoff])

                    if len(dataset_dict[stat_key]) == 0:
                        # dataset_dict[stat_key] = [region]*cutoff
                        # st.write(stat[key],stat_key)
                        stat[key] = [stat_col for stat_col in stat[key] if stat_col != stat_key or 'Tot' in stat_col]
                    else:
                        stat[key] = [stat_col for stat_col in stat[key] if 'Tot' not in stat_col]
                else:
                    dataset_dict[stat_key] = list(dataset[idx].sort_values(by=stat_key,ascending=False)['adm0_a3'][:cutoff])

        dataset_dict = {key:stat_key for key,stat_key in dataset_dict.items() if stat_key and region not in stat_key}

        sizes = {}

        for key, stat_key in dataset_dict.items():
            if not sizes.get('min') or (sizes.get('min') and len(dataset_dict[sizes['min']]) > len(stat_key)):
                sizes['min'] = key
            if not sizes.get('max') or (sizes.get('max') and len(dataset_dict[sizes['max']]) < len(stat_key)):
                sizes['max'] = key

        residues = list(set(dataset_dict[sizes['max']])-set(dataset_dict[sizes['min']]))

        for stat_key, val in dataset_dict.items():
            if len(val) < len(dataset_dict[sizes['max']]):
                dataset_dict[stat_key].extend(residues)

        len_cand = min([len(cand) for cand in dataset_dict.values()])


        df_dataset = pd.DataFrame(dataset_dict).reset_index()


    else:
        df_dataset = pd.DataFrame()

    return df_dataset