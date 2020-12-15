# NOTES

## Features to implement

- Check sentiment of particular topic over time period (1 year intervals, avg sentiment of 50 pages of article every month for 12 months)
- Check sentiment on particular month
- output a matplotlib graph
- Allow for comparison of topic sentiments, graph on same plot.

## Functions to implement

- Create csv file with choosen topic and sentiments added, accepts a topic, date period and pages, returns a dataframe
  - Accepts topic, start month , start year, end month, end year, page
  - Creates a dataframe with sentiment,choosen topic, selected year and month for start month period, 50 pages
  - for each subsequent month after, do the same thing as before, adding on to the dataframe and csv

- Adds to and updates dataframe when given a topic, date period and pages. updates the ouptcsv file.
  - Accepts a dataframe, topic, start month, end month, start year, end year and pages. Returns an updated dataframe

- Creates a plot with x axis as date and y axis as sentiment, for each topic on csv.
  - Accepts a dataframe and creates a graph on same plot for each topic (different color for different topic)
  - if one month only, create bar chart. x axis topic, y axis sentiment
  - if more than one month, create line graph. x axis date, y axis sentiment, label topic with legend.