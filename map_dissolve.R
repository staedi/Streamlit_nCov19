setwd('/Users/minpark/Documents/Streamlit/nCovid19/data')

library(dplyr)
filename <- 'CHN'
original <- geojsonio::geojson_sf(paste0(filename,'.json'))

dissolver <- function(original) {
  original$area <- sf::st_area(original)
  
  target <- original %>%
    dplyr::group_by(adm0_a3,geounit,admin) %>%
    dplyr::summarise(area = sum(area)) %>%
    dplyr::mutate(name = geounit) %>%
    dplyr::ungroup()
  return (target)
}

simplifier <- function(original) {
  target <- rmapshaper::ms_simplify(original,keep=.25)
  return (target)
}

operation <- function(original,mode) {
  if (mode == 0) {
    return (dissolver(original))
  }
  else {
    return (simplifier(original))
  }
}

target <- operation(original,1)
target_json <- geojsonsf::sf_geojson(target[c('name','adm0_a3','region','admin','geometry')])
write(target_json,paste0(filename,'.geojson'))
  