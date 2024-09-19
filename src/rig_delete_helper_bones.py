import bpy

"""
Objective/Purpose
    - purges all helper bones in selected rig

To Do
    - use proper names "delete_bone" is bad
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

def delete_helper_bone(armature):
    for layer in range(len(armature.data.layers)):
        armature.data.layers[layer] = True
        
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

def delete_rig_by_name(rig_name):
    if bpy.data.objects.get(rig_name, False):
        rig_object = bpy.data.objects[rig_name]
        rig_armature = bpy.data.objects[rig_name].data
        
        bpy.data.objects.remove(rig_object)
        bpy.data.armatures.remove(rig_armature)

def duplicate_rig(source_rig, copy_name):
    bpy.context.view_layer.objects.active = source_rig
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = source_rig
    source_rig.select_set(True)
    
    if not bpy.data.objects.get(source_rig.name + '.001', False):
        bpy.ops.object.duplicate()
    
    if bpy.data.objects.get(source_rig.name + '.001', False):
        copy_object = bpy.data.objects.get(source_rig.name + '.001')
        copy_object.name = copy_name
        copy_object.data.name = copy_name
        
        return copy_object

def delete_facial_bones(armature):
    for layer in range(len(armature.data.layers)):
        armature.data.layers[layer] = True
        
    delete_bone_name_lists = []
    bpy.ops.object.mode_set(mode='OBJECT') # Context switching to prevent un-updated data
    for bone in armature.data.bones:
        if bone.layers[0] or bone.layers[1] or bone.layers[2]:
            delete_bone_name_lists.append(bone.name)
    
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='DESELECT')
    
    for bone_name in delete_bone_name_lists:
        armature.data.bones[bone_name].select = True
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.delete()
    bpy.ops.object.mode_set(mode='OBJECT')

    

### Execution ###

def main():
    
    source_rig = bpy.data.objects['metarig']
    delete_rig_by_name('rig_game')
    
    game_rig = duplicate_rig(source_rig, 'rig_game')
    delete_helper_bone(game_rig)
    delete_facial_bones(game_rig)

if __name__ == "__main__":
    main()
        
    
