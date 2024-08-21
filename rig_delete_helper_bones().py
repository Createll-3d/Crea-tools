import bpy

"""
Objective/Purpose
    - purges all helper bones in selected rig

To Do
    - use proper names lmao "delete_bone" is bad
"""

def get_armature_selection():
    selected_armatures = []
    for obj in bpy.context.selected_objects:
        if obj.type == 'ARMATURE':
            selected_armatures.append(obj)
    return selected_armatures

def get_armature_users(armature):
    # if we want it fully autoamted
    return

def delete_bone(armature):
    delete_bone_name_lists = []
    bpy.ops.object.mode_set(mode='OBJECT') # Context switching to prevent un-updated data
    for bone in armature.data.bones:
        if 'helper' in bone.name:
            delete_bone_name_lists.append(bone.name)
    
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='DESELECT')
    for bone_name in delete_bone_name_lists:
        armature.data.bones[bone_name].select = True
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.delete()
    bpy.ops.object.mode_set(mode='OBJECT')
     
### Execution ###

for armature in get_armature_selection():
    delete_bone(armature)
        
    
