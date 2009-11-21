#   $Author: almar $
#   $Date: 2008-09-30 10:26:38 +0200 (Tue, 30 Sep 2008) $
#   $Rev: 557 $
#
#   Copyright 2008 Almar Klein
#
#   This file is part of IEP.
#    
#   IEP is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
# 
#   IEP is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
# 
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" IEP - Interactive Editor for Python
This is the main module, where I define some stuff to be used in the other
modules.

"""

import sys, os

# import ssdf or the suplied copy if not available
try:
    import ssdf
except ImportError:
    # if strux not available, use the copy we included with IEP
    import ssdf_copy as ssdf


## Some functions...

def isFrozen():
    """ Find out whether this is a frozen application
    (using bbfreeze or py2exe) by finding out what was
    the executable name to start the application.
    """
    import os
    ex = os.path.split(sys.executable)[1]
    ex = os.path.splitext(ex)[0]
    if ex.lower() == 'python':
        return False
    else:
        return True


def getResourceDir():
    """ Get the directory to the resources. """
    if isFrozen():
        path =  os.path.abspath( os.path.dirname(sys.executable) )
    else:
        path = os.path.abspath( os.path.dirname(__file__) )
    return path

# get the path where IEP is located
path = getResourceDir()

def startIep():
    """ RUN IEP 
    """        
    from main import MainWindow
    from PyQt4 import QtCore, QtGui
    app = QtGui.QApplication([])
    app.setStyle(config.qtstyle)
    frame=MainWindow()
    app.exec_()
    
    
def normalizeLineEndings(text):
    """ normalize text, following Python styles.
    Convert all line endings to the \\n (LF) style.    
    """ 
    # line endings
    text = text.replace("\r\n","\n")
    text = text.replace("\r","\n")    
    # done
    return text


def GetMainFrame(window):
    """ Get the main frame, giving a window that's in it.
    Can be used by windows to find the main frame, and
    via it, can interact with other windows.
    """
    try:
        while True:
            parent = window.parent()
            if parent is None:
                return window
            else:
                window = parent
    except:    
        raise Exception("Cannot find the main window!")


## the configuration stuff...

defaultConfigString = """
qtstyle = 'cleanlooks'
editorState = ''
editorStackBarWidth = 128
editorStackBarSpacing = 0
find_matchCase = 1
find_regExp = 1
editor = dict:
  showWhiteSpace = 0
  showWrapSymbols = 0
  showLineEndings = 0
  zoom = 0
  autoIndent = 1
  highlightCurrentLine = 1
  edgeColumn = 80  
  showIndentGuides = 1
  wrapText = 1
  defaultStyle = 'python'
  defaultIndentation = 4
  defaultLineEndings = 'LF'
  doBraceMatch = 1
  tabWidth = 4
  codeFolding = 0
  # advanced settings
  homeAndEndWorkOnDisplayedLine = 1
shortcuts = dict:
  edit__paste = 'Ctrl+V,'
  view__zooming__zoom_in = 'Ctrl+=,'
  edit__select_all = 'Ctrl+A,'
  edit__move_to_matching_brace = 'Ctrl+],'
  settings__qt_theme__cleanlooks = 'Ctrl+F12,'
  edit__find_next = 'F3,'
  edit__find_or_replace = 'Ctrl+F,'
  edit__find_previous = 'Shift+F3,'
  file__new_file = 'Ctrl+N,'
  edit__copy = 'Ctrl+C,'
  view__zooming__zoom_out = 'Ctrl+-,'
  settings__enable_code_folding = 'Alt+F,'
  edit__redo = 'Ctrl+Y,'
  view__select_previous_file = 'Ctrl+Tab,'
  settings__qt_theme__plastique = 'Ctrl+F11,'
  file__close_file = 'Ctrl+W,'
  view__wrap_text = 'Alt+W,'
  edit__uncomment_lines = 'Ctrl+T,'
  file__open_file = 'Ctrl+O,'
  settings__qt_theme__windows = 'Ctrl+F10,'
  file__save_file = 'Ctrl+S,'
  edit__find_selection = 'Ctrl+F3,'
  edit__undo = 'Ctrl+Z,'
  edit__comment_lines = 'Ctrl+R,'
  edit__cut = 'Ctrl+X,'
  view__zooming__zoom_reset = 'Ctrl+\\,'
plugins = dict:
  top = list:
  bottom = list:
layout = dict:
  splitter2 = 400
  splitter0 = 600
  splitter1 = 400
  heigth = 700
  top = 42
  width = 900
  maximized = 0
  left = 181
"""

# create ssdf in module namespace
config = ssdf.new()
defaultConfig = ssdf.loads(defaultConfigString)


def loadConfig():
    """Load configurations, create if doesn't exist!"""
    
    # init
    filename = os.path.join(path,"config.ssdf")
    ssdf.clear(config)
    
    # load file if we can
    if os.path.isfile(filename):
        tmp = ssdf.load(os.path.join(path,"config.ssdf"))
        for key in tmp:
            config[key] = tmp[key]
    
    # fill editor keys
    if 'editor' not in config:
        config['editor'] = ssdf.new()
    for key in defaultConfig.editor:
        if key not in config.editor:
            config.editor[key] = defaultConfig.editor[key]
            
    # fill in other missing values
    for key in defaultConfig:
        if key not in config:
            config[key] = defaultConfig[key]

def saveConfig():
    """Store configurations"""
    #ssdf.save( os.path.join(path,"config.ssdf"), config )
    tmp="This function must be overridden to update the config before saving."
    raise NotImplemented(tmp)

# load on import
loadConfig()


if __name__ == "__main__":
    startIep()
    
