'''
@author: Joel Christophel
'''

from Tkinter import *
from tkFileDialog import askdirectory
import tkFont
import tkMessageBox

import os
import platform
import getopt

def findAppDataPath():
    system = platform.system()
    path = ''

    if system == 'Windows':
        path = os.getenv('localappdata') + '\\'
    elif system == 'Darwin':
        path = os.path.expanduser("~/Library/Application Support/")
    elif system == 'Linux':
        path = '~/.local/share/'
        
    if not os.path.isdir(path):
        path = ''
        
    return path

def findDemosPath():
    tfDirectoryChoices = ["C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\\tf", "C:\Program Files\Steam\steamapps\common\Team Fortress 2\\tf", os.path.expanduser("~/Library/Application Support/Steam/steamapps/common/Team Fortress 2/tf")]

    for i in range(0, len(tfDirectoryChoices)):
        demosPath = tfDirectoryChoices[i] + os.path.sep + "demos"
        if dirHasKillStreaksFile(demosPath): return demosPath
        if dirHasKillStreaksFile(tfDirectoryChoices[i]): return tfDirectoryChoices[i]

    return ''

def dirHasKillStreaksFile(path):
    if not os.path.isdir(path): return False

    files = os.listdir(path)

    for i in range(0, len(files)):
        if "KillStreaks.txt" == files[i]: return True

    return False

def getNotableDemos(killStreaksPath):
    with open(killStreaksPath) as f:
        lines = f.readlines()

    demos = []
    titleMatcher = re.compile('.*"(.+)".*')

    for i in range(0, len(lines)):
        if lines[i].strip():
            matches = titleMatcher.match(lines[i])
            if matches.group(1) not in demos:
                demos.append(matches.group(1).lower() + ".dem")

    return demos

def getAllDemos(path):
    try:
        files = os.listdir(path)
        demos = []

        for i in range(0, len(files)):
            if ".dem" in files[i]:
                demos.append(files[i].lower())

        return demos
    except:
        return []

def deleteUselessDemos(path, guiMode):
    try: notableDemos = getNotableDemos(path + os.path.sep + 'KillStreaks.txt')
    except IOError:
        errorMessage = "Couldn't find KillStreaks.txt in the specified directory"
        if guiMode: tkMessageBox.showwarning("Error", errorMessage)
        else: print errorMessage
        return
    allDemos = getAllDemos(path)
    counter = 0

    if notableDemos and allDemos: # Not empty
        for i in range(0, len(allDemos)):
            if allDemos[i] not in notableDemos:
                counter+=1
                os.remove(path + os.path.sep + allDemos[i])
      
    successMessage = getSuccessMessage(counter)

    if guiMode: tkMessageBox.showinfo("Success", successMessage)
    else: print successMessage
    
    with open(findAppDataPath() + 'tf2-demos-path.txt', 'w') as f:
        f.write(path)

def getSuccessMessage(counter):
    successMessage = "Deleted " + str(counter) + " useless demos!"

    if counter == 0: successMessage = "None of your demos were useless!"
    elif counter == 1: successMessage = "Deleted 1 useless demo!"

    return successMessage

class GUI (Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, padx=20, pady=15)   

        self.parent = parent
        self.initUI()
        demosPathFile = findAppDataPath() + 'tf2-demos-path.txt'
        if os.path.isfile(demosPathFile): 
            with open(demosPathFile, 'r+') as f:
                self.setText(self.pathEntry, f.readline())
        if not self.pathEntry.get(): self.setText(self.pathEntry, findDemosPath())

    def initUI(self):
        titleFont = tkFont.Font(size=13, weight='bold')
        authorFont = tkFont.Font(size= 9, weight='bold')
        titleLabel = Label(self, text='P-REC Useless Demo Deleter', font=titleFont)
        authorLabel = Label(self, text='by Joel Christophel', font=authorFont)
        pathLabel = Label(self, text='Path to demos:')
        self.pathEntry = Entry(self, width=80)
        browseButton = Button(self, text='Browse', command=self.onBrowse)
        self.autoFindButton = Button(self, text='Auto-find', command=self.onAutoFind)
        deleteButton = Button(self, text='Delete useless demos', command=self.onDelete)

        titleLabel.grid(row=0, column=0, columnspan=4)
        authorLabel.grid(row=1, column=0, columnspan=4, pady=(4, 20))
        pathLabel.grid(row=2, column=0, padx=(0, 15))
        self.pathEntry.grid(row=2, column=1, padx=(0, 15))
        browseButton.grid(row=2, column=2, padx=(0, 8))
        self.autoFindButton.grid(row=2, column=3)
        deleteButton.grid(row=3, column=0, columnspan=4, pady=(25, 0))

        self.pack()

    def setText(self, entry, text):
        self.pathEntry.delete(0, len(entry.get()))
        self.pathEntry.insert(0, text)

    def onBrowse(self):
        self.setText(self.pathEntry, askdirectory())

    def onAutoFind(self):
        path = findDemosPath()
        if path:
            self.setText(self.pathEntry, findDemosPath())
        else:
            tkMessageBox.showwarning("Sorry", "Couldn't automatically find your demos")

    def onDelete(self):
        deleteUselessDemos(self.pathEntry.get(), True)

def center(window):
    window.update_idletasks()
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    size = tuple(int(_) for _ in window.geometry().split('+')[0].split('x'))
    x = screenWidth/2 - size[0]/2
    y = screenHeight/2 - size[1]
    window.geometry("%dx%d+%d+%d" % (size + (x, y)))

def printHelpMessage():
    print ''
    print 'Use -p or --path to specify the location of your demos. Run the program without any arguments for a graphical user interface. Use -h or --help for these instructions.'

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:h', ['path=', 'help'])
    except getopt.GetoptError:
        print ""
        print "Invalid option."
        printHelpMessage()
        sys.exit(2)

    if opts:
        for opt, arg in opts:
            if opt in ('-p', '--path'):
                deleteUselessDemos(arg, False)
            elif opt in ('-h', '--help'):
                printHelpMessage()
            else:
                print ""
                print "'" + opt + "' is not a valid option."
                printHelpMessage()
    else:
        window = Tk()
        window.title('P-REC Useless Demo Deleter for TF2')
        try:
            window.iconbitmap(default='tf2.ico')
        except:
            pass 
        GUI(window)
        center(window)
        window.update()
        window.resizable(width=FALSE, height=FALSE)
        window.mainloop()