# Streamlit_nCovid19
Interactive Dashboard of nCovid19 employing Streamlit module

This module aimed to build an interactive web dashboard depicting nCovid-19 using [Streamlit](https://www.streamlit.io).

## Primary objectives
* Basic options for users to choose
  * Cumulative or daily changes measures
  * Global aggregate stat or per-country information
* Display a basic statistics for selected area (Global or for specific country)
* Draw a heatmap detailing given a region and measure (e.g., Daily infections increases in the US)
* Draw a Choropleth with the same selection (Country-level or state-level comparisons)

## Data sources
* Infections data
  * [Johns Hopkins University Github](https://github.com/CSSEGISandData/COVID-19): Global dataset
  * [KCDC](http://ncov.mohw.go.kr/): South Korean data with provincial-level details
* Geographical data
  * [Naturalearth](http://naturalearthdata.com/): Country (admin0) and state (admin1) data used (1:10m data is used for states data of non-American continent while 1:50m for others)
  * [mapmeld](https://gist.github.com/mapmeld/8742ae89c6d687171d00/): To convert `MultiPolygon` geojson to `Polygon` form
  * [simplify](https://philmikejones.me/tutorials/2016-09-29-simplify-polygons-without-creating-slivers/): Using rmapshaper::simplify() in R to greatly reduce file sizes (Phil Mickey Johns)
  * [dissolve](https://philmikejones.me/tutorials/2015-09-03-dissolve-polygons-in-r//): Merge small-scale districts into larger level ones (e.g., counties -> states) (Phil Mickey Johns)
 
## Selected modules used
  * [Altair](http://altair-viz.github.io/): Altair chart module used to draw heatmap (streamlit.altair_chart)
  * [Pydeck](http://pydeck.gl/): Pydeck mapping module used to draw Choropleth/PolygonLayer (streamlit.pydeck_chart)
