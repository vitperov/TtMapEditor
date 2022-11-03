#!/usr/bin/python

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from modules.Model import *
from modules.View import *
from modules.Controller import *

def main():
    app = QApplication(sys.argv)

    view = Window()
    view.show()
    
    #stream = Stream(newText=view.consoleWrite)
    #sys.stdout = stream
        

    model = Model()

    controller = Controller(view=view, model=model)

    exitcode = app.exec_()
    
    del stream
    sys.stdout = sys.__stdout__

    sys.exit(exitcode)

if __name__ == '__main__':
    main()
