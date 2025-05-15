from PySide import QtCore, QtGui
import FreeCAD as App
import math
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

    def onCircleChosen(self):
        self.mode = "circle"

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
        self.setGeometry(250, 250, 320, 400)
        self.setFixedSize(320, 400)
        self.setWindowTitle("Nya")

        ##  Labels and inputs.
        validator_double = QtGui.QDoubleValidator()

        self.l_wd = QtGui.QLabel("Wire diameter [mm]:", self)
        self.l_wd.move(20, 20) 
        self.ti_wd = QtGui.QLineEdit(self)
        self.ti_wd.setValidator(validator_double)
        self.ti_wd.setText("0.5")
        self.ti_wd.setFixedWidth(80)
        self.ti_wd.move(220, 20)

        self.l_h = QtGui.QLabel("Height [mm]:", self)
        self.l_h.move(20, 70)
        self.ti_h = QtGui.QLineEdit(self)
        self.ti_h.setValidator(validator_double)
        self.ti_h.setText("30")
        self.ti_h.setFixedWidth(80)
        self.ti_h.move(220, 70)

        self.l_bh = QtGui.QLabel("Base height [mm]:", self)
        self.l_bh.move(20, 120)
        self.ti_bh = QtGui.QLineEdit(self)
        self.ti_bh.setValidator(validator_double)
        self.ti_bh.setText("2")
        self.ti_bh.setFixedWidth(80)
        self.ti_bh.move(220, 120)

        self.l_r = QtGui.QLabel("Radius [mm]:", self)
        self.l_r.move(20, 170)
        self.ti_r = QtGui.QLineEdit(self)
        self.ti_r.setValidator(validator_double)
        self.ti_r.setText("2.5")
        self.ti_r.setFixedWidth(80)
        self.ti_r.move(220, 170)

        self.l_p = QtGui.QLabel("Pitch [mm]:", self)
        self.l_p.move(20, 220)
        self.ti_p = QtGui.QLineEdit(self)
        self.ti_p.setValidator(validator_double)
        self.ti_p.setText("3")
        self.ti_p.setFixedWidth(80)
        self.ti_p.move(220, 220)
        ##  Labels and inputs end.

        ##  Additional options.
        
        self.rb_flat = QtGui.QRadioButton("flat end", self)
        self.rb_flat.clicked.connect(self.onFlatChosen)
        self.rb_flat.toggle()
        self.rb_flat.move(20, 280)

        self.rb_hook = QtGui.QRadioButton("hook end", self)
        self.rb_hook.clicked.connect(self.onHookChosen)
        self.rb_hook.move(210, 280)

        self.rb_hook = QtGui.QRadioButton("circle end", self)
        self.rb_hook.clicked.connect(self.onCircleChosen)
        self.rb_hook.move(120, 310)
        ##  Additional options end.


        ##  Confirm/Cancel buttons.
        bt_cancel = QtGui.QPushButton("Cancel", self)
        bt_cancel.clicked.connect(self.onCancel)
        bt_cancel.move(20, 350)

        bt_ok = QtGui.QPushButton("Make the spring", self)
        bt_ok.clicked.connect(self.onOk)
        bt_ok.setAutoDefault(True)
        bt_ok.move(190, 350)
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

def makeCircle(doc, radius, wire_diameter = 0.5):
    body = doc.addObject("Part::Torus", "Torus")

    body.Radius1 = radius
    body.Radius2 = wire_diameter/2
    body.Angle1 = -180
    body.Angle2 = 180
    body.Angle3 = 360

    return body
##  FreeCAD object functions end


if(form.success):
    ##  Get input
    wire_diameter = float(form.ti_wd.text())
    radius = float(form.ti_r.text())
    height = float(form.ti_h.text())
    base_height = float(form.ti_bh.text())
    pitch = float(form.ti_p.text())
    ##  Input values end 

    base_rotation = base_height/wire_diameter*360
    radius = radius - wire_diameter/2

    doc = App.activeDocument()
    
    links = []

    ##  Hooked spring
    if(form.mode == "hook"):
        center_height = height-(radius+base_height)*2
        center_rotation = center_height/pitch*360

        lower_hook = makeHook(doc, radius, wire_diameter)
        lower_hook.Placement = App.Placement(App.Vector(0,0,radius),App.Rotation(App.Vector(-1,0,0),90))
        lower_hook.Label = "Lower hook"
        links.append(lower_hook)

        lower_placement = App.Placement(App.Vector(0, 0, radius), 
                                        App.Rotation(0, 0, 0))
        center_placement = App.Placement(App.Vector(0, 0, radius+base_height), 
                                         App.Rotation(base_rotation, 0, 0))
        upper_placement = App.Placement(App.Vector(0, 0, radius+base_height+center_height), 
                                        App.Rotation(base_rotation+center_rotation, 0, 0))

        upper_hook = makeHook(doc, radius, wire_diameter)
        upper_hook.Placement = App.Placement(App.Vector(0, 0, radius+base_height+center_height+base_height), 
                                             App.Rotation(base_rotation+center_rotation+base_rotation, 0, 90), App.Vector(0,0,0))
        upper_hook.Label = "Upper hook"
        links.append(upper_hook)

    ##  Circle end
    elif(form.mode == "circle"):
        center_height = height-(radius*2+base_height)*2
        center_rotation = center_height/pitch*360

        lower_circle = makeCircle(doc, radius, wire_diameter)
        lower_circle.Placement = App.Placement(App.Vector(radius,0,radius),
                                               App.Rotation(90,0,90))
        lower_circle.Label = "Lower circle"
        links.append(lower_circle)

        lower_placement = App.Placement(App.Vector(0, 0, radius*2), 
                                        App.Rotation(0, 0, 0))
        center_placement = App.Placement(App.Vector(0, 0, radius*2+base_height), 
                                         App.Rotation(base_rotation, 0, 0))
        upper_placement = App.Placement(App.Vector(0, 0, radius*2+base_height+center_height), 
                                        App.Rotation(base_rotation+center_rotation, 0, 0))

        upper_circle = makeCircle(doc, radius, wire_diameter)
        upper_circle.Placement = App.Placement(App.Vector(radius*math.cos((base_rotation+center_rotation+base_rotation)/180*math.pi), radius*math.sin((base_rotation+center_rotation+base_rotation)/180*math.pi), radius*2+base_height+center_height+base_height+radius), 
                                               App.Rotation(base_rotation+center_rotation+base_rotation+90, 0, 90), 
                                               App.Vector(0,0,0))
        upper_circle.Label = "Upper circle"
        links.append(upper_circle)
        
    ##  Flat-end spring as default
    else:
        center_height = height-(base_height)*2
        center_rotation = center_height/pitch*360

        lower_placement = App.Placement(App.Vector(0, 0, 0), App.Rotation(0, 0, 0))
        center_placement = App.Placement(App.Vector(0, 0, base_height), App.Rotation(base_rotation, 0, 0))
        upper_placement = App.Placement(App.Vector(0, 0, base_height+center_height), App.Rotation(base_rotation+center_rotation, 0, 0))
    ##  Spring end creation end
    

    ##  Spring center segment (common for all spring types)
    center = makeHelix(doc, center_height, pitch, radius, wire_diameter)
    center.Placement = center_placement
    center.Label = "Central segment"
    links.append(center) 
    ##  Spring center end
    
    
    ##  If possible, add spring base segments
    if(base_height >= wire_diameter):
        lower = makeHelix(doc, base_height, wire_diameter, radius, wire_diameter)
        lower.Placement = lower_placement
        lower.Label = "Lower segment"
        links.append(lower)
        upper = makeHelix(doc, base_height, wire_diameter, radius, wire_diameter)
        upper.Placement = upper_placement
        upper.Label = "Upper segment"
        links.append(upper)
    ##  Spring base segments end


    compound = doc.addObject("Part::Compound", "springCompound")
    compound.Links = links 


    doc.recompute()

'''                             Modelling code end                          '''
##===========================================================================##
