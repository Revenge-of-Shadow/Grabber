import FreeCAD as App


wire_diameter = 0.5
height = 30
radius = 2.5
pitch = 3
central_height = height-radius*2


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

doc = App.activeDocument()

lower = makeHook(doc, radius)
lower.Placement = App.Placement(App.Vector(0,0,radius),App.Rotation(App.Vector(-1,0,0),90))
lower.Label = "Lower hook"

central = makeHelix(doc, central_height, pitch, radius)
central.Placement = App.Placement(App.Vector(0, 0, radius), App.Rotation(0, 0, 0))
central.Label = "Central segment"
angle = central_height/pitch*360

upper = makeHook(doc, radius)
upper.Placement = App.Placement(App.Vector(0,0,height - radius), App.Rotation(angle,0,90), App.Vector(0,0,0))
upper.Label = "Upper hook"

compound = doc.addObject("Part::Compound", "springCompound")
compound.Links = [lower, central, upper,]



doc.recompute()
