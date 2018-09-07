import numpy as np
import sklearn
import nltk
import os
import math
from os import listdir
import gui
from tkinter import Tk
from tkinter.ttk import *

FILEPATH = os.path.dirname(os.path.abspath(__file__)) + "\\Source"

authors = []
corpora = {}
authAverageLength = {}
noSamples = {}
totalCorpus = []

#Classifier (Delta Method)
generated = False
featureList = []
freqVals = {}
featureVals = {}
knownZScores = {}

'''
#checkGenerated - getter method to check whether a classifier has been calculated yet
'''
def checkGenerated():
    return generated

'''
#identify - takes in a text file, and attributes it to an authors
     @filePath - path of .txt file
'''
def identify(filePath):
    print("ANALYSIS FOR " + filePath)
    sample = readFileAsString(filePath)
    tokens = nltk.word_tokenize(sample)
    refinedTokens = ([token for token in tokens if any(c.isalpha() for c in token)])

    count = len(refinedTokens)
    idFreqs = {}

    for f in featureList:
        idFreqs[f] = refinedTokens.count(f)/count

    testZs = {}
    for f in featureList:
        testZs[f] = (idFreqs[f]-featureVals[f]["Mean"]) / featureVals[f]["StdDev"]

    deltas = []
    lowestDelta = 100
    deltaAuth = ""
    nextLowestDelta = 0
    for auth in authors:
        delta = 0
        for f in featureList:
            delta += math.fabs((testZs[f] - knownZScores[auth][f]))

        delta = delta/len(featureList)
        deltas.append(delta)
        print("This samples Δ for " + auth + " is: " + str(delta))

        if(delta < lowestDelta):
            nextLowestDelta = lowestDelta
            lowestDelta = delta
            deltaAuth = auth

    certainty = "Unsure"
    diff = nextLowestDelta-lowestDelta

    if diff > 0.5:
        certainty = "Very High"
    elif diff > 0.3:
        certainty = "High"
    elif diff > 0.2:
        certainty = "Moderate"
    elif diff > 0.1:
        certainty = "Fair"
    else:
        certainty = "Low"

    return [deltaAuth, certainty]




'''
#getAuths - gets list of files containing training data for an author
            and initalises their data objects
'''
def getAuths():
    if(checkDirectory()):
        inputFiles = listdir(FILEPATH)
        for file in inputFiles:
            if(file.endswith('.txt')):
                #Using 2 letter codes for each author for use in dictionaries
                currAuthor = file.split("-")[0]
                #Upon finding a new code register a new author
                if(currAuthor not in authors):
                    authors.append(currAuthor)
                    corpora[currAuthor] = []
                    authAverageLength[currAuthor] = 0
                    noSamples[currAuthor] = 0
        authorList = ['None']
        authorList.extend(authors)
        return authorList
    else:
        return {'None'}

'''
#analyseAuthor - loads text from their training data, and creates feature list for that data for
                 categorisation
    @authCode - small text code identifier for that author
'''
def analyseAuthor(authCode):
    global totalCorpus
    if(authCode != 'None'):
        dirFiles = listdir(FILEPATH)
        authFiles = [i for i in dirFiles if i.endswith('.txt') and i.startswith(authCode)]

        for f in authFiles:
            text = readFileAsString(FILEPATH + "\\" + f)
            tokens = nltk.word_tokenize(text)
            refinedTokens = ([token for token in tokens if any(c.isalpha() for c in token)])

            corpora[authCode].extend(refinedTokens)
            noSamples[authCode] += 1
            allWordDist = nltk.FreqDist(w.lower() for w in corpora[authCode])

            lens = [len(word) for word in corpora[authCode]]
            avLength = np.mean(lens)
            mostCommonAbove5 = getWords(allWordDist.most_common(300), 7)
            totalWords = len(corpora[authCode])
            totalCorpus += refinedTokens

        return authFiles

'''
#generateIdentifier - combine corpora and create identifier using delta method (John Burrows)
    -Details on method with reference to François Dominic Laramée, at:
     https://programminghistorian.org/en/lessons/introduction-to-stylometry-with-python#third-stylometric-test-john-burrows-delta-method-advanced
'''
def generateIdentifier():
    global generated
    global featureList
    valid = True
    for auth in authors:
        if(noSamples[auth] == 0):
            valid = False

    if(valid):
        top30 = nltk.FreqDist(totalCorpus).most_common(30)

        #Calculate author features
        for auth in authors:
            freqVals[auth] = {}
            count = len(corpora[auth])
            for x in top30:
                featureCount = corpora[auth].count(x[0])
                freqVals[auth][x[0]] = featureCount/count

        #Baseline features
        featureList = [x for x,y in top30]

        for f in featureList:
            #Calculate average frequency for feature
            featureVals[f] = {}
            totalFreq = 0
            for auth in authors:
                totalFreq += freqVals[auth][f]
            featureVals[f]["Mean"] = totalFreq / len(authors)

            #Calculate standard deviation
            stdDevCurrent = 0
            for auth in authors:
                distance = freqVals[auth][f] - featureVals[f]["Mean"]
                stdDevCurrent += distance*distance

            stdDevCurrent = stdDevCurrent / (len(authors) - 1)
            stdDev = math.sqrt(stdDevCurrent)
            featureVals[f]["StdDev"] = stdDev

        #Generate the z-scores used to classify
        for auth in authors:
            knownZScores[auth] = {}

            for f in featureList:
                knownZScores[auth][f] = (freqVals[auth][f]-featureVals[f]["Mean"]) / featureVals[f]["StdDev"]

        generated = True
        return 1
    else:
        return 0

'''
#readFileAsString - gets the contents of a text file and returns it as one incredibly long string
    @filePath - location of the .txt file
'''
def readFileAsString(filePath):
    result = ""
    with open(filePath, 'r') as inputText:
        result = inputText.read().replace('\n', '')
    return result

'''
#getWords - gets words from corpora over a certain length
    @searchList - tokenised list of words to search through
    @threshold - minimum word length to get
'''
def getWords(searchList, threshold):
    words = []
    found = False
    i = 0
    noFound = 0

    while(noFound < 5 and i < len(searchList)):
        if len(searchList[i][0]) >= threshold:
            wordMost = searchList[i]
            words.append(searchList[i][0])
            noFound+=1
        i+=1

    return words

'''
#checkDirectory - checks for the directory containing existing analyses
'''
def checkDirectory():
    if not os.path.exists(FILEPATH + "//Analysis"):
        os.makedirs(FILEPATH + "//Analysis")
        return False
    else:
        return True

'''
#main - Used to initialise the gui
'''
def main():
    root = Tk()
    mainGui = gui.MainGui(root)
    root.resizable(False,False)
    root.mainloop()


if __name__ == "__main__":
    main()
