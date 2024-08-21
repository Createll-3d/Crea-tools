import bpy

"""
Objective/Purpose
    - used to manage paint lines for the bleed
 
To Do
    - we could do paint lines but from on the mesh to the 
		- UV space of thae mesh with geomtery nodes
		- us plane for canvas on the UV space to reduce poly count
"""


PaintLine = "p_LineBase.007"
PaintTarget = "pants.a"

bpy.data.objects[PaintLine].modifiers["Shrinkwrap.Initial"].target = bpy.data.objects[PaintTarget]
bpy.context.object.modifiers["GN-Paint"]["Input_4"] = bpy.data.objects[PaintTarget]
bpy.data.objects[PaintLine].modifiers["Shrinkwrap.Bot"].target = bpy.data.objects[PaintTarget]
bpy.data.objects[PaintLine].modifiers["Shrinkwrap.Top"].target = bpy.data.objects[PaintTarget]