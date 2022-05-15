# Global Summary
# Infections / Deaths
# Administered / Fully Vaccinated (%)

# Daily Changes / Daily Changes Per 100K (%)
# Infections, Deaths, Administered, Fully Vaccinated
# Country + State
# Line Graphs / Heatmap


# pylint: disable=unused-variable
# pylint: disable=anomalous-backslash-in-string

import generic
import pandas as pd
import numpy as np
import math
import altair as alt
import pydeck as pdk
import streamlit as st

read_columns = {'infections':{7:['confirmed','Cumulative (Up-To-Date)'],9:['i_confirmed','Changes (Daily)'],11:['Tot_confirmed','Cumulative (Up-To-Date)'],12:['iTot_confirmed','Changes (Daily)'],15:['deaths','Cumulative (Up-To-Date)'],17:['i_deaths','Changes (Daily)'],19:['Tot_deaths','Cumulative (Up-To-Date)'],20:['iTot_deaths','Changes (Daily)']},'vaccines':{7:['r_admin','Cumulative (Up-To-Date)'],9:['ri_admin','Changes (Daily)'],11:['rTot_admin','Cumulative (Up-To-Date)'],12:['riTot_admin','Changes (Daily)'],15:['r_full','Cumulative (Up-To-Date)'],17:['ri_full','Changes (Daily)'],19:['rTot_full','Cumulative (Up-To-Date)'],20:['riTot_full','Changes (Daily)']}}

# Module to display sidebar
def display_sidebar(data):
    # adm0_a3, Country/Region
    sel_region,sel_country = None, None

    # Sidebar sections to provide choices (Region, State)
    # if not check:
    #     # Choose a startdate to display
    #     st.sidebar.header('Choose a startdate below')
    #     st.sidebar.markdown('Choose a startdate (e.g., 2020-08-15)')
    #     startdate = st.sidebar.slider('Startdate',data['Date'].unique()[0],data['Date'].unique()[-1])
    #
    # else:

    st.sidebar.header('Choose options below')
    # 0) Need to reset data
    st.sidebar.markdown('Reset dataset?')
    if st.sidebar.button(label='Clear cache'):
        st.caching.clear_cache()
        st.experimental_rerun()

    # 1) Choose a Region/Country to display
    # st.sidebar.subheader('Choose Region/Country below')
    # st.sidebar.subheader('*Note*: Only multi-states countries are currently supported!')

    # Set candiates of region (Country/Region)
    st.sidebar.markdown('Choose a Country/Region (e.g., Canada)')

    country = sorted(set(data['infections'].loc[data['infections']['len_states']>1,'Country/Region']) & set(data['vaccines']['Country/Region']))
    # country = sorted(data.loc[data['len_states']>1,'Country/Region'].unique())
    country = ['Worldwide'] + list(country[:])
    sel_country = st.sidebar.selectbox('Country/Region',country)

    # Candiates of countries (adm0_a3) are automatically set
    if sel_country and sel_country != 'Worldwide':
        sel_region = data['infections'].loc[(data['infections']['len_states']>1) & (data['infections']['Country/Region'].str.contains(sel_country)),'adm0_a3'].unique()[0]

    # 2) Choose a statistics
    st.sidebar.markdown('Choose a Statistics (e.g., Changes (Daily))')

    stat_text = sorted(set(val[1] for val in read_columns['infections'].values()))
    stat_text = [None] + stat_text[:]

    # chosen_stat = {'infections':[],'vaccines':[]}
    chosen_stat = {'infections':[]}
    chosen_stat_text = st.sidebar.selectbox('Statistics',stat_text)

    if chosen_stat_text:
        for key in chosen_stat:
            chosen_stat[key] = sorted([val[0] for val in read_columns[key].values() if val[1] in chosen_stat_text])
            # iTot
            if not sel_region:
                chosen_stat[key] = [val for val in chosen_stat[key] if 'Tot' in val]
            elif key == 'infections':
                chosen_stat[key] = [val for val in chosen_stat[key] if 'Tot' not in val]


    # chosen_stat = {}
    # if chosen_stat_text:
    #     for key in chosen_stat_key:
    #         chosen_stat[key] = chosen_stat_text

    # 3) Draw map
    sel_map = None
    if chosen_stat:
        st.sidebar.markdown('Draw a map?')
        sel_map = st.sidebar.checkbox('Definitely')

    return sel_region, sel_country, chosen_stat, sel_map

# Print latest global status
def show_stats(data,sel_region,sel_country,chosen_stat,candidates,map=None):
    date = max([max(data[key]['Date']) for key in data.keys()])
    st.header('Summary statistics')

    if not sel_region:
        st.subheader('Global status as of ' + date.strftime('%m/%d/%y'))

        infections = f"\n* Cumulative infections:  `{data['infections'][data['infections']['Date']==date].groupby(['adm0_a3','Country/Region'])['Tot_confirmed'].max().sum():,}`"
        infections += f"\n* Cumulative casualties: `{data['infections'][data['infections']['Date']==date].groupby(['adm0_a3','Country/Region'])['Tot_deaths'].max().sum():,}`"
        infections += f"\n* Daily infections changes: `{data['infections'][data['infections']['Date']==date].groupby(['adm0_a3','Country/Region'])['iTot_confirmed'].max().sum():,}`"
        infections += f"\n* Daily casualties changes: `{data['infections'][data['infections']['Date']==date].groupby(['adm0_a3','Country/Region'])['iTot_deaths'].max().sum():,}`"
        st.write('***Infections*** '+infections)

        # vaccinations = f"\n* Cumulative administed doses:  `{data['vaccines'][data['vaccines']['Date']==date].groupby(['adm0_a3','Country/Region'])['Tot_admin'].max().sum():,}`"
        # vaccinations += f"\n* Cumulative fully vaccinations: `{data['vaccines'][data['vaccines']['Date']==date].groupby(['adm0_a3','Country/Region'])['Tot_full'].max().sum():,}`"
        # vaccinations += f"\n* Daily administed doses changes: `{data['vaccines'][data['vaccines']['Date']==date].groupby(['adm0_a3','Country/Region'])['iTot_admin'].max().sum():,}`"
        # vaccinations += f"\n* Daily fully vaccinations changes: `{data['vaccines'][data['vaccines']['Date']==date].groupby(['adm0_a3','Country/Region'])['iTot_full'].max().sum():,}`"
        # st.write('***Vaccinations*** '+vaccinations)

    else:
        st.subheader(sel_country + ' status as of ' + date.strftime('%m/%d/%y'))

        infections = f"\n* Cumulative infections:  `{data['infections'][(data['infections']['Date']==date) & (data['infections']['adm0_a3']==sel_region) & (data['infections']['Country/Region']==sel_country)].groupby(['adm0_a3','Country/Region'])['Tot_confirmed'].max().sum():,}`"
        infections += f"\n* Cumulative casualties: `{data['infections'][(data['infections']['Date']==date) & (data['infections']['adm0_a3']==sel_region) & (data['infections']['Country/Region']==sel_country)].groupby(['adm0_a3','Country/Region'])['Tot_deaths'].max().sum():,}`"
        infections += f"\n* Daily infections changes: `{data['infections'][(data['infections']['Date']==date) & (data['infections']['adm0_a3']==sel_region) & (data['infections']['Country/Region']==sel_country)].groupby(['adm0_a3','Country/Region'])['iTot_confirmed'].max().sum():,}`"
        infections += f"\n* Daily casualties changes: `{data['infections'][(data['infections']['Date']==date) & (data['infections']['adm0_a3']==sel_region) & (data['infections']['Country/Region']==sel_country)].groupby(['adm0_a3','Country/Region'])['iTot_deaths'].max().sum():,}`"
        st.write('***Infections*** '+infections)

        # vaccinations = f"\n* Cumulative administed doses:  `{data['vaccines'][(data['vaccines']['Date']==date) & (data['vaccines']['adm0_a3']==sel_region) & (data['vaccines']['Country/Region']==sel_country)].groupby(['adm0_a3','Country/Region'])['Tot_admin'].max().sum():,}`"
        # vaccinations += f"\n* Cumulative fully vaccinations: `{data['vaccines'][(data['vaccines']['Date']==date) & (data['vaccines']['adm0_a3']==sel_region) & (data['vaccines']['Country/Region']==sel_country)].groupby(['adm0_a3','Country/Region'])['Tot_full'].max().sum():,}`"
        # vaccinations += f"\n* Daily administed doses changes: `{data['vaccines'][(data['vaccines']['Date']==date) & (data['vaccines']['adm0_a3']==sel_region) & (data['vaccines']['Country/Region']==sel_country)].groupby(['adm0_a3','Country/Region'])['iTot_admin'].max().sum():,}`"
        # vaccinations += f"\n* Daily fully vaccinations changes: `{data['vaccines'][(data['vaccines']['Date']==date) & (data['vaccines']['adm0_a3']==sel_region) & (data['vaccines']['Country/Region']==sel_country)].groupby(['adm0_a3','Country/Region'])['iTot_full'].max().sum():,}`"
        # st.write('***Vaccinations*** '+vaccinations)

    show_chart(data,chosen_stat,candidates,sel_region)

    if map and chosen_stat:
        show_map(data,chosen_stat,sel_region)

# Load mapdata for selected region
def show_map(data,stat,region=None,date=None):
    st.header('Color maps')

    if not date:
        date = max([max(data[key]['Date']) for key in data.keys()])

    # Custom color scale (colorbrewer2.org -> Sequential Single-Hue)
    breaks = [.0, .2, .4, .6, .8, 1]
    color_range = [
        # 6-class Blues
        [255,255,255],
        [198,219,239],
        [158,202,225],
        [107,174,214],
        [49,130,189],
        [8,81,156],

        # # 6-class Purples (For reference)
        # [242,240,247],
        # [218,218,235],
        # [188,189,220],
        # [158,154,200],
        # [117,107,177],
        # [84,39,143],
    ]

    def color_scale(val):
        for i, b in enumerate(breaks):
            if val <= b:
                return color_range[i]
        return color_range[i]

    def elevation_scale(val,scale):
        for i, b in enumerate(breaks):
            if val <= b:
                return i*scale

    def set_nan(val):
        if np.isnan(val):
            return -1
        else:
            return val

    stat_text = {'infections':['Infections','Casualties'],'vaccines':['Administered','Fully Vaccinated']}

    for key, stat_key in stat.items():
        if key == 'infections':
            st.subheader('Infections')
        elif key == 'vaccines':
            st.subheader('Vaccines')

        st.write(f'* Color depths: {stat_text[key][0]} \n* Elevation: {stat_text[key][1]}')
        stat_tot = sum(['Tot' in stat_keys for stat_keys in stat_key])

        # Load in the JSON data
        if region and region != 'Worldwide' and stat_tot == 0:
            src_geo = 'data/geojson/'+region+'.json'
        else:
            src_geo = 'data/geojson/countries.json'

        json_geo = pd.read_json(src_geo)
        df = pd.DataFrame()

        # Parse the geometry out in Pandas
        df["coordinates"] = json_geo["features"].apply(lambda row: row["geometry"]["coordinates"])
        df["name"] = json_geo["features"].apply(lambda row: row["properties"]["name"])
        df["adm0_a3"] = json_geo["features"].apply(lambda row: row["properties"]["adm0_a3"])
        df["admin"] = json_geo["features"].apply(lambda row: row["properties"]["admin"])

        df['param'] = f"{str.title(key)} {sorted(set(val[1] for val in read_columns[key].values() if val[0] in stat_key))[0]}"
        df['stat_text0'] = stat_text[key][0]
        df['stat_text1'] = stat_text[key][1]

        stat_key = [stat_keys[1:] if stat_keys[0]=='r' else stat_keys for stat_keys in stat_key]
        filtered_data = data[key].loc[data[key]['Date']==date,['adm0_a3','Province/State','lat','lon']+stat_key]


        if not region or region == 'Worldwide' or stat_tot>0:
            filtered_data = filtered_data.groupby(['adm0_a3'])[['lat','lon']+stat_key].mean()
            df = pd.merge(df,filtered_data,how='inner',left_on=['adm0_a3'],right_on=['adm0_a3'])
            df['name'] = 'N/A'
            if region and region != 'Worldwide':
                zoom = 3
            else:
                zoom = 1
        else:
            filtered_data = filtered_data.loc[filtered_data['adm0_a3']==region,['adm0_a3','Province/State','lat','lon']+stat_key]
            df = pd.merge(df,filtered_data,how='inner',left_on=['name','adm0_a3'],right_on=['Province/State','adm0_a3'])
            zoom = 3

        # Moved to generic.py
        # df.loc[df[stat_keys[0]]<0,stat_keys[0]] = 0
        # df.loc[df[stat_keys[1]]<0,stat_keys[1]] = 0
        # df[stat_keys[0]] = df[stat_keys[0]].apply(set_nan)
        # df[stat_keys[1]] = df[stat_keys[1]].apply(set_nan)


        df['fill_color'] = (df[stat_key[0]]/df[stat_key[0]].max()).replace(np.nan,0).apply(color_scale)
        df['elevation'] = (df[stat_key[1]]/df[stat_key[1]].max()).replace(np.nan,0).apply(lambda x:elevation_scale(x,1e4))

        df.rename(columns={stat_key[0]:'stat_0',stat_key[1]:'stat_1'},inplace=True)

        if not region or region == 'Worldwide':
            lat = df.loc[(df['lat'] != 0) & (df['lon'] != 0),'lat'].mean(skipna=True)
            lon = df.loc[(df['lat'] != 0) & (df['lon'] != 0),'lon'].mean(skipna=True)
        else:
            lat = df.loc[(df['adm0_a3']==region) & (df['lat'] != 0) & (df['lon'] != 0),'lat'].mean(skipna=True)
            lon = df.loc[(df['adm0_a3']==region) & (df['lat'] != 0) & (df['lon'] != 0),'lon'].mean(skipna=True)

        view_state = pdk.ViewState(
            latitude = lat, #df.loc[(df['lat'] != 0) & (df['lon'] != 0),'lat'].mean(skipna=True),
            longitude = lon, #df.loc[(df['lat'] != 0) & (df['lon'] != 0),'lon'].mean(skipna=True),
            # bearings=15,
            # pitch=45,
            zoom=zoom)

        polygon_layer = pdk.Layer(
            "PolygonLayer",
            df,
            id="geojson",
            opacity=0.2,
            stroked=False,
            get_polygon="coordinates",
            filled=True,
            get_elevation='elevation',
            # elevation_scale=1e5,
            # elevation_range=[0,100],
            extruded=True,
            # wireframe=True,
            get_fill_color= 'fill_color',
            get_line_color=[255, 255, 255],
            auto_highlight=True,
            pickable=True,
        )


        tooltip = {"html": "<b>Country/Region:</b> {admin} <br /><b>Province/State:</b> {name} <br /><b>Type:</b> {param}<br /><b>{stat_text0}:</b> {stat_0} <br /><b>{stat_text1}:</b> {stat_1}"}

        r = pdk.Deck(
            layers=[polygon_layer],
            initial_view_state=view_state,
            map_style='light',
            tooltip=tooltip,
            )

        # return r
        st.pydeck_chart(r, use_container_width=True)


def show_chart(data,stat,candidates,region,date=None):
    if not date:
        date = min([min(data[key]['Date']) for key in data.keys()])
    dataset = []

    # Set quantiles for x-axis ('Date')
    # dates = data['Date'].map(lambda x:x.strftime('%m/%d/%y')).unique().tolist()
    dates = data['infections']['Date'].map(lambda x:x.strftime('%m/%d/%y')).unique().tolist()
    presets = [0,.25,.5,.75,1]
    quantiles = np.quantile(np.arange(0,len(dates)),presets).tolist()
    quantiles = [int(np.floor(q)) for q in quantiles]
    date_visible = [dates[idx] for idx in quantiles]

    stat_len = min([len(val) for val in stat.values()])

    if stat_len > 0:
        st.header('Regional analyses')
        for key, stat_key in stat.items():
            dataset.append(data[key].loc[(data[key]['Date']>=date),['Date','adm0_a3','Country/Region','Province/State']+stat_key])

        for idx, key in enumerate(stat):
            if idx == 0:
                st.subheader('Infections developments')
            else:
                st.subheader('Vaccines developments *(Per 100K population)*')

            stat_text = {'infections':['Infections','Casualties'],'vaccines':['Administered','Fully Vaccinated']}

            for stat_idx, stat_key in enumerate(stat[key]):

                if region and 'Tot' not in stat_key:
                        filtered_data = pd.merge(dataset[idx][['Date','Province/State',stat_key]],candidates[['index',stat_key]],how='inner',left_on='Province/State',right_on=stat_key)
                        filtered_data.drop([stat_key+'_y'],axis=1,inplace=True)
                        filtered_data.rename(columns={stat_key+'_x':stat_key,'index':'order'},inplace=True)

                        filtered_data['Date'] = filtered_data['Date'].map(lambda x:x.strftime('%m/%d/%y'))

                        target_cat = 'Province/State'
                else:
                    if stat_key in candidates.columns.tolist():
                        filtered_data = pd.merge(dataset[idx][['Date','adm0_a3','Country/Region',stat_key]],candidates[['index',stat_key]],how='inner',left_on='adm0_a3',right_on=stat_key)
                        filtered_data.drop([stat_key+'_y'],axis=1,inplace=True)
                        filtered_data.rename(columns={stat_key+'_x':stat_key,'index':'order'},inplace=True)
                        filtered_data['Date'] = filtered_data['Date'].map(lambda x:x.strftime('%m/%d/%y'))

                    elif region:
                        if stat_idx == 0:
                            filtered_data = dataset[idx].loc[dataset[idx]['adm0_a3']==region,['Date','adm0_a3','Country/Region',stat_key]]
                        else:
                            filtered_data = pd.merge(filtered_data, dataset[idx].loc[dataset[idx]['adm0_a3']==region,['Date','adm0_a3','Country/Region',stat_key]],how='inner',on=['Date','adm0_a3','Country/Region'])
                            filtered_data['Date'] = filtered_data['Date'].map(lambda x:x.strftime('%m/%d/%y'))

                        filtered_data[stat_text[key][stat_idx]] = filtered_data[stat_key]

                    target_cat = 'Country/Region'


                # try:
                if stat_key[0] == 'r':
                    tooltip_format = ',.2f'
                else:
                    tooltip_format = ','

                if sum(filtered_data[stat_key]) != 0:
                    if stat_key in candidates.columns.tolist():
                        heatmap = alt.Chart(filtered_data).mark_rect().encode(
                                x=alt.X('Date:O', sort=dates, axis=alt.Axis(values=date_visible,labelAngle=0)),
                                y=alt.Y(target_cat, sort=alt.EncodingSortField(field='order',order='ascending')),
                                color=alt.Color(stat_key,scale=alt.Scale(scheme='blues'),title=stat_text[key][stat_idx]),
                                tooltip=['Date:O',target_cat,alt.Tooltip(stat_key,title=stat_text[key][stat_idx],format=tooltip_format)]
                                ).configure_scale(
                                    bandPaddingInner=.1
                                    )
                        stacked = heatmap

                    elif stat_idx > 0:
                        bar = alt.Chart(filtered_data).transform_fold(
                            stat_text[key],['Types','Vaccinations']).mark_bar().encode(
                            x=alt.X('Date:O', sort=dates, axis=alt.Axis(values=date_visible,labelAngle=0)),
                            # y=alt.Y(target_cat, sort=alt.EncodingSortField(field='order',order='ascending')),
                            y=alt.Y('Vaccinations:Q', sort=alt.EncodingSortField(field='order',order='ascending')),
                            color=alt.Color('Types:N',scale=alt.Scale(scheme='blues')),
                            tooltip=['Date:O',target_cat,'Types:O',alt.Tooltip('Vaccinations:Q',format=tooltip_format)]
                                )
                                # .configure_scale(
                                #     bandPaddingInner=.1
                                #     )


                        stacked = bar

                    else:
                        continue

                    st.altair_chart(stacked,use_container_width=True)

                # except:
                #     pass
