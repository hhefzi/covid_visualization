#!/bin/bash

wget https://covid.ourworldindata.org/data/owid-covid-data.csv -O ./data/world.csv

wget https://covidtracking.com/api/v1/states/daily.csv -O ./data/states.csv

wget https://covidtracking.com/api/v1/us/daily.csv -O ./data/US.csv
