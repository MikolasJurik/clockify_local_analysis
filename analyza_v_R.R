library(readr)
library(tidyverse)
library(stringr)
clocktify_export <- read.csv("clockify_export.csv")
britva <- select(clocktify_export, project_name, duration_hours)
britva$den <- as.Date(clocktify_export$start)

agregace <- britva |> group_by(project_name) |> summarize(celkem_hodin=sum(duration_hours,na.rm=TRUE)) |> 
  arrange(desc(celkem_hodin))

head(agregace,n=20)
