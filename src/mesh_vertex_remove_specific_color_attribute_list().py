import bpy
 
"""
Objective/Purpose
    - was used when we messed up
 
To Do
    - not really used much maybe deadge
"""
 
 
ca_names = ["CA - Edge:Root:Extra1", 
            "CA - Lit:Highlight:Add", 
            "CA - AO:TrueShadow:Subtract", 
            "CA - Mask 1:2:3", 
            "CA - Mask 2:3:4", 
            "CA - Mask 5:6:7"]

for obj in bpy.context.selected_objects:
    i = 0
    bpy.context.view_layer.objects.active = obj
    while len(obj.data.color_attributes) > 0:
        bpy.ops.geometry.color_attribute_remove()
    