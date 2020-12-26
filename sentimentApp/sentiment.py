from GoogleNews import GoogleNews
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from shutil import make_archive
import pandas as pd
import matplotlib.pyplot as plt
#import matplotlib.colors as mcolors
import datetime
import sys
import os

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
'''
def gNewsTest(topic, startDate, endDate, pages = 1):
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
    df.to_csv("testOutput.csv",index=False)
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
    print(output)
    googlenews.clear()

'''

# Date function from https://stackoverflow.com/questions/42950/how-to-get-the-last-day-of-the-month



def last_day_of_month(any_day):
    # this will never fail
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
    return next_month - datetime.timedelta(days=next_month.day)

analyzer = SentimentIntensityAnalyzer()
# Eg input: createSentimentList("Trump",9,2019,4,2020)
#Topic accepts string, rest of inputs are integers. pages will multiply input int by 10
def createSentimentList(topic, startMonth ,startYear ,endMonth , endYear, dirName=None,inputSentimentList = None,pages = 5):
    print("Running createSentimentList function")
    if (not inputSentimentList):
        print("Initialising empty output list")
        output = []
    else:
        print("Initialising exisiting list as output list")
        output = inputSentimentList
    
    monthsInYear = 12
    monthCount = (endYear - startYear)*monthsInYear + (endMonth - startMonth)
    print(f"Number of months (batches):{monthCount}")
    for i in range(monthCount):
        batch = []
        #Prepare start date and end date
        inputMonth = 12 if (startMonth + i)%12 == 0 else (startMonth + i)%12
        inputYear = (startYear + (startMonth + i)//12) - 1 if inputMonth == 12 else (startYear + (startMonth + i)//12)
        print(f"Loop:{i+1}, Month: {inputMonth}, Year:{inputYear}")
        startDate = datetime.datetime(inputYear,inputMonth,1)
        endDate = last_day_of_month(startDate)
        #endDate = datetime.datetime(inputYear,inputMonth,last_day_of_month(startDate.strftime('%s')))
        startDateStr = startDate.strftime("%m/%d/%Y")
        endDateStr = endDate.strftime("%m/%d/%Y")
        print(f"Date range: {startDateStr} - {endDateStr}")

        #Create GoogleNews Object
        googlenews = GoogleNews(lang='en',start=startDateStr,end=endDateStr,encode='utf-8')
        print(f"searching the topic '{topic}' on google from {startDateStr} - {endDateStr}...")
        googlenews.search(topic)

        #get_page(1) is called by default.
        #Iterate here for number of pages
        print("retrieved page 1")
        for i in range(pages-1):
            googlenews.get_page(i+2)
            print (f"retrieved page {i+2}")

        totalPolarity = 0
        totalSubjectivity = 0
        adjustedPolarity = 0
        adjustedSubjectivity = 0
        vaderPolarity = 0
        adjustedVaderPolarity = 0
        textBlobAdjustedLength = 0
        vaderAdjustedLength = 0
        
        for newsDict in googlenews.result(sort=True):
            opinion = TextBlob(newsDict["title"]).sentiment
            vaderOpinion = analyzer.polarity_scores(newsDict["title"])['compound']
            newsDict["textBlob polarity"] = opinion.polarity
            newsDict["textBlob subjectivity"] = opinion.subjectivity
            newsDict["vader polarity"] = vaderOpinion
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
            batch.append(newsDict)
            
        batchName = f"{inputMonth}_{inputYear}_{topic}"
        df=pd.DataFrame(batch)
        df.to_csv(f"outputs/{dirName}/batches/{batchName}.csv",index=False)
        print(f"Created outputs/{dirName}/batches/{batchName}NewsBatch.csv")
        batchLength = len(batch)

        meanPolarity = totalPolarity/batchLength
        meanSubjectivity = totalSubjectivity/batchLength
        meanAdjustedPolarity = adjustedPolarity/textBlobAdjustedLength
        meanAdjustedSubjectivity = adjustedSubjectivity/textBlobAdjustedLength
        meanVaderPolarity = vaderPolarity/batchLength
        meanAdjustedVaderPolarity = adjustedVaderPolarity/vaderAdjustedLength

        batchData = {}
        batchData['month'] = inputMonth
        batchData['year'] = inputYear
        batchData['topic'] = topic
        batchData['batchLength'] = batchLength
        batchData['textBlobAdjustedLength'] = textBlobAdjustedLength
        batchData['vaderAdjustedLength'] = vaderAdjustedLength
        batchData['meanPolarity'] = meanPolarity
        batchData['meanSubjectivity'] = meanSubjectivity
        batchData['meanAdjustedPolarity'] = meanAdjustedPolarity
        batchData['meanAdjustedSubjectivity'] = meanAdjustedSubjectivity
        batchData['meanVaderPolarity'] = meanVaderPolarity
        batchData['meanAdjustedVaderPolarity'] = meanAdjustedVaderPolarity
        #print(batchData)
        
        output.append(batchData)
    return output



def createGraphFromList(inputDF,saveName="output.jpg"):
    topicList = []
    for topic in inputDF['topic']:
        #print(topic)
        if topic not in topicList:
            topicList.append(topic)
    df=inputDF
    # code from https://stackoverflow.com/questions/53259415/month-year-with-value-plot-pandas-and-matplotlib
    #print(topicList)
    df['date'] = df['month'].map(str)+ '-' +df['year'].map(str)
    df['date'] = pd.to_datetime(df['date'], format='%m-%Y').dt.strftime('%m-%Y')
    
    fig, ax = plt.subplots(figsize=(16,9))
    #plt.figure(figsize=(11,5))
    for topic in topicList:
        dfByTopic = df[df['topic']==topic]
        plt.plot_date(dfByTopic['date'], dfByTopic['meanAdjustedVaderPolarity'],label=topic,linestyle='-')
        ax.legend()
        #print(dfByTopic.head())
    fig.suptitle('Average Adjusted Sentiment of Topic in Google News per month',fontsize=20)
    plt.xlabel('Date (MM/YYYY)',fontsize=18)
    plt.ylabel('Adjusted Vader Sentiment',fontsize=20)
    fig.savefig(saveName)
    #plt.show()



'''
 testList2 = createSentimentList("Amazon",1,2020,1,2021,testList,pages=3)
testList3 = createSentimentList("Google",1,2020,1,2021,testList2,pages=3)
testList4 = createSentimentList("Apple",1,2020,1,2021,testList3,pages=3)
testList4 = createSentimentList("Microsoft",1,2020,1,2021,testList3,pages=3)
testList5 = createSentimentList("Alibaba",1,2020,1,2021,testList4,pages=3)
testList6 = createSentimentList("Tencent",1,2020,1,2021,testList5,pages=3)
'''

def chainSentimentList(topicLists,startMonth,startYear,endMonth,endYear,pages=5):
    output = []
    topicString = '+'.join(topicLists)
    dirName = f"{startMonth}_{startYear}-{endMonth}_{endYear}_{topicString}"
    if not os.path.exists(f"outputs"):
        os.mkdir(f"outputs")
    if not os.path.exists(f"zips"):
        os.mkdir(f"zips")
    if not os.path.exists(f"outputs/{dirName}"):
        os.mkdir(f"outputs/{dirName}")
        os.mkdir(f"outputs/{dirName}/batches")
        print(f"created outputs/{dirName} directory")
    else:
        print(f"outputs/{dirName} directory already exists")
    
    for topic in topicLists:
        output = createSentimentList(topic,startMonth,startYear,endMonth,endYear,dirName=dirName,inputSentimentList=output,pages=pages)

    df=pd.DataFrame(output)
    df.to_csv(f"outputs/{dirName}/aggregatedData.csv",index=False)
    inputDf = pd.read_csv(f"outputs/{dirName}/aggregatedData.csv")
    createGraphFromList(inputDf,saveName=f"outputs/{dirName}/outputGraph.jpg")
    make_archive(f"zips/{dirName}", 'zip', f"outputs/{dirName}")

    #return output

# testList = createSentimentList("Vaccine",1,2020,1,2021,pages=5)
testCLIInput = ""
def parseCLIInputs(inputArgs):
    output = []
    print(inputArgs)
    topicArgs = inputArgs[5:]
    for arg in topicArgs:
        output.append(arg)
    return (output,int(inputArgs[1]),int(inputArgs[2]),int(inputArgs[3]),int(inputArgs[4]))



'''
topicList = ['Apple','Samsung','Sony']
startMonth = 1
startYear = 2020
endMonth = 2
endYear = 2020
'''


'''
formattedArgs = parseCLIInputs(sys.argv)
topicList = formattedArgs[0]
startMonth = formattedArgs[1]
startYear = formattedArgs[2]
endMonth = formattedArgs[3]
endYear = formattedArgs[4]
chainSentimentList(topicList,startMonth,startYear,endMonth,endYear)
'''
