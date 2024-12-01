library(dplyr)
library(reshape2)
library(tidyr)
library(stringr)
library(readr)

inputpath <- "/Users/bryan/Documents/Puzzles/Advent 2021/day01/input.txt"

# Parse
depths <- read_file(inputpath) %>%
  strsplit('\n\n') %>% unlist()