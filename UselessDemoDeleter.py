'''
@author: Joel Christophel
'''

from Tkinter import *
from tkFileDialog import askdirectory
import tkFont
import tkMessageBox

import getopt
import os
import platform

dateVar = None
dateArg = False
guiMode = False

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

#"Notable" means that demo is listed in KillStreaks.txt
def getNotableDemos(killStreaksPath):
    with open(killStreaksPath) as f:
        lines = f.readlines()

    demos = []
    titleMatcher = re.compile('.*"(.+)".*')

    for i in range(0, len(lines)):
        if lines[i].strip():
            matches = titleMatcher.match(lines[i])
            if matches.group(1) not in demos:
                demos.append(matches.group(1) + ".dem")

    return demos

#"Eligible" means that filename meets criteria for deletion
def getEligibleDemos(path):
    try:
        files = os.listdir(path)
        demos = []

        onlyDeleteDates = dateVar.get() == 1 if guiMode else dateArg

        for i in range(0, len(files)):
            if (onlyDeleteDates and re.match(r'.*\d{8}_\d{4}.*\.dem', files[i])) or (not onlyDeleteDates and '.dem' in files[i]):
                demos.append(files[i])      
        return demos
    except:
        return []

def deleteUselessDemos(path):
    try: notableDemos = getNotableDemos(path + os.path.sep + 'KillStreaks.txt')
    except IOError:
        errorMessage = "Couldn't find KillStreaks.txt in the specified directory"
        if guiMode: tkMessageBox.showwarning("Error", errorMessage)
        else: print errorMessage
        return
    eligibleDemos = getEligibleDemos(path)
    counter = 0

    if notableDemos and eligibleDemos: # Not empty
        for i in range(0, len(eligibleDemos)):
            if eligibleDemos[i] not in notableDemos:
                counter+=1
                os.remove(path + os.path.sep + eligibleDemos[i])
      
    successMessage = getSuccessMessage(counter)

    if guiMode: tkMessageBox.showinfo("Success", successMessage)
    else:
        print ''
        print successMessage
    
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
        self.settingsWindow = self.initSettings()
        titleFont = tkFont.Font(size=13, weight='bold')
        authorFont = tkFont.Font(size= 9, weight='bold')
        titleLabel = Label(self, text='P-REC Useless Demo Deleter', font=titleFont)
        authorLabel = Label(self, text='by Joel Christophel', font=authorFont)
        pathLabel = Label(self, text='Path to demos:')
        self.pathEntry = Entry(self, width=80)
        browseButton = Button(self, text='Browse', command=self.onBrowse)
        self.autoFindButton = Button(self, text='Auto-find', command=self.onAutoFind)
        
        dateFrame = Frame(self)
        global dateVar
        dateVar = IntVar()
        dateVar.set(1)
        dateButton = Checkbutton(dateFrame, variable=dateVar)
        dateLabel = Label(dateFrame, text="Only delete demos with filenames containing P-REC's date format")
        
        bottomFrame = Frame(self)
        settingsButton = Button(bottomFrame, text='Settings', command=self.onSettings)
        deleteButton = Button(bottomFrame, text='Delete useless demos', command=self.onDelete)

        row = 0;
        titleLabel.grid(row=row, column=0, columnspan=4)
        row += 1
        authorLabel.grid(row=row, column=0, columnspan=4, pady=(4, 20))
        row += 1
        pathLabel.grid(row=row, column=0, padx=(0, 15))
        self.pathEntry.grid(row=row, column=1, padx=(0, 15))
        browseButton.grid(row=row, column=2, padx=(0, 8))
        self.autoFindButton.grid(row=row, column=3)
        row += 1
        dateButton.grid(row=row, column=0)
        dateLabel.grid(row=row, column=1)
        row += 1
        dateFrame.grid(row=row, column=0, columnspan=4, pady=(15, 0))
        dateButton.grid(row=0, column=0)
        dateLabel.grid(row=0, column=1)
        row += 1
        bottomFrame.grid(row=row, column=0, columnspan=4, pady=(25, 0))
        #settingsButton.grid(row=0, column=0, padx=(0, 8))
        deleteButton.grid(row=0, column=1)

        self.pack()

    def initSettings(self):
        window = Toplevel(width=500, height=300, padx=20, pady=15)
        window.withdraw()
        window.title('Settings')
        center(window)
        window.protocol("WM_DELETE_WINDOW", self.onSettingsExit)

        self.dateVar = IntVar()
        self.dateVar.set(1)
        #self.dateVar.trace('w', self.onVarChanged)
        self.dateButton = Checkbutton(window, variable=self.dateVar)
        dateLabel = Label(window, text="Only delete demos with filenames containing P-REC's date format")
        okayButton = Button(window, text='Okay')
        
        row = 0
        self.dateButton.grid(row=row, column=0)
        dateLabel.grid(row=row, column=1)
        row += 1
        okayButton.grid(row=row, column=0, columnspan=2, pady=(25, 0))

        return window

    def onSettingsExit(self):
        self.settingsWindow.withdraw()

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

    def onSettings(self):
        self.settingsWindow.deiconify()

    def onDelete(self):
        deleteUselessDemos(self.pathEntry.get())

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
    print "Run the program without any arguments for a graphical user interface.\nUse -p or --path to specify the location of your demos.\nUse -d or --date (no parameter) to indicate that you only wish to delete demos with filenames containing P-REC's date format.\nUse -h or --help for these instructions."

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:dh', ['path=', 'date', 'help'])
    except getopt.GetoptError:
        print ""
        print "Invalid option."
        printHelpMessage()
        sys.exit(2)

    if opts:
        guiMode = False
        deleteDemos = True
        path = ''

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                printHelpMessage()
                deleteDemos = False
                break
            elif opt in ('-p', '--path'):
                path = arg
            elif opt in ('-d', '--date'):
                dateArg = True
            else:
                print ""
                print "'" + opt + "' is not a valid option."
                printHelpMessage()
                deleteDemos = False
                break

        if deleteDemos: deleteUselessDemos(path)
    else:
        guiMode = True
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
        window.focus()
        window.mainloop()