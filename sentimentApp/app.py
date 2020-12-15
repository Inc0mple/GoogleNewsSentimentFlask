from GoogleNews import GoogleNews
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import newspaper

"""
NOTES:

Features to implement:
-Check sentiment of particular topic over time period (1 year intervals, avg sentiment of 50 pages of article every month for 12 months)
-Check sentiment on particular month
-output a matplotlib graph
-Allow for comparison of topic sentiments, graph on same plot.

Functions to implement:
-Create csv file with choosen topic and sentiments added, accepts a topic, date period and pages, returns a dataframe
    -Accepts topic, start month , start year, end month, end year, page
    -Creates a dataframe with sentiment,choosen topic, selected year and month for start month period, 50 pages
    -for each subsequent month after, do the same thing as before, adding on to the dataframe and csv

-Adds to and updates dataframe when given a topic, date period and pages. updates the ouptcsv file.
    Accepts a dataframe, topic, start month, end month, start year, end year and pages. Returns an updated dataframe

-Creates a plot with x axis as date and y axis as sentiment, for each topic on csv.
    Accepts a dataframe and creates a graph on same plot for each topic (different color for different topic)
    if one month only, create bar chart. x axis topic, y axis sentiment
    if more than one month, create line graph. x axis date, y axis sentiment, label topic with legend.



"""


analyzer = SentimentIntensityAnalyzer()
def gNews(topic, startDate, endDate, pages = 1):
    output = []
    googlenews = GoogleNews(lang='en',start=startDate,end=endDate,encode='utf-8')
    print(f"searching the topic '{topic}' on google...")
    googlenews.search(topic)
    #get_page(1) is called by default.
    #Iterate here for number of pages
    print("retrieved page 1")
    for i in range(pages-1):
        googlenews.get_page(i+2)
        print (f"retrieved page {i+2}")


    for newsDict in googlenews.result(sort=True):
        output.append(newsDict)

    totalPolarity = 0
    totalSubjectivity = 0
    adjustedPolarity = 0
    adjustedSubjectivity = 0
    vaderPolarity = 0
    adjustedVaderPolarity = 0
    outputLength = len(output)
    textBlobAdjustedLength = 0
    vaderAdjustedLength = 0

    print("output length:", outputLength)
    #print (output[1]["desc"])
    #print (len(output[1]["desc"]))
    #print(googlenews.get_texts())
    for row in output:
        #print(row["desc"])
        opinion = TextBlob(row["title"]).sentiment
        vaderOpinion = analyzer.polarity_scores(row["title"])['compound']
        row["textBlob polarity"] = opinion.polarity
        row["textBlob subjectivity"] = opinion.subjectivity
        row["vader polarity"] = vaderOpinion
        vaderPolarity += vaderOpinion
        totalPolarity += opinion.polarity
        totalSubjectivity += opinion.subjectivity
        if opinion.polarity != 0:
            textBlobAdjustedLength += 1
            adjustedPolarity += opinion.polarity
            adjustedSubjectivity += opinion.subjectivity
        if vaderOpinion != 0:
            vaderAdjustedLength += 1
            adjustedVaderPolarity += vaderOpinion


    df=pd.DataFrame(output)
    df.to_csv("output.csv",index=False)
    print(df.head())
    print("Textblob adjusted output length:", textBlobAdjustedLength)
    print("Vader adjusted output length:", vaderAdjustedLength)
    meanPolarity = totalPolarity/outputLength
    meanSubjectivity = totalSubjectivity/outputLength
    meanAdjustedPolarity = adjustedPolarity/textBlobAdjustedLength
    meanAdjustedSubjectivity = adjustedSubjectivity/textBlobAdjustedLength
    meanVaderPolarity = vaderPolarity/outputLength
    meanAdjustedVaderPolarity = adjustedVaderPolarity/vaderAdjustedLength
    print(f"Textblob stats for '{topic}' topic on Google News from {startDate} - {endDate}:")
    print(f"\tMean polarity: {round(meanPolarity,3)}")
    print(f"\tMean subjectivity: {round(meanSubjectivity,3)}")
    print(f"\tAdjusted mean polarity: {round(meanAdjustedPolarity,3)}")
    print(f"\tAdjusted mean subjectivity: {round(meanAdjustedSubjectivity,3)}")
    print(f"Vader stats for '{topic}' topic on Google News from {startDate} - {endDate}:")
    print(f"\tMean vader polarity: {round(meanVaderPolarity,3)}")
    print(f"\tAdjusted mean vader polarity: {round(meanAdjustedVaderPolarity,3)}")
    googlenews.clear()

gNews("AMD","11/1/2020","12/1/2020",5)
#print(TextBlob("PHOTOS: Trump Supporters Rally In Washington To Oppose 2020 Election Results").sentiment.polarity)