import FreeCAD as App


wire_diameter = 0.5
height = 30
central_height = 28/30*height
base_height = (height - central_height)/2
radius = 2.5
pitch = 3


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

doc = App.activeDocument()

lower = makeHelix(doc, base_height, wire_diameter, radius)
lower.Placement = App.Placement(App.Vector(0, 0, 0), App.Rotation(0, 0, 0))
lower.Label = "Lower segment"
angle = base_height/wire_diameter*360

central = makeHelix(doc, central_height, pitch, radius)
central.Placement = App.Placement(App.Vector(0, 0, base_height), App.Rotation(angle, 0, 0))
central.Label = "Central segment"
angle = central_height/pitch*360

upper = makeHelix(doc, base_height, wire_diameter, radius)
upper.Placement = App.Placement(App.Vector(0, 0, height - base_height), App.Rotation(angle, 0, 0))
upper.Label = "Upper segment"

compound = doc.addObject("Part::Compound", "springCompound")
compound.Links = [lower, central, upper,]



doc.recompute()
