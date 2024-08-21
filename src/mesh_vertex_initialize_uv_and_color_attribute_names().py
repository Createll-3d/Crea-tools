import bpy

"""
Objective/Purpose
    - creates UV and Color attribure names on selected objects
 
To Do
    - 
"""

uv_names = ["UV - Bake + UDIM", 
            "UV - Shader - 01", 
            "UV - Shader - 02", 
            "UV - GeoNodes - 01", 
            "UV - PaintMap", 
            "UV - Decal"]
            
            
ca_names = ["CA - Edge:Root:Extra1", 
            "CA - Lit:Highlight:Add", 
            "CA - AO:TrueShadow:Subtract", 
            "CA - Mask 1:2:3", 
            "CA - Mask 2:3:4", 
            "CA - Mask 5:6:7",
            "CA - MeshOutlineWidth",
            "CA - MeshOutlineColor"]

for obj in bpy.context.selected_objects:
    i = 0
    bpy.context.view_layer.objects.active = obj
    if obj.type == 'MESH':
        while len(obj.data.uv_layers) < len(uv_names):
            bpy.ops.mesh.uv_texture_add()

        for name in uv_names:
            obj.data.uv_layers[i].name = name
            i = i+1

for obj in bpy.context.selected_objects:
    i = 0
    bpy.context.view_layer.objects.active = obj
    if obj.type == 'MESH':
        while len(obj.data.color_attributes) < len(ca_names):
            bpy.ops.geometry.color_attribute_add(name='Color', domain='CORNER', data_type='FLOAT_COLOR', color=(0.0, 0.0, 0.0, 1.0))
            #bpy.ops.geometry.attribute_add(name='Attribute', domain='CORNER', data_type='FLOAT_COLOR')
        
        for name in ca_names:
            obj.data.color_attributes[i].name = name
            i += 1
    