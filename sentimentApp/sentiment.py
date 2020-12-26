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
