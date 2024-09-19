import bpy

for object in bpy.data.collections['Texture Bake.Upload'].all_objects:
    if object.modifiers.get('Armature', False):
        try:
            #object.modifiers['Armature'].object = bpy.data.objects['metarig']
            object.modifiers['Armature'].object = bpy.data.objects['rig_game']
        except:
            None
