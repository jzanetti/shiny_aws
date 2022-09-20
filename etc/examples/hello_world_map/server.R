library(shiny)
library(leaflet)

df <- readRDS(file = "/home/szhang/Gitlab/shiny_app/r/hello_world_map/etc/income.rds")
# df <- readRDS(file = "/tmp/hello_world_map/income.rds")


colors <- c("red", "orange", "yellow", "green", "blue")
labels <- c("low", "", "medium", "", "high")
pal <- colorNumeric(colors, range(0, 3))

server <- function(input, output) {
    output$map <- renderLeaflet({
        leaflet(options = leafletOptions(zoomControl = FALSE)) %>%
            addProviderTiles(providers$Stamen.TonerLite) %>%
            setView(
                lng = 174.76,
                lat = -36.85,
                zoom = 8.0
            )
    })


    observeEvent(input, {
        leafletProxy("map") %>%
            clearShapes() %>%
            clearControls() %>%
            addPolygons(
                data = df,
                color = pal(df$mean),
                weight = 0.5,
                fillOpacity = 0.5,
                smoothFactor = 0.2
            ) %>%
            addLegend(
                position = "bottomright",
                colors = colors,
                labels = labels,
                values = range(0, 3),
                title = "household (SA2 averaged) income"
            )
    })
}
