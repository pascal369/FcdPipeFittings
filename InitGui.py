#***************************************************************************
#*    Copyright (C) 2023 
#*    This library is free software
#***************************************************************************
import inspect
import os
import sys
import FreeCAD
import FreeCADGui

class FcdFittingsShowCommand:
    def GetResources(self):
        file_path = inspect.getfile(inspect.currentframe())
        module_path=os.path.dirname(file_path)
        return  { 
          'Pixmap': os.path.join(module_path, "icons", "FcdFittings.svg"),
          'MenuText': "FcdFittings",
          'ToolTip': "Show/Hide FcdFittings"}

    def IsActive(self):
        import Ductile
        Ductile
        return True

    def Activated(self):
        try:
          import Ductile
          Ductile.main.d.show()
        except Exception as e:
          FreeCAD.Console.PrintError(str(e) + "\n")

    def IsActive(self):
        import Ductile
        return not FreeCAD.ActiveDocument is None

class FcdFittingsWB(FreeCADGui.Workbench):
    def __init__(self):
        file_path = inspect.getfile(inspect.currentframe())
        module_path=os.path.dirname(file_path)
        self.__class__.Icon = os.path.join(module_path, "icons", "FcdFittings.svg")
        self.__class__.MenuText = "FcdFittings"
        self.__class__.ToolTip = "FcdFittings by Pascal"

    def Initialize(self):
        self.commandList = ["FcdFittings_Show"]
        self.appendToolbar("&FcdFittings", self.commandList)
        self.appendMenu("&FcdFittings", self.commandList)

    def Activated(self):
        import Ductile
        Ductile.main.d.show()
        return

    def Deactivated(self):
        return

    def ContextMenu(self, recipient):
        return

    def GetClassName(self): 
        return "Gui::PythonWorkbench"
    
FreeCADGui.addWorkbench(FcdFittingsWB())
FreeCADGui.addCommand("FcdFittings_Show", FcdFittingsShowCommand())    
