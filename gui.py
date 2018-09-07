import os
from os import listdir
import stylo
from tkinter import Tk, BOTH
from tkinter.ttk import *
from tkinter import *

class MainGui:
    currentSelection = 'None'
    loadedFiles = {}
    totalTests = 0
    totalCorrect = 0
    FILEPATH = os.path.dirname(os.path.abspath(__file__))
    testsRun = []

    '''
    #getFileList - gets the list of files added to the treeview
    '''
    def getFileList(self):
        storedAuthors = self.analysisTree.get_children()
        for i in storedAuthors:
            print(self.analysisTree.item(i))

    '''
    #createID - calls to the stylometry module to generate an identifier
    '''
    def createID(self):
        if(stylo.generateIdentifier() == 0):
            messagebox.showinfo("Error", "In order to generate an identifier, more than one author's texts should be loaded")
        else:
            messagebox.showinfo("Success", "Identifier created successfully")

    def updateAccuracy(self, passFail):
        if(passFail):
            self.totalCorrect += 1
            self.totalTests += 1
        else:
            self.totalTests += 1

        self.currentAccuracy['text'] = "Current Accuracy: " + str("{0:.0%}".format(self.totalCorrect/self.totalTests))

    def loadTests(self):
        if(stylo.checkGenerated()):
            dirFiles = listdir(self.FILEPATH + "//Test")
            testFiles = [i for i in dirFiles if i.endswith('.txt')]

            count = 0
            failCount = 0
            passCount = 0
            testResults = {}
            for i in testFiles:
                if(i not in self.testsRun):
                    count += 1
                    self.testsRun.append(i)
                    answer = i.split("-")[0]

                    if(not self.resultsTree.exists(answer)):
                        self.resultsTree.insert('', 'end', answer, text=answer)

                    result = stylo.identify(self.FILEPATH + "//Test//" + i)
                    if(result[0] == answer):
                        self.resultsTree.insert(answer, 'end', text="PASS: " + i, tags=('PASS',))
                        self.updateAccuracy(True)
                        passCount += 1
                    else:
                        self.resultsTree.insert(answer, 'end', text="FAIL " + i + " (" + result[0] + ")", tags=('FAIL',))
                        self.updateAccuracy(False)
                        failCount += 1

                    self.resultsTree.tag_configure('PASS', background='green')
                    self.resultsTree.tag_configure('FAIL', background='red')

            messagebox.showinfo("Test Results", "Run " + str(count) + " tests: " + str(passCount) + " passes, " + str(failCount) + " fails.")
        else:
            messagebox.showinfo("Error", "In order to run tests, an identifier should be generated first.")

    '''
    #identify - identifies the author of a selected text file
    '''
    def identify(self):
        if(stylo.checkGenerated()):
            filePath = filedialog.askopenfilename(initialdir = self.FILEPATH,title = "Choose a File to Open",filetypes=[("text files","*.txt")])
            author = stylo.identify(filePath)
            mode = messagebox.askyesno("ID Mode", "Do you know the actual author of the text?")
            if(mode):
                result = messagebox.askyesno("Identification", "The author of this text is predicted to be: " + author[0] + ", with certainty: (" + author[1] + ") - is this correct?")
                if(result):
                    self.updateAccuracy(True)
                else:
                    self.updateAccuracy(False)
            else:
                messagebox.showinfo("Identification", "The author of this text is predicted to be: " + author[0] + ", with certainty: (" + author[1] + ")")
        else:
            messagebox.showinfo("Error", "In order to identify a text, an identifier should be generated first.")
    '''
    #analyse - runs analysis on a specific authors training data
        @authCode - small string code representing that author
    '''
    def analyse(self, authCode):
        files = stylo.analyseAuthor(authCode)
        if files:
            self.loadedFiles[authCode] = files

            if(not self.analysisTree.exists(authCode)):
                self.analysisTree.insert('', 'end', authCode, text=authCode)

            for i in files:
                self.analysisTree.insert(authCode, 'end', text=i)
        else:
            messagebox.showinfo("Error", "No associated files found for author: " + authCode + " - check that some have been loaded")

    '''
    #analyseAll - analyses all files loaded
    '''
    def analyseAll(self, *args):
        result = messagebox.askokcancel("Analyse all", "If there are a lot of files to analyse, this function can take a while, would you like to continue?")
        if result == 1:
            auths = stylo.getAuths()
            for i in auths:
                if not i == "None":
                    self.analyse(i)

            self.getFileList()
        else:
            messagebox.showinfo("Analyse all", "Operation cancelled.")

    '''
    #analyseClicked - event function for the analyse button, runs analysis on the item selected in the drop-down
    '''
    def analyseClicked(self, *args):
        self.analyse(self.currentSelection)

    '''
    #authChanged - event function for the drop-down, sets a variable to the currently selected value so that this can be referenced elsewhere
    '''
    def authChanged(self, value):
        self.currentSelection = value

    '''
    Initialises all UI elements
    '''
    def __init__(self,master):
        self.master = master
        master.option_add("*Font", ("Segoe UI", 12))
        master.title("Stylometric Analyser")

        self.authLabel = Label(master, text="Author Samples: ")
        self.authLabel.grid(row = 1, column = 1)

        self.authChoiceVar = StringVar(master)
        self.choices = stylo.getAuths()
        self.authChoiceVar.set('None')
        self.authChoice = OptionMenu(master, self.authChoiceVar, *self.choices, command=self.authChanged)
        self.authChoice.grid(row = 1, column = 2)

        self.analyseButton = Button(master, text = "Analyse", command=self.analyseClicked)
        self.analyseButton.grid(row = 1, column = 3)

        Separator(master, orient=VERTICAL).grid(column = 4, row = 1, sticky =N+S, rowspan=5, padx = 5)

        self.analysisTree = Treeview(master)
        self.analysisTree.heading('#0', text='Analysed Training Data')
        self.analysisTree.grid(row = 1, column = 5, padx = 5, rowspan=5)

        self.resultsTree = Treeview(master)
        self.resultsTree.heading('#0', text='Tests Run')
        self.resultsTree.grid(row = 1, column = 6, padx = 5, rowspan=5)

        self.analyseAllButton = Button(master, text = "Analyse All Files", command=self.analyseAll)
        self.analyseAllButton.grid(row = 2, column = 1, columnspan = 3, sticky=W+E)

        self.createIdButton = Button(master, text="Create Identifier", command=self.createID)
        self.createIdButton.grid(row=3,column=1,columnspan=3,sticky=W+E)

        self.identifyButton = Button(master, text="Determine author", command=self.identify)
        self.identifyButton.grid(row=5,column=1,columnspan=3,sticky=W+E)

        self.identifyButton = Button(master, text="Run Tests", command=self.loadTests)
        self.identifyButton.grid(row=4,column=1,columnspan=3,sticky=W+E)

        self.currentAccuracy = Label(master, text = "Current accuracy: ")
        self.currentAccuracy.grid(row=6, column = 1, columnspan = 5)
