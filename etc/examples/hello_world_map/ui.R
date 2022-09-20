library(shiny)
library(leaflet)

# ui <- fillPage(
#    tags$style(type = "text/css", "html, body {width:100%; height:100%}"),
#    leafletOutput("map", width = "100%", height = "100%"),
# )




ui <- navbarPage(
  title = 'Example',

  tabPanel(
    "Summary",
    leafletOutput("map", width = "100%", height = "100%"),
  ),
  tabPanel(
    "Summary",
    leafletOutput("map", width = "100%", height = "100%"),
  )
)