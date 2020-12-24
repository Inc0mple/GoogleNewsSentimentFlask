# NOTES

## Features to implement

- Check sentiment of particular topic over time period (1 year intervals, avg sentiment of 50 pages of article every month for 12 months)
- Check sentiment on particular month
- Check sentiment now or on particular day
- output a matplotlib graph
- Allow for comparison of topic sentiments, graph on same plot if given same time period

## Functions to implement

- Function that creates a dictionary with choosen topic and sentiments added, accepts a topic, date period and pages, returns a dictionary
  - Accepts topic, start month , start year, end month, end year, page
  - Creates a dataframe with sentiment,choosen topic, selected year and month for start month period, 50 pages
  - for each subsequent month after, do the same thing as before, adding on to the dataframe and csv

- Function that adds to and updates news dictionary when given a dictionary, topic, date period and pages.
  - Accepts a dictionary, topic, start month, end month, start year, end year and pages. Returns an updated dictionary

- Function that creates a CSV file from input dictionary

- Function that creates a plot with x axis as date and y axis as sentiment, for each topic on csv.
  - Accepts a dataframe and creates a graph on same plot for each topic (different color for different topic)
  - if one month only, create bar chart. x axis topic, y axis sentiment
  - if more than one month, create line graph. x axis date, y axis sentiment, label topic with legend 