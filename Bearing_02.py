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



o_line_1 = Part.makeLine((outer_R, 0, thick - fillet_r), (outer_R, 0, fillet_r))
o_line_2 = Part.makeLine((outer_R - fillet_r, 0, 0), (outer_r+fillet_r, 0, 0))
o_line_3 = Part.makeLine((outer_r, 0, fillet_r), (outer_r, 0, thick - fillet_r))
o_line_4 = Part.makeLine((outer_r + fillet_r, 0, thick), (outer_R-fillet_r, 0, thick))

o_rnding_1 = Part.makeCircle(fillet_r, Base.Vector(outer_R - fillet_r, 0, fillet_r), Base.Vector(0, 1, 0), 0, 90)
o_rnding_2 = Part.makeCircle(fillet_r, Base.Vector(outer_r + fillet_r, 0, fillet_r), Base.Vector(0, 1, 0), 90, 180)
o_rnding_3 = Part.makeCircle(fillet_r, Base.Vector(outer_r + fillet_r, 0, thick - fillet_r), Base.Vector(0, 1, 0), 180, 270)
o_rnding_4 = Part.makeCircle(fillet_r, Base.Vector(outer_R - fillet_r, 0, thick - fillet_r), Base.Vector(0, 1, 0), 270, 360)

o_wire = Part.Wire([o_line_1, o_rnding_1, o_line_2, o_rnding_2, o_line_3, o_rnding_3, o_line_4, o_rnding_4])
o_wire = Part.Face(o_wire)
o_wire = o_wire.revolve(Base.Vector(0, 0, 1), Base.Vector(0, 0, 360))
o_circle = Part.makeCircle(ball_r, Base.Vector(ball_hoffset, 0, ball_voffset), Base.Vector(0, 1, 0), 0, 360)
o_circwire = Part.Wire([o_circle])
o_circwire = Part.Face(o_circwire)
o_circwire = o_circwire.revolve(Base.Vector(0, 0, 1), Base.Vector(0, 0, 360))
o_wire = o_wire.cut(o_circwire)
Part.show(o_wire)



i_line_1 = Part.makeLine((inner_R, 0, thick - fillet_r), (inner_R, 0, fillet_r))
i_line_2 = Part.makeLine((inner_R - fillet_r, 0, 0), (inner_r+fillet_r, 0, 0))
i_line_3 = Part.makeLine((inner_r, 0, fillet_r), (inner_r, 0, thick - fillet_r))
i_line_4 = Part.makeLine((inner_r + fillet_r, 0, thick), (inner_R - fillet_r, 0, thick))

i_rnding_1 = Part.makeCircle(fillet_r, Base.Vector(inner_R - fillet_r, 0, fillet_r), Base.Vector(0, 1, 0), 0, 90)
i_rnding_2 = Part.makeCircle(fillet_r, Base.Vector(inner_r + fillet_r, 0, fillet_r), Base.Vector(0, 1, 0), 90, 180)
i_rnding_3 = Part.makeCircle(fillet_r, Base.Vector(inner_r + fillet_r, 0, thick - fillet_r), Base.Vector(0, 1, 0), 180, 270)
i_rnding_4 = Part.makeCircle(fillet_r, Base.Vector(inner_R - fillet_r, 0, thick - fillet_r), Base.Vector(0, 1, 0), 270, 360)

i_wire = Part.Wire([i_line_1, i_rnding_1, i_line_2, i_rnding_2, i_line_3, i_rnding_3, i_line_4, i_rnding_4])
i_wire = Part.Face(i_wire)
i_wire = i_wire.revolve(Base.Vector(0, 0, 1), Base.Vector(0, 0, 360))
i_circle = Part.makeCircle(ball_r, Base.Vector(ball_hoffset, 0, ball_voffset), Base.Vector(0, 1, 0), 0, 360)
i_circwire = Part.Wire([i_circle])
i_circwire = Part.Face(i_circwire)
i_circwire = i_circwire.revolve(Base.Vector(0, 0, 1), Base.Vector(0, 0, 360))
i_wire = i_wire.cut(i_circwire)
Part.show(i_wire)


for i in range(ball_amount):
    ball = Part.makeSphere(ball_r)
    angle = (i*2*math.pi)/ball_amount
    ball_placement = (ball_hoffset*math.cos(angle), ball_hoffset*math.sin(angle), ball_voffset)
    ball.translate(ball_placement)
    Part.show(ball)

App.ActiveDocument.recompute()
Gui.ActiveDocument.ActiveView.viewAxometric()
Gui.SendMsgToActiveView("ViewFit")
