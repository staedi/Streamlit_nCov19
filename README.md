# Streamlit_nCov19
Interactive Dashboard of Novel COVID-19 employing [Streamlit](https://www.streamlit.io) module.
You can try [here](https://share.streamlit.io/staedi/streamlit_ncov19/app.py).

## Primary objectives
* Basic options for users to choose
  * Cumulative or daily changes measures
  * Global aggregate stat or per-country information
* Display a basic statistics for selected area (Global or for specific country)
* Draw a heatmap detailing given a region and measure (e.g., Daily infections increases in the US)
* Draw a Choropleth with the same selection (Country-level or state-level comparisons)

## Data sources and helpful resources
* Data sources
  * [Johns Hopkins University Github](https://github.com/CSSEGISandData/COVID-19): Global nCov-19 dataset
  * [KCDC](http://ncov.mohw.go.kr/): South Korean dataset providing provincial-level details
  * [NaturalEarth](http://naturalearthdata.com/): Geographical shapedata for countries (admin0) and states-level (admin1) data to be used (1:10m data is used for selected countries for states details while 1:50m used for others)
* Useful resources
  * [polygon conversion](https://gist.github.com/mapmeld/8742ae89c6d687171d00/): To convert `MultiPolygon` geojson to `Polygon` form (Nick Doiron)
  * [simplify](https://philmikejones.me/tutorials/2016-09-29-simplify-polygons-without-creating-slivers/): Using rmapshaper::simplify() in R to greatly reduce file sizes (Phil Mickey Johns)
  * [dissolve](https://philmikejones.me/tutorials/2015-09-03-dissolve-polygons-in-r//): Merge small-scale districts into larger level ones (e.g., counties -> states) (Phil Mickey Johns)

## Descriptions of objects
* Heatmap
  * Two separate charts are drawn, one for infections and the other for casaulties
  * Regions on y-axis are pre-sorted by the figures (ordered in a descending manner for top-25 disricts)
* Choropleth
  * Both measures are drawn on a single choropleth (casualties on top of infections)
  * Infections are shown by the color depth while casualties are represented by elevations of the regions
  
## Selected modules used
  * [Altair](http://altair-viz.github.io/): Altair chart module used to draw heatmap (`streamlit.altair_chart`)
  * [Pydeck](http://pydeck.gl/): Pydeck mapping module used to draw Choropleth/PolygonLayer (`streamlit.pydeck_chart`)
  
## Snapshots
### Main Landing Page
![main](https://github.com/staedi/Streamlit_nCov19/raw/master/samples/main.png)

### Heatmap
![US_heatmap](https://github.com/staedi/Streamlit_nCov19/raw/master/samples/US.png)

### Map
![US](https://github.com/staedi/Streamlit_nCov19/raw/master/samples/US_map.png)
