import Part
import math
from FreeCAD import Base


inner_r = 6.0/2.0
inner_R = inner_r * (5.0/3.0)   #   Calculated from example.
outer_R = 17.0/2.0
outer_r = outer_R * (3.0/4.0)   #   Calculated from example.

thick = 6.0
ball_amount = 10
ball_r = (outer_R-inner_r)/4
fillet_r = 0.1

# Ball center as offset.
ball_hoffset = ((outer_r - inner_R)/2 + inner_R)
ball_voffset = thick / 2


App.newDocument("Unnamed")
App.setActiveDocument("Unnamed")
App.ActiveDocument = App.getDocument("Unnamed")
Gui.ActiveDocument = Gui.getDocument("Unnamed")


# Inner ring.
cyl_cutout = Part.makeCylinder(inner_r, thick)
cyl_inner = Part.makeCylinder(inner_R, thick)
tube_inner = cyl_inner.cut(cyl_cutout) 

# Extra shaping.
ti_edges = tube_inner.Edges
ti_fillet = tube_inner.makeFillet(fillet_r, ti_edges)


# Outer ring.
cyl_cutout_outer = Part.makeCylinder(outer_r, thick)
cyl_outer = Part.makeCylinder(outer_R, thick)
tube_outer = cyl_outer.cut(cyl_cutout_outer)

# Extra shaping.
to_edges = tube_outer.Edges
to_fillet = tube_outer.makeFillet(fillet_r, to_edges)


# Groove.
tor = Part.makeTorus(ball_hoffset, ball_r)
tor.translate(Base.Vector(0,0,ball_voffset))

# Subtract the groove and show
ring_inner = ti_fillet.cut(tor)
Part.show(ring_inner)

ring_outer = to_fillet.cut(tor)
Part.show(ring_outer)



# The balls.
for i in range(ball_amount):
    ball = Part.makeSphere(ball_r)
    angle = (i*2*math.pi)/ball_amount
    ball_placement = (ball_hoffset*math.cos(angle), ball_hoffset*math.sin(angle), ball_voffset)
    ball.translate(ball_placement)
    Part.show(ball)



App.activeDocument().recompute()
Gui.activeDocument().activeView().viewAxometric()
Gui.SendMsgToActiveView("ViewFit")
