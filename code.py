import zipfile
import threading
import time
from tkinter import *
import string

doneLoading = False #ends loading screen once index has loaded

table = str.maketrans({key: None for key in string.punctuation})#for removing punctuation from strings

zipFile = zipfile.ZipFile("C:/Users/magui/PycharmProjects/stuff/rhf.zip")
fileNames = zipFile.namelist()

#threading used to play loading animation while index loads
def loadingAnimation():
    loadScreen = Tk()
    loadScreen.attributes("-topmost", 1)
    loadScreen.title("ZipSearch")
    loadScreen.configure(background="black")
    #textDisplay1 = Label(loadScreen, text='Loading Index', bg='black', fg='white', font='none 12').pack()
    loadingImage1 = PhotoImage(file='loadingicon.gif', format='gif -index 0')
    loadingImage2 = PhotoImage(file='loadingicon.gif', format='gif -index 1')
    loadingImage3 = PhotoImage(file='loadingicon.gif', format='gif -index 2')
    loadingImage4 = PhotoImage(file='loadingicon.gif', format='gif -index 3')
    loadingImages = [loadingImage1, loadingImage2, loadingImage3, loadingImage4]
    pic = Label(loadScreen, image=loadingImages[0])
    pic.photo = loadingImages[0]
    pic.pack()
    timer = Label(loadScreen, text='time elapsed: 0.0s', bg='black', fg='white')
    timer.pack()
    timeSoFar = 0
    i = 0
    while doneLoading == False:
        i = (i+1)%4
        pic.configure(image = loadingImages[i])
        #textList[1]
        loadScreen.update_idletasks()
        loadScreen.update()
        time.sleep(0.07)
        timeSoFar += 0.07
        text="time elapsed: "+"{0:.2f}".format(timeSoFar)+'s'
        timer.configure(text=text)
    loadScreen.destroy()
t1 = threading.Thread(name='loadingScreen', target=loadingAnimation)
t1.start()

#loads index of files
fileNameDictionary = {}
fileContentDictionary = {}
for fileName in fileNames:
        # create string to hold file contents
    openFile = zipFile.open(fileName, 'r')
        # ceates a list containing all strings and makes them lower-case

    fileContent = str(openFile.read()).lower().translate(table).split()
    wordList = []  # will contain all alphabet words in file
        # adds strings with only alphabet chars to list

    for string in fileContent:
        if string.isalpha():
            wordList.append(string)

      # create dictionary to be nested
    for word in wordList:
            # key maps to num occurances
        if fileContentDictionary.get(word) == None:
            fileContentDictionary[word] = {'inFiles': {fileName:1}, 'numLocations':1 }
        elif fileContentDictionary[word]['inFiles'].get(fileName) != None:
            fileContentDictionary[word]['inFiles'][fileName] += 1
            fileContentDictionary[word]['numLocations'] += 1
        else:#word not in this file
            fileContentDictionary[word]['inFiles'].update({fileName: 1})
            fileContentDictionary[word]['numLocations'] += 1


            # fileContentDictionary.setdefault(word, []).append(word)
        # map fileName key to dictionary containing all words in the file
doneLoading = True #signals loadingAnimation to end

#scans keyword from inputBox and searches index. outputs files with word
def click(event=None):
    keyword = textEntry.get()
    keyword = keyword.lower()
    output.delete(0.0,END)
        # if keyword is in the nested dictionary
    if fileContentDictionary.get(keyword) != None:

        numOccurrences = fileContentDictionary.get(keyword)['numLocations']
        inFiles = list(fileContentDictionary.get(keyword)['inFiles'])
        if numOccurrences == 1:
            outText = 'found ' + str(numOccurrences) + ' match in '+str(len(inFiles))+' file:'
            output.insert(END, outText + '\n')
            outText = str(numOccurrences) + " match in: " + inFiles[0]
            output.insert(END, outText+'\n')
        else:
            outText = 'found ' + str(numOccurrences) + ' matches in '+str(len(inFiles))+' files:'
            output.insert(END, outText + '\n')
            for file in inFiles:
                outText = str(fileContentDictionary[keyword]['inFiles'][file]) + " matches in: " + file
                output.insert(END, outText+'\n')
    else:
        output.insert(END, 'no match found')

#create main program window
window = Tk()
window.attributes("-topmost", 1)
window.title("ZipSearch")
window.configure(background = "black")

Label(window, text='Please enter a search term:', bg='black', fg='white', font='none 20').pack()

textEntry = Entry(window, width=20, bg="white", fg='black', font='none 20')
textEntry.pack(pady=15)

#allows button click or pressing enter to initiate keyword search
submit = Button(window, text="submit", width = 6, command = click, bg='black', fg='white', font='none 20').pack()
window.bind('<Return>', click)

output = Text(window, width=75, height=12, wrap=WORD, background='white', foreground='black', font='none 20')
output.pack(padx=15, pady=15)
window.mainloop()

"""store word locations by file, char Number, and line"""
"""
try to use multi-threading to decrease the time to load the index
by splitting the fileNameList into parts and having each thread handle a 
different part of the list. will probably use 4 threads
"""
"""
track location by tracking each string in a file linearly
ie. the first string is 1, second word is 2 etc... then use those numbers
to search for phrases. this will work by splitting the phrase into 
a list of strings, then checking if the order of the strings in the file
matches the order of strings in the list.
"""