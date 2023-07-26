# NOTE: I wrote and ran this code locally. I doubt whether it'll run in anything other than just straight python on your local machine.
# Make sure you create an 'output' folder in the same directory as Analyse.py, and drop the dialogueText.csv from the ubuntu dataset
# into the folder alongside it too. I'm not including that in the repo because of its size. Then you can just call it like:
# > python .\Analyse.py 
# or
# > python .\Analyse.py -f dialogueText2.csv -q 20 -a 50
# Enjoy! :)
# -Matt

#region Imports

from typing import List
from tqdm import tqdm
import pandas as pd
import argparse
from datetime import datetime
from collections import Counter

#endregion

#region Command Line Arguments

argParser = argparse.ArgumentParser(description="Analyse.py Argument Parser",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
argParser.add_argument("-f", "--filename", default="dialogueTextTEST.csv", type=str, help="Which file to analyse")
argParser.add_argument("-q", "--question-length-threshold", type=int, default=20, help="Question length (words) threshold")
argParser.add_argument("-a", "--answer-length-threshold", type=int, default=20, help="Answer length (words) threshold")

args = argParser.parse_args()

#endregion

#region Internal Classes

class Dialogue:
    id = 0,
    utterances = [],
    questionCount = 0,
    combinedQuestionWordLength = 0,
    combinedAnswerWordLength = 0,
    answerCount = 0

    def __init__(self, id):
        self.id = id
        self.utterances = []
        self.questionCount = 0
        self.combinedQuestionWordLength = 0
        self.combinedAnswerWordLength = 0
        self.answerCount = 0

class Utterance:
    text = "",
    dialogueId = -1,
    fromUser = "",
    isQuestion = False,
    isAnswer = False

    def __init__(self, text, dialogueId, fromUser):
        self.text = text
        self.dialogueId = dialogueId
        self.fromUser = fromUser
        self.isQuestion = False
        self.isAnswer = False

#endregion

#region Logger Setup

# Log to console, and to a timestamped log file
def Log(text):    
    print(text)
    with open(logFilePath, 'a') as f:
        f.write(datetime.now().strftime("%H:%M:%S") + " " + text + "\n")

#endregion

#region Setup

fileName = args.filename
questionWordThreshold = args.question_length_threshold
answerWordThreshold = args.answer_length_threshold

startTime = datetime.now()
logFileName = startTime.strftime("%Y%m%d_%H%M%S.txt")
logFilePath = "./output/{logFileName}".format(logFileName = logFileName)

totalQuestionCount = 0
totalAnswerCount = 0
total3TurnDialogueCount = 0
totalNon3TurnDialogueCount = 0
totalLTEQuestionThresholdWord3TurnDialogueCount = 0
totalOverQuestionThresholdWord3TurnDialogueCount = 0
totalLTEAnswerThresholdWord3TurnDialogueCount = 0
totalOverAnswerThresholdWord3TurnDialogueCount = 0
totalDialoguesWithinThreshold = 0

df = (pd.read_csv(fileName))

#endregion

#region Data Handling

def GetUtterances():
    parsedUtterances = []

    for index, row in df.iterrows():
        dialogueId = row["dialogueID"]
        # Strip .tsv from end of dialogue Id
        dialogueId = dialogueId[0:len(dialogueId) - 4]

        # Make unique id from folder and dialogue id
        strUniqueId = "{folderId}{dialogueId}".format(folderId = row["folder"], dialogueId = dialogueId)
        parsedUtterances.append(Utterance(row['text'], int(strUniqueId), row['from']))

    return parsedUtterances

#endregion

#region Data Analysis

# def PerformAnalysis():
#     Log("Proceeding with analysis tasks...")

#     startTime = datetime.now()

#     Log("Commencing analysis of {commentClassDescription} class comments".format(commentClassDescription = commentClass.description))

#     for comment in tqdm(commentClass.comments):
#         TokeniseForAnalysis(comment, commentClass)

#     Log("Spelling corrections required for {count} words".format(count = commentClass.correctedSpellingsCount))
#     Log("Sentence count: {count}".format(count = commentClass.sentenceCount))
#     Log("Token counts - before processing: {preTokensCount}, after processing: {postTokensCount} ".format(
#         preTokensCount = commentClass.preProcessedTokenCount, postTokensCount = commentClass.postProcessedTokenCount))
#     Log("Most commonly-appearing words: {top10}".format(top10 = Counter(commentClass.tokens).most_common(10)))

#     endTime = datetime.now()
#     secondsElapsed = str(endTime - startTime)
#     Log("Finished analysing '{commentClassDescription}' class in {elapsed}".format(
#         commentClassDescription = commentClass.description, elapsed = secondsElapsed))
    
#     Log("Analysis complete.")

#endregion

#region Program Flow

Log("Parsing utterances...")
utterances:List[Utterance] = GetUtterances()
Log("Done. {count} utterances parsed.".format(count = len(utterances)))

Log("Parsing into dialogues")
dialogues:List[Dialogue] = []
dialogue = Dialogue(utterances[0].dialogueId)
lastDialogueId = utterances[0].dialogueId

for u in tqdm(utterances):
    if u.dialogueId != lastDialogueId:
        # Stash the current dialogue and create a new one to work with
        dialogues.append(dialogue)
        dialogue = Dialogue(u.dialogueId)

    # NOTE: Following our meeting 26/7/23, this logic is questionable
    if len(dialogue.utterances) == 0:
        # must the the question, first message
        u.isQuestion = True
    elif len(dialogue.utterances) == 1:
        u.isQuestion = (dialogue.utterances[0].fromUser == u.fromUser)
        u.isAnswer = (dialogue.utterances[0].fromUser != u.fromUser)
    else:
        # third turn cannot be the question
        u.isQuestion = False
        u.isAnswer = True

    dialogue.utterances.append(u)

    if u.isQuestion:
        dialogue.questionCount += 1
        totalQuestionCount += 1
        dialogue.combinedQuestionWordLength += len(str(u.text))

    if u.isAnswer:
        dialogue.answerCount += 1
        totalAnswerCount += 1
        dialogue.combinedAnswerWordLength += len(str(u.text))

    lastDialogueId = u.dialogueId

# now push the final dialogue we were working on
dialogues.append(dialogue)

Log("Parsed utterances into {count} distinct dialogues".format(count = len(dialogues)))

for dialogue in dialogues:
    if len(dialogue.utterances) == 3:
        total3TurnDialogueCount += 1
        if dialogue.combinedQuestionWordLength <= questionWordThreshold:
            totalLTEQuestionThresholdWord3TurnDialogueCount += 1
        else:
            totalOverQuestionThresholdWord3TurnDialogueCount += 1

        if dialogue.combinedAnswerWordLength <= answerWordThreshold:
            totalLTEAnswerThresholdWord3TurnDialogueCount += 1
        else:
            totalOverAnswerThresholdWord3TurnDialogueCount += 1

        if dialogue.combinedQuestionWordLength <= questionWordThreshold and dialogue.combinedAnswerWordLength <= answerWordThreshold:
            totalDialoguesWithinThreshold += 1
    else:
        totalNon3TurnDialogueCount += 1
        Log("Non 3 Turn Dialogue found, Our Unique ID: {id}".format(id=dialogue.id))

Log("There are {count} non-three-turn dialogues".format(count = totalNon3TurnDialogueCount))
Log("There are {count} three-turn dialogues".format(count = total3TurnDialogueCount))
Log("Among the three-turn dialogues, there are {count} with <={threshold} question words (in threshold), and {count2} over threshold"
    .format(count = totalLTEQuestionThresholdWord3TurnDialogueCount, count2 = totalOverQuestionThresholdWord3TurnDialogueCount, threshold=questionWordThreshold))
Log("Among the three-turn dialogues, there are {count} with <={threshold} answer words (in threshold), and {count2} over threshold"
    .format(count = totalLTEAnswerThresholdWord3TurnDialogueCount, count2 = totalOverAnswerThresholdWord3TurnDialogueCount, threshold=answerWordThreshold))
Log("Total Number of Dialogues Falling Within the specified Thresholds: {count}".format(count=totalDialoguesWithinThreshold))

Log("Getting Word Counts")
# Note that we are given the following data from toc.csv in the ubuntu dataset, so no need to get it again
#lines,words,characters,filename
#9212878,91660344,996253904,dialogueText_196.csv
#16587831,166392849,1799936480,dialogueText_301.csv
#1038325,11035331,116070597,dialogueText.csv

# Note, I used 'Counter' in my mid-module assignment to get the most popular words.
# I think you'll need a quick and dirty spaCy tokeniser to rip the utterances list into just a flat list of words.
# It's going to be massive, but once you've done that, you can do Counter(flatListOfWords).most_common(20) 

Log("Analyse.py ceased executing at {now}".format(now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
Log("Shell output logged to {file}".format(file = logFilePath))

#endregion