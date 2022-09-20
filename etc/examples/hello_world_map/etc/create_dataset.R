library(tidycensus)
library(shiny)
library(leaflet)
library(tidyverse)
library(sf)
library(data.table)
library(dplyr)
library(tidyr)
# library(plyr)

# read sa2 geographic data
sa2_file <- "/home/szhang/Gitlab/shiny_app/r/hello_world_map/etc/statistical-area-2-2022-north-island.csv"
sa2_data <- fread(sa2_file, select = c("WKT", "SA22022_V1_00", "SA22022_V1_00_NAME"))
sa2_data <- sa2_data[!grepl("Oceanic", sa2_data$SA22022_V1_00_NAME), ]

# read hh data
hh_file <- "/home/szhang/Gitlab/shiny_app/r/hello_world_map/etc/syn_hh.csv"
hh_data <- fread(hh_file)

# read hh income data
income_file <- "/home/szhang/Gitlab/shiny_app/r/hello_world_map/etc/hhincome.csv"
income_data <- fread(income_file)
income_data <- income_data[-1, ] %>%
  separate(V2, c("na", "hh_key"), "-")
income_data <- subset(income_data, select = c(hh_key, V3))
income_data <- income_data %>% rename(income = V3)
income_data$hh_key <- as.numeric(income_data$hh_key)

# map hh to income data
setkey(income_data, hh_key)
setkey(hh_data, hh_id)
joint_data <- hh_data[income_data, ]
joint_data <- na.omit(joint_data)

# apply value to income threshold
joint_data$income <- recode(joint_data$income, "low" = "1", "medium" = "2", "high" = "3")
joint_data$income <- as.numeric(joint_data$income)

joint_data_mean <- aggregate(income ~ SA22018, joint_data, mean)
joint_data_mean <- na.omit(joint_data_mean)
joint_data_mean <- joint_data_mean %>% rename(mean = income)

joint_data_max <- aggregate(income ~ SA22018, joint_data, max)
joint_data_max <- na.omit(joint_data_max)
joint_data_max <- joint_data_max %>% rename(max = income)


joint_data_min <- aggregate(income ~ SA22018, joint_data, min)
joint_data_min <- na.omit(joint_data_min)
joint_data_min <- joint_data_min %>% rename(min = income)


joint_data <- cbind(joint_data_mean, joint_data_max$max, joint_data_min$min)

## map sa2 WKT to joint data
setkey(sa2_data, SA22022_V1_00)
joint_data2 <- sa2_data[joint_data, ]
joint_data2 <- na.omit(joint_data2)

joint_data2 <- st_as_sf(joint_data2, wkt = "WKT")

# save output
saveRDS(joint_data2, file = "/home/szhang/Gitlab/shiny_app/r/hello_world_map/etc/income.rds")

# we need to upload the data to S3
# cmd <- "aws s3 cp /home/szhang/Gitlab/shiny_app/r/hello_world_map/etc/income.rds s3://mot-shiny-app/etc/tmp/hello_world_map/income.rds"
# system(cmd, TRUE)
