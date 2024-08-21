import bpy

"""
Objective/Purpose
    - used to sync the the selected UV on diifferent objects
 
To Do
    - close to be depreciated because of Zen UV
"""



UV_active = bpy.context.active_object.data.uv_layers.active_index
CA_active = bpy.context.active_object.data.attributes.active_color_index

for obj in bpy.context.selected_objects:
 
    if obj.type == 'MESH':
        obj.data.uv_layers.active_index = UV_active
        obj.data.attributes.active_color_index = CA_active
