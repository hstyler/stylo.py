﻿		╔═══════════════════════════════════════╗
		║  ____  _         _                    ║
		║ / ___|| |_ _   _| | ___   _ __  _   _ ║
		║ \___ \| __| | | | |/ _ \ | '_ \| | | |║
		║  ___) | |_| |_| | | (_) || |_) | |_| |║
		║ |____/ \__|\__, |_|\___(_) .__/ \__, |║
		║            |___/         |_|    |___/ ║
		╚═══════════════════════════════════════╝
	   _               
  ___  ___| |_ _   _ _ __  
 / __|/ _ \ __| | | | '_ \ 
 \__ \  __/ |_| |_| | |_) |
 |___/\___|\__|\__,_| .__/ 
                    |_|  

Required packages: nltk, sklearn, tkinter, numpy

To install the required packages:

pip3 install <packagename> --upgrade
		or
pip install <packagename> --upgrade

-----------------------------------------------
To set up nltk:

Open the Python console and run:

import nltk
nltk.download()
            _     _ _                   _       _        
   __ _  __| | __| (_)_ __   __ _    __| | __ _| |_ __ _ 
  / _` |/ _` |/ _` | | '_ \ / _` |  / _` |/ _` | __/ _` |
 | (_| | (_| | (_| | | | | | (_| | | (_| | (_| | || (_| |
  \__,_|\__,_|\__,_|_|_| |_|\__, |  \__,_|\__,_|\__\__,_|
                            |___/                        
The program reads in training data from '/Source', in its local directory.
Files should be named as such:
<author name>-<number>.txt
e.g. hplovecraft-1.txt
And contain a raw text extract of their writing to be analysed.

Test data can be added in the same format as above to '/Test', and tests run from the GUI, explained below.


   _     _            _   _  __ _           _   _             
  (_) __| | ___ _ __ | |_(_)/ _(_) ___ __ _| |_(_) ___  _ __  
  | |/ _` |/ _ \ '_ \| __| | |_| |/ __/ _` | __| |/ _ \| '_ \ 
  | | (_| |  __/ | | | |_| |  _| | (_| (_| | |_| | (_) | | | |
  |_|\__,_|\___|_| |_|\__|_|_| |_|\___\__,_|\__|_|\___/|_| |_|
                                                             
To identify the most likely author of a section of text, populate the text source folder with 
writing from all of the authors you want to decide from (as described above).
Then run stylo.py to open the GUI.
╔═══════════════════════════════════════════════════════════════════════════════════════════════════╗
║ ∂ Stylometric Analyser                                                                            ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════════╣
║               ¹┌─────────────┐ ²┌─────────┐⁴┌────────────────────────┐⁹┌────────────────────────┐ ║
║Author Samples  │ None  [__]  │  │ Analyse │ │ Analysed Training Data │ │       Tests Run        │ ║
║                └─────────────┘  └─────────┘ │ <author1>[-]           │ │ <author1>[-]           │ ║
║³┌─────────────────────────────────────────┐ │    ├author1-1.txt      │ │    ├PASS:author1-1.txt │ ║
║ │            Analyse All Files            │ │    ├author1-2.txt      │ │    ├PASS:author1-2.txt │ ║
║ └─────────────────────────────────────────┘ │ <author2>[-]           │ │ <author2>[-]           │ ║
║⁵┌─────────────────────────────────────────┐ │    ├author2-1.txt      │ │    ├PASS:author2-1.txt │ ║
║ │           Create Identifier             │ │    ├author2-2.txt      │ │    ├PASS:author2-2.txt │ ║
║ └─────────────────────────────────────────┘ │    ├author2-3.txt      │ │    ├FAIL:author2-3.txt │ ║
║⁸┌─────────────────────────────────────────┐ │ <author3>[+]           │ │    ├PASS:author2-4.txt │ ║
║ │               Run Tests                 │ │                        │ │ <author3>[+]           │ ║
║ └─────────────────────────────────────────┘ │                        │ │                        │ ║
║⁶┌─────────────────────────────────────────┐ │                        │ │                        │ ║
║ │            Determine Author             │ │                        │ │                        │ ║
║ └─────────────────────────────────────────┘ └────────────────────────┘ └────────────────────────┘ ║
║                       ⁷                                                                           ║
║                        Current Accuracy: x %                                                      ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════╝
(UI Diagram - See UI.png if this is not displayed correctly)

1: When the program loads, it will load the list of identified authors in the training data.
   You can choose a specific author to analyse with this drop down list
2: When you have chosen an author to analyse, click 'Analyse' and it will process their data
3: If you simply want to analyse all of the data you have given, press 'Analyse all available'
   WARNING: with large text samples, this will take some time to process.
4: When a file is analysed, it is added to a tree view, you can expand each authors list to see
   which files have been loaded.
5: When you have loaded files for each author, click 'Create Identifier'. This will take each set of
   text data and process it to create a set of features to identify that author, enabling you to determine
   the author of text files outside of the training set.
6: After a identifier is created, clicking 'Determine Author' will allow you to open a file for identification.
   When a result is determined, it will show the result in a message box, and ask if this was correct, for use 
   in testing with known samples. 
7: When you mark an prediction as correct/incorrect, this is used to determine the accuracy of the classifier 
   so far, which is displayed here.
8: Tests can be run, taking labelled text files, identifying them and comparing the result with the actual
   answer. Clicking on 'Run Tests' will perform this test on all files in /Tests.
9: The results of the tests will show up in this tree view, and the accuracy of the classifier (7) will be
   updated on completion of all tests.


                       _                  
  _ __  _ __ _____   _(_) ___  _   _ ___  
 | '_ \| '__/ _ \ \ / / |/ _ \| | | / __| 
 | |_) | | |  __/\ V /| | (_) | |_| \__ \ 
 | .__/|_|  \___| \_/ |_|\___/ \__,_|___/ 
 |_|  | |_ ___  ___| |_                   
      | __/ _ \/ __| __|                  
      | ||  __/\__ \ |_       _ _         
       \__\___||___/\__|_   _| | |_ ___   
         | '__/ _ \/ __| | | | | __/ __|  
         | | |  __/\__ \ |_| | | |_\__ \  
         |_|  \___||___/\__,_|_|\__|___/  
                                          

Training Data:
--------------
Arthur Conan Doyle: 5 samples (338,149 words)
Charles Dickens: 5 samples (651,674 words)
H.P. Lovecraft: 8 samples (120,707 words)
Mark Twain: 4 samples (395,368 words)
Oscar Wilde: 4 samples (156,454 words)
William Shakespeare: 4 samples (68,049 words)

Test Data:
----------
