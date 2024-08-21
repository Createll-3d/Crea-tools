import bpy

"""
Objective/Purpose
    - purges all helper bones in selected rig

To Do
    - use proper names lmao "delete_bone" is bad
"""

import sys
import os
import importlib
sys.path.append(bpy.utils.script_paths()[2]) # change script path on blender or change this 
import _createll_script_utils
importlib.reload(_createll_script_utils)
from _createll_script_utils import (
    # only import whats necessary
    set_armature_and_bone_name, #(rig_type, weight_armature = bpy.data.armatures['metarig'], anim_armature = bpy.data.armatures['rig_anim'], mesh_lists = get_mesh_selection()):
    
)


def create_geometry_node():
    return

def get_mesh_selection():
    selected_objects = []
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            selected_objects.append(obj)
    return selected_objects

def add_weight_via_geometry_node(target_object, parent_bone_name, helper_bone_name):
    print(helper_bone_name + "->" + parent_bone_name)
    
    
    target_object.modifiers.new("_temp_HelperToParent", 'NODES')
    target_object.modifiers[len(target_object.modifiers)-1].node_group = bpy.data.node_groups['Util_HelperToParent']
    target_object.modifiers['_temp_HelperToParent']['Input_2'] = parent_bone_name
    target_object.modifiers['_temp_HelperToParent']['Input_3'] = helper_bone_name
        
    # Set-up Context
    bpy.context.view_layer.objects.active = target_object
    target_object.select_set(True)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Apply
    bpy.ops.object.modifier_move_to_index(modifier="_temp_HelperToParent", index=0)
    if target_object.active_shape_key:
        bpy.ops.gret.shape_key_apply_modifiers(modifier_mask=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    else:
        bpy.ops.object.modifier_apply(modifier="_temp_HelperToParent")

def get_helper_parent(armature, helper_bone_name):

    helper_bone = armature.data.bones.get(helper_bone_name)
    
    # Print the bone for debugging
   
    
    if helper_bone:
        if 'helper' in helper_bone.name:
            if helper_bone.parent:
                return get_helper_parent(armature, helper_bone.parent.name)
            else:
                print(f"Bone '{helper_bone_name}' has no parent.")
                return None
        else:
            return helper_bone
    else:
        return None

def merge_helper_to_parent(object, armature = None):
    if armature is None:
        try:
            armature = object.modifiers['Armature'].object
        except:
            raise print(f"{object.name} has no armature")
    vetex_group_collection = []
    vetex_group_collection_merged = []
    for vertex_group in object.vertex_groups: # Might look redundant but removing will cause a decoding error -> suspected cause -> geometry node function reorders vertex groups in memory (?) 
        if 'helper' in str(vertex_group):
            vetex_group_collection.append(vertex_group.name)
    
    for helper_bone_name in vetex_group_collection:
        
        print(f"Activity: Getting Parent of {helper_bone_name} ")
        parent_bone_name = get_helper_parent(armature, helper_bone_name).name        
        
        if parent_bone_name:
            print(f"Activity: {helper_bone_name} to {parent_bone_name}")
            if parent_bone_name.startswith('ORG-'): # just a temporary measure helper bones should be parented to the def vers
                parent_bone_name = parent_bone_name.replace('ORG-', 'DEF-', 1)
                
            add_weight_via_geometry_node(object, parent_bone_name, helper_bone_name)
            
            vetex_group_collection_merged.append(helper_bone_name)
    
    missed_bones = set(vetex_group_collection) - set(vetex_group_collection_merged)
    print(missed_bones)
    
#    if len(vetex_group_collection) > 0:
#        merge_helper_to_parent(object, armature)

                
def clear_shapekeys(object):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = object
    object.select_set(True)
    
    try:
        bpy.ops.object.shape_key_remove(all=True)
    except:
        None
    
    object.select_set(False)

def extract_shape_keys_vertex_positons(object):
    bpy.ops.object.mode_set(mode='OBJECT')
    shape_keys_vertex_positons = {}
    
    try:
        shape_keys = object.data.shape_keys.key_blocks
    except:
        return shape_keys_vertex_positons        
    
    for shape_key in shape_keys:
        if shape_key.name != "Basis": # we can just get rid of this but for safety so that the new basis doesnt get influenced by this code
            shape_keys_vertex_positons[shape_key.name] = [shape_key.data[i].co.copy() for i in range(len(shape_key.data))]
        print(f"Activity: Extrated {shape_key.name} vertex locations")
    
    
    return shape_keys_vertex_positons

def reconstruct_shape_keys_vertex_positons(object, vertex_data):
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # incase we dicide to also get Basis from original state mesh
    if "Basis" in vertex_data:
        for i, vertex_location in enumerate(vertex_data["Basis"]):
            basis_shape_key_data[i].co = vertex_location
    else:
        bpy.context.view_layer.objects.active = object
        object.select_set(True)
        bpy.ops.object.shape_key_add(from_mix=False)
        object.select_set(False)
       

    for shape_key_name, vertices in vertex_data.items():
        if shape_key_name != "Basis":
            new_shape_key = object.shape_key_add(name=shape_key_name, from_mix=False)
            shape_key_data = new_shape_key.data
            
            for i, vertex_location in enumerate(vertices):
                shape_key_data[i].co = vertex_location
        
        print(f"Activity: Reconstructing {shape_key_name}")
    
    object.data.update()
    print(f"Activity: Reconstructing Shapekeys Finished")

# =================================================================== #

print(f"--------------------------------\nActivity: Starting")
create_geometry_node() #if we want it truly automated; also dont forget that we still need to mention that geometryn node


selected_objects = get_mesh_selection()
for object in selected_objects:
    if object['_rig_name'] == 'rig_anim':
        current_rig_state = object[_rig_name]
        set_armature_and_bone_name('METARIG')
    
    shape_key_vertex_data = extract_shape_keys_vertex_positons(object)
    clear_shapekeys(object)
    merge_helper_to_parent(object)
    reconstruct_shape_keys_vertex_positons(object, shape_key_vertex_data)
    
    if current_rig_state != object['_rig_name']:
        set_armature_and_bone_name(current_rig_state)


