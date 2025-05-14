from PySide import QtCore, QtGui
import FreeCAD as App
##===========================================================================##
'''                         Graphical user interface code                   '''
class GuiClass(QtGui.QDialog):
    def __init__(self):
        super(GuiClass, self).__init__()
        self.initUI()

    ##  Event handler methods
    def onFlatChosen(self):
        self.mode = "flat"

    def onHookChosen(self):
        self.mode = "hook"

    def onOk(self):
        self.success = True
        self.close()

    def onCancel(self):
        self.success = False
        self.close()
    ##  Event handler methods end


    def initUI(self): 
        self.success = False
        self.mode = "flat"
        self.setGeometry(250, 250, 320, 320)
        self.setWindowTitle("Nya")

        ##  Labels and inputs.
        validator_double = QtGui.QDoubleValidator()

        self.l_wd = QtGui.QLabel("Wire diameter:", self)
        self.l_wd.move(20, 20) 
        self.ti_wd = QtGui.QLineEdit(self)
        self.ti_wd.setValidator(validator_double)
        self.ti_wd.setText("0.5")
        self.ti_wd.setFixedWidth(80)
        self.ti_wd.move(220, 20)

        self.l_h = QtGui.QLabel("Height:", self)
        self.l_h.move(20, 70)
        self.ti_h = QtGui.QLineEdit(self)
        self.ti_h.setValidator(validator_double)
        self.ti_h.setText("30")
        self.ti_h.setFixedWidth(80)
        self.ti_h.move(220, 70)

        self.l_r = QtGui.QLabel("Radius:", self)
        self.l_r.move(20, 120)
        self.ti_r = QtGui.QLineEdit(self)
        self.ti_r.setValidator(validator_double)
        self.ti_r.setText("2.5")
        self.ti_r.setFixedWidth(80)
        self.ti_r.move(220, 120)

        self.l_p = QtGui.QLabel("Pitch:", self)
        self.l_p.move(20, 170)
        self.ti_p = QtGui.QLineEdit(self)
        self.ti_p.setValidator(validator_double)
        self.ti_p.setText("3")
        self.ti_p.setFixedWidth(80)
        self.ti_p.move(220, 170)
        ##  Labels and inputs end.

        ##  Additional options.
        
        self.rb_flat = QtGui.QRadioButton("flat end", self)
        self.rb_flat.clicked.connect(self.onFlatChosen)
        self.rb_flat.toggle()
        self.rb_flat.move(20, 220)

        self.rb_hook = QtGui.QRadioButton("hook end", self)
        self.rb_hook.clicked.connect(self.onHookChosen)
        self.rb_hook.move(210, 220)
        ##  Additional options end.


        ##  Confirm/Cancel buttons.
        bt_cancel = QtGui.QPushButton("Cancel", self)
        bt_cancel.clicked.connect(self.onCancel)
        bt_cancel.move(20, 280)

        bt_ok = QtGui.QPushButton("Make the spring", self)
        bt_ok.clicked.connect(self.onOk)
        bt_ok.setAutoDefault(True)
        bt_ok.move(190, 280)
        ##  Confirm/Cancel buttons end.


        self.show()

form = GuiClass()
form.exec()
'''                         Graphical user interface end                    '''
##===========================================================================##

##===========================================================================##
'''                             Modelling code                              '''
##  FreeCAD object functions
def makeHelix(doc, height, pitch, radius, wire_diameter = 0.5):
    body = doc.addObject('PartDesign::Body','springBody')
    
    circle_sketch = body.newObject('Sketcher::SketchObject', 'circleSketch')
    circle_sketch.AttachmentSupport = (doc.getObject('XZ_Plane'),[''])
    circle_sketch.MapMode = 'FlatFace'

    geoList = []
    geoList.append(Part.Circle(App.Vector(radius, 0, 0), App.Vector(0, 0, 1), wire_diameter/2))
    circle_sketch.addGeometry(geoList,False)
    del geoList

    helix = body.newObject('PartDesign::AdditiveHelix','AdditiveHelix')
    helix.Profile = (circle_sketch, ['',])
    helix.ReferenceAxis = (circle_sketch,['V_Axis'])

    helix.Mode = 0
    helix.Pitch = pitch
    helix.Height = height
    helix.Turns = height/pitch
    helix.Angle = 0
    helix.Growth = 0
    helix.LeftHanded = 0
    helix.Reversed = 0

    return body

def makeHook(doc, radius, wire_diameter = 0.5):
    body = doc.addObject("Part::Torus", "Torus")

    body.Radius1 = radius
    body.Radius2 = wire_diameter/2
    body.Angle1 = -180
    body.Angle2 = 180
    body.Angle3 = 150

    return body
##  FreeCAD object functions end


if(form.success):
    wire_diameter = float(form.ti_wd.text())
    radius = float(form.ti_r.text())
    height = float(form.ti_h.text())
    pitch = float(form.ti_p.text())

    doc = App.activeDocument()
    
    ##  Hooked spring
    if(form.mode == "hook"):
        central_height = height-radius*2

        lower = makeHook(doc, radius, wire_diameter)
        lower.Placement = App.Placement(App.Vector(0,0,radius),App.Rotation(App.Vector(-1,0,0),90))

        central = makeHelix(doc, central_height, pitch, radius, wire_diameter)
        central.Placement = App.Placement(App.Vector(0, 0, radius), App.Rotation(0, 0, 0))
        
        angle = central_height/pitch*360

        upper = makeHook(doc, radius, wire_diameter)
        upper.Placement = App.Placement(App.Vector(0,0,height - radius), App.Rotation(angle,0,90), App.Vector(0,0,0))
        
    ##  Flat-end spring as default
    else:
        central_height = 28/30*height
        base_height = (height-central_height)/2

        lower = makeHelix(doc, base_height, wire_diameter, radius, wire_diameter)
        lower.Placement = App.Placement(App.Vector(0, 0, 0), App.Rotation(0, 0, 0))
        angle = base_height/wire_diameter*360

        central = makeHelix(doc, central_height, pitch, radius, wire_diameter)
        central.Placement = App.Placement(App.Vector(0, 0, base_height), App.Rotation(angle, 0, 0))
        angle = central_height/pitch*360

        upper = makeHelix(doc, base_height, wire_diameter, radius, wire_diameter)
        upper.Placement = App.Placement(App.Vector(0, 0, height - base_height), App.Rotation(angle, 0, 0))

    lower.Label = "Lower segment"
    central.Label = "Central segment"
    upper.Label = "Upper segment"
    compound = doc.addObject("Part::Compound", "springCompound")
    compound.Links = [lower, central, upper,]

    doc.recompute()

'''                             Modelling code end                          '''
##===========================================================================##
