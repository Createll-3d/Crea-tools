import bpy

"""
Objective/Purpose
    - purges all helper bones in selected rig

To Do
    - use proper function names "delete_bone" is bad
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

def add_weight_via_geometry_node(target_object, parent_bone_name, helper_bone_name): # might need to change depending on you geometry node inputs
    print(f"Activity: For '{target_object.name}' Merging vertex weights of '{helper_bone_name}' to '{parent_bone_name}'")
    
    
    target_object.modifiers.new("_temp_HelperToParent", 'NODES')
    target_object.modifiers[len(target_object.modifiers)-1].node_group = bpy.data.node_groups['Util_HelperToParent']
    target_object.modifiers['_temp_HelperToParent']['Input_2'] = parent_bone_name
    target_object.modifiers['_temp_HelperToParent']['Input_3'] = helper_bone_name
        
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

    
    helper_bone = armature.data.bones.get(helper_bone_name,None)   
    
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
        
        if armature.data.bones.get(helper_bone_name):
            parent_bone = get_helper_parent(armature, helper_bone_name)
            
            if parent_bone:
                parent_bone_name = parent_bone.name        
                
                if parent_bone_name:
                    
                    if parent_bone_name.startswith('ORG-'): # just a temporary measure helper bones should be parented to the def vers
                        parent_bone_name = parent_bone_name.replace('ORG-', 'DEF-', 1)
                        
                    add_weight_via_geometry_node(object, parent_bone_name, helper_bone_name)
                    
                    vetex_group_collection_merged.append(helper_bone_name)

    missed_bones = set(vetex_group_collection) - set(vetex_group_collection_merged)
    print(f"Debug : Missed bones {missed_bones}")
    
#    if len(vetex_group_collection) > 0:
#        merge_helper_to_parent(object, armature)

def merge_facial_bones_weight_to_spine(object, spine_vertex_group_name = 'spine.006'):
    merge_collection = []
    object_vetex_groups_name = []
    
    for vertex_group in object.vertex_groups:
        object_vetex_groups_name.append(vertex_group.name)    
    
    for bone in bpy.data.objects['metarig'].data.bones:
        if bone.layers[0] or bone.layers[1] or bone.layers[2]:
            if bone.name in object_vetex_groups_name:
                merge_collection.append(bone.name)
    
    if not object.vertex_groups.get(spine_vertex_group_name, False):
        object.vertex_groups.new(name = spine_vertex_group_name)
    
    for facial_bone_name in merge_collection:
        add_weight_via_geometry_node(object, spine_vertex_group_name, facial_bone_name)
                
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
    bpy.context.view_layer.objects.active = object
    bpy.ops.object.mode_set(mode='OBJECT')
    shape_keys_vertex_positons = {}
    
    try:
        shape_keys = object.data.shape_keys.key_blocks
    except:
        return shape_keys_vertex_positons        
    
    for shape_key in shape_keys:
        if shape_key.name != "Basis": # we can just get rid of this but for safety so that the new basis doesnt get influenced by this code
            shape_keys_vertex_positons[shape_key.name] = [shape_key.data[i].co.copy() for i in range(len(shape_key.data))]
        print(f"Activity: For '{object.name}', Extrated {shape_key.name} vertex locations")
    
    
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
        
        print(f"Activity: For '{object.name}', Reconstructing {shape_key_name}")
    
    object.data.update()
    print(f"Activity: Reconstructing Shapekeys Finished for '{object.name}'")


def remove_zero_weight_vertex_groups(object, reference_armature = None, toggle_only_helper = False):

    
    print(f"Activity: Removing zero weight vertex groups")
    
    vertex_groups = object.vertex_groups[:]
    
    for vg in vertex_groups:
        
        vg_name = vg.name
        remove_group = True
        for v in object.data.vertices:
            for g in v.groups:
                if g.group == vg.index:
                    if g.weight > 0:
                        remove_group = False
                        break
            if not remove_group:
                break
            
        if remove_group:
            if toggle_only_helper and '.helper' not in vg_name:
                print(f"Debug: For {object.name}, Skipping vertex group {vg_name}")
            else:
                print(f"Activity: For {object.name}, Removing vertex group {vg_name}")
                object.vertex_groups.remove(vg)
            
        else:
            None



# =================================================================== #

create_geometry_node() #if we want it truly automated; also dont forget that we still need to mention that geometryn node

def main(objects_list):
    
    print(f"--------------------------------\nActivity: Starting {__name__}")
    
    for object in objects_list:
        
        print(f"Activity: Starting merge for {object.name}")
        
#        current_rig_state = object['_rig_name']
#        if object['_rig_name'] == 'rig_anim':
#            set_armature_and_bone_name('METARIG')
#            object['_rig_name'] == 'metarig'
#            current_rig_state = object['_rig_name']
        
        shape_key_vertex_data = extract_shape_keys_vertex_positons(object)
        clear_shapekeys(object)
        remove_zero_weight_vertex_groups(object, toggle_only_helper = True)  
        
        bpy.ops.ed.undo_push(message = f"Activity: Undo Split for {object.name}") #to prevent memory crash
        print(f"Activity: Undo Split for {object.name}")
        
        merge_helper_to_parent(object, bpy.data.objects['metarig'])
        
        
        bpy.ops.ed.undo_push(message = f"Activity: Undo Split for {object.name}") #to prevent memory crash
        print(f"Activity: Undo Split for {object.name}")
        
        remove_zero_weight_vertex_groups(object, toggle_only_helper = False)
        merge_facial_bones_weight_to_spine(object, 'spine.006')
        
        bpy.ops.ed.undo_push(message = f"Activity: Undo Split for {object.name}") #to prevent memory crash
        print(f"Activity: Undo Split for {object.name}")
        
        remove_zero_weight_vertex_groups(object, toggle_only_helper = False)
        reconstruct_shape_keys_vertex_positons(object, shape_key_vertex_data)
        
        
#        if current_rig_state != object['_rig_name']:
#            set_armature_and_bone_name(current_rig_state)
            
        bpy.ops.ed.undo_push(message = f"Activity: Undo Split fot {object.name}")
        print(f"Activity: Undo Split for {object.name}")

if __name__ == "__main__":
    
    objects_list = get_mesh_selection()
    
    if len(objects_list) < 1:
        objects_list = bpy.data.collections['Texture Bake.Upload'].all_objects
    
    main(objects_list)
    
    

        

