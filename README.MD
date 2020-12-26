# GoogleNews Sentiment Analysis with Vader

## Summary

This project is intended to be a web app that analyses and compares the sentiment of Google News headlines based on user-defined topics and date period in MM/YYYY format. For example, given the topic 'Trump' and 'Biden' and the dates 01/2020 - 01/2021, the webapp calculates the averages sentiment of GoogleNews headlines in each month and ouputs a graph along with CSV data generated per month per topic.

The aim is to capture and compare the perception of certain topics by mainstream media over a cetain time through an easy-to-use and accessible online application.

## Limitations

Currently however, this currently incomplete project has 2 major limitations:

- **Non-functioning server**: This project uses a flask server which was intended to be deployed online on a Platform as a Service (PaaS) like Heroku. However, because of the long time required for web scapping, background jobs and queueing operations using libraries like Redis Queue are required. As such operations are beyond my capabilities at the moment, this application will have to be used offline.

- **Imprecision of Sentiment Analysis for intended purpose**: The current program does not contextualise when given a topic. For example, when searching Google News for the topic of 'AMD', a headline such as 'Leaks Suggests AMD will destroy Intel in Performance' would be preceived as negative although the opposite is true in context. Additionally, some Vader Sentiment is sometimes unable to guage the polarity of certain headlines. Such results are excluded in the computation of the mean monthly polarity, hence decreasing sample size.

## Setup and Usage

- To do

## Sample Outputs

### Coronavirus Nov 2019 - Dec 2020

Webapp Screenshot for Coronavirus
![Webapp Screenshot for Coronavirus](WebappScreenshot.JPG)

Coronavirus Graph
![Coronavirus Graph](outputs\11_2019-1_2021_Coronavirus\outputGraph.jpg)

### AMD vs Intel vs Nvidia from Jan 2020 - Dec 2020

AMD Intel Nvidia Graph
![AMD Intel Nvidia Graph](outputs\1_2020-1_2021_Intel+AMD+Nvidia\outputGraph.jpg)

Below is a small sample of the batch data used for calulating the average sentiment of the topic 'AMD' on November 2020 (Last column is used for caluating mean, with 0 values ignored in its computation)
![AMD Batch Data](SampleAMDBatchData.JPG)

### Biden vs Trump Jan 2018 - Dec 2020

![Biden Trump Graph](outputs\1_2018-1_2021_Biden+Trump\outputGraph.jpg)

## Future Plans

The hope is to deploy a scalable version of this application online, instead of being limited to running it locally. 