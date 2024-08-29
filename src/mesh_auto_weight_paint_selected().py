import bpy

weight_armature_name = 'metarig'
anim_armature_name = 'rig_anim'

"""
Objective/Purpose
    - used to auto weight selected object with the metarig
 
To Do
    - think of a way to store data with the rig rather than the mesh
"""

import sys
import os
import importlib
sys.path.append(bpy.utils.script_paths()[2]) # change script path on blender or change this 
import _createll_script_utils
importlib.reload(_createll_script_utils)
from _createll_script_utils import (
    get_mesh_selection,
    set_armature_and_bone_name,
    get_main_object_from_object_with_name_suffix,
)

def toggle_armature_and_bone_name():
    rig_count = 0
    
    for obj in get_mesh_selection():
        if obj.modifiers.get('Armature').object.name == weight_armature_name:
            rig_count += 1
        else:
            rig_count -= 1
    
    if rig_count >= 0:
        rig_count_type = 'METARIG'
    else:
        rig_count_type = 'ANIMRIG'
    
    set_armature_and_bone_name(rig_count_type)


set_armature_and_bone_name('METARIG')

for target_mesh in get_mesh_selection():
    
    print(f"Activity: Auto-weight paint {target_mesh.name}")
    
    weight_armature = bpy.data.objects[weight_armature_name]
    anim_armature = bpy.data.objects[anim_armature_name]
    
    hide_bones = []
    hide_bones.clear()
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    main_object = get_main_object_from_object_with_name_suffix(target_mesh)
    for vgroup in main_object.vertex_groups:
        if vgroup.lock_weight and not vgroup.name.startswith('_'):
            hide_bones.append(vgroup.name)


    target_mesh.select_set(True)
    weight_armature.select_set(True)

    bpy.context.view_layer.objects.active = weight_armature
    bpy.ops.object.mode_set(mode='POSE')
    anim_armature.data.pose_position = 'REST'
    weight_armature.data.pose_position = 'REST'
    bpy.ops.pose.reveal(select=False)
    bpy.ops.pose.select_all(action='DESELECT')

    for hb in hide_bones:
        try:
            weight_armature.pose.bones[hb].bone.hide = True
            print(f"Activity: Hide pose bone {hb}")
        except KeyError:
            pass

    bpy.ops.pose.select_all(action='SELECT')

    bpy.context.view_layer.objects.active = target_mesh

    ## Remove Weights From Locked Groups

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    for hb in hide_bones:
        try:
            vg_index = target_mesh.vertex_groups[hb].index
            target_mesh.vertex_groups.active_index = vg_index
            target_mesh.vertex_groups[vg_index].lock_weight = 0
            bpy.ops.object.vertex_group_remove_from(use_all_groups=False, use_all_verts=True)
            target_mesh.vertex_groups[vg_index].lock_weight = 1
        except KeyError:
            pass

    bpy.ops.ed.undo_push(message = f"Activity: Undo Split fot {target_mesh.name}")
    print(f"Activity: Undo Split for {target_mesh.name}")
    
    print(f"Activity: Starting blender operation 'weight_from_bones' for {target_mesh.name}") # the starting and finished activity prints are just for long blender ops that we just have to trust
    
    bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
    bpy.ops.paint.weight_from_bones(type='AUTOMATIC')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    print(f"Activity: Finished blender operation 'weight_from_bones' for {target_mesh.name}")
    
    bpy.ops.ed.undo_push(message = f"Activity: Undo Split fot {target_mesh.name}")
    print(f"Activity: Undo Split for {target_mesh.name}")
    
    
    print(f"Activity: Starting blender operation 'vertex_group_smooth' for {target_mesh.name}")
    # smooth to remove some weight artifacts
    bpy.context.view_layer.objects.active = target_mesh
    target_mesh.select_set(True)
    bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
    smooth_repeat = target_mesh.get('_rigWeight_smoothRepeat', 0)
    target_mesh['_rigWeight_smoothRepeat'] = smooth_repeat
    bpy.ops.object.vertex_group_smooth(group_select_mode='BONE_DEFORM', repeat = smooth_repeat)
    bpy.ops.object.vertex_group_clean(group_select_mode='BONE_DEFORM', limit=.001)
    bpy.ops.object.mode_set(mode='OBJECT')
    print(f"Activity: Finished blender operation 'vertex_group_smooth' for {target_mesh.name}")
    
    
    bpy.ops.ed.undo_push(message = f"Activity: Undo Split fot {target_mesh.name}")
    print(f"Activity: Undo Split for {target_mesh.name}")
    
    if True: # a switch for -
        bpy.context.view_layer.objects.active = weight_armature
        bpy.ops.object.mode_set(mode='POSE')
        weight_armature.data.pose_position = 'POSE'
        anim_armature.data.pose_position = 'POSE'
    

set_armature_and_bone_name('METARIG') # rig_type = 'ANIMRIG' or 'METARIG'


print(f"-------------------------\n\nDone\n\n-------------------------")#this is just here because this script takes long change to a proper ping system