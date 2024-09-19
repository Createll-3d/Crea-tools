import bpy

"""
Objective/Purpose
    - for an intermediary scene for testing and to reduce lag
    - Duplicates the weight mesh collection to a target arkit mesh collection

To Do
    - handle missing scene
    - handle missing collection
    - more robust initialize same with the other copy related stuff
    - unlink pose on armature before start
    - need to create scene if none
    - an actual class ? or centralized copy system
    - main
        - manual for now : create scene
        - manual for now : create target collection
        - create game rig
            - just delete all metarig helper bones ?
            - missing twist bones though ... so we use anim rig ? and just take deform and remove DEF name ?
                - wait do we even have twist bones ? for the meta to use for auto weight
        - set to metarig
        - clean modifiers
            - maybe use a custom one ? or a more robust clean modifiers
        - duplicate
        - merge helper bones
            - merge to this
        - merge facial bones
            - merge to this
        - apply game rig modifier
    - have it so that the final gets merged and ready to upload in the upload scene
        - all modifications should be in the final state
            - weights, UDIMs, etc.
"""

import sys
import os
import importlib

sys.path.append(bpy.utils.script_paths()[2])
import _createll_script_utils
importlib.reload(_createll_script_utils)
from _createll_script_utils import (
    get_mesh_selection,
    set_object_active, 
    link_object_to_collection, 
    duplicate_mesh_object, 
    apply_modifiers_via_gret,
    apply_modifiers_till_modifier_type_via_gret,
    link_collections_to_scene,
    clean_mesh_modifiers,
    create_armature_modifier,
    create_surface_deform_modifier,
    set_armature_and_bone_name,
)

sys.path.append(os.path.join(bpy.utils.script_paths()[2],'src'))
import mesh_weight_helper_to_parent
mesh_weight_helper_main = mesh_weight_helper_to_parent.main

######

def clear_material(object):
    print(f"Activity: {object.name} | Clear materials")
    
    if not object.get('_bakeTextureGroup',False):
        try:
            object['_bakeTextureGroup'] = object.data.materials[0].name
        except:
            None
    
    object.data.materials.clear()
    

def link_material(object, material_name):
    print(f"Activity: {object.name} | link material to {material_name}")
    
    if not bpy.data.materials.get(material_name, False):
        material = bpy.data.materials.new(material_name)
        material.use_fake_user = True
    else:
        material = bpy.data.materials.get(material_name)
    
    if len(object.data.materials) == 0:
        object.data.materials.append(material)
    elif material not in object.data.materials:
        object.data.materials.append(material)
    else:
        None

def strip_name_after_keyword(name, keywords, keep_keyword = False):
    keyword_index = -1
    for keyword in keywords:
        if name.find(keyword) != -1:
            if keyword_index == -1:
                keyword_index = name.find(keyword)
            elif name.find(keyword) < keyword_index:
                keyword_index = name.find(keyword)
    if keyword_index != -1:
        return name[:keyword_index + (len(keyword) * keep_keyword )]
    else:
        return name

def create_vertex_group(object, vertex_group_name, vertex_weight = 1):
    print(f"Activity: {object.name} | Create vertex group '{vertex_group_name}'")
    
    if not object.vertex_groups.get(vertex_group_name, False):
        object.vertex_groups.new(name = vertex_group_name)
    
    vindex = object.vertex_groups[vertex_group_name].index
    
    object.vertex_groups.active_index = vindex
    
    bpy.context.view_layer.objects.active = object
    object.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.context.scene.tool_settings.vertex_group_weight = vertex_weight
    bpy.ops.object.vertex_group_assign()
    bpy.ops.object.mode_set(mode='OBJECT')
    
def delete_mesh_by_vertex_group_mask(object, vertex_group_name):
    
    
    if not object.vertex_groups.get(vertex_group_name, False):
        return
    
    print(f"Activity: {object.name} | Delete vertices by vertex mask '{vertex_group_name}'")
    vindex = object.vertex_groups[vertex_group_name].index
    
    object.vertex_groups.active_index = vindex
    bpy.context.view_layer.objects.active = object
    object.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_select()
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT')
    
def join_mesh(objects_list, joined_name, link_to_collection = None):
    if link_to_collection == None:
        link_to_collection = objects_list[0].users_collection[0]
    
    bpy.context.view_layer.objects.active = objects_list[0]
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    
    mask_vertex_group_list = []
    for object in objects_list:
        
        
        object.select_set(True)
        
        object_name_stripped = strip_name_after_keyword(object.name, [".ARkit",".Final",".Upload"]) # update to final when were golden
        mask_vertex_group = "mesh_" + object_name_stripped
        
        print(f"Activity: {object.name} | Create mesh mask vertex groups  to {mask_vertex_group}")
        
        create_vertex_group(object, mask_vertex_group, 1)
        
        mask_vertex_group_list.append(mask_vertex_group)
        
    print(f"Activity: Create Object '{joined_name}'")
    if bpy.data.meshes.get(joined_name,False): 
        joined_mesh = bpy.data.meshes.get(joined_name)
    else:
        joined_mesh = bpy.data.meshes.new(joined_name)             
    
    if bpy.data.objects.get(joined_name,False):
        joined_object = bpy.data.objects.get(joined_name) # if existing make it so it only deletes the mesh thats contested # we might need to rely on the vertex group mesh mask
    else:
        joined_object = bpy.data.objects.new(joined_name, object_data = joined_mesh) 

    try:
        link_to_collection.objects.link(joined_object)
    except:
        None

    for vertex_group in mask_vertex_group_list:
        delete_mesh_by_vertex_group_mask(joined_object, vertex_group)

    
    print(f"Activity: Blender operatation 'join' of '{joined_name}' from {objects_list}")
    bpy.context.view_layer.objects.active = joined_object
    joined_object.select_set(True)
    bpy.ops.object.join()
    
    
    return joined_object

def get_object_dictionary_by_property_name(objects_list, property_name):
    object_dictionary = {}
    skipped_objects = []
    
    for object in objects_list:
        if object.get(property_name, False):
            if not object_dictionary.get(object[property_name], False):
                object_dictionary[object[property_name]] = []
            
            object_dictionary[object[property_name]].append(object)
        else:
            skipped_objects.append(object.name)
    
    return object_dictionary
    print(f"Activity: Dictionary by Property Name: {join_mesh_lists}")
    print(f"Debug: Skipped objects for 'dictionary': {skipped_objects}")

def duplicate_mesh_object_lists(objects_list):# add a mesh check              
    bpy.context.view_layer.objects.active = objects_list[0]
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    
    for object in objects_list:
        object.select_set(True)
    
    print(f"Activity: Blender operation 'duplicate' for {objects_list}")
    bpy.ops.object.duplicate()
    
    duplicated_lists = bpy.context.selected_objects
    
    return duplicated_lists


def main():
    objects_main_list = get_mesh_selection()
    if len(objects_main_list) < 1:
        objects_main_list = bpy.data.collections['Texture Bake.Upload'].all_objects
    

    join_mesh_dict = get_object_dictionary_by_property_name(objects_main_list, '_uploadMeshGroup')

    print(join_mesh_dict)

    for joined_object_name, objects_list in join_mesh_dict.items():
        objects_list = duplicate_mesh_object_lists(objects_list)
        for object in objects_list:
            clear_material(object)
            link_material(object, object['_bakeTextureGroup'] + "_Final")
            clean_mesh_modifiers(object,['OH_OUTLINE','Set_Mesh_Outline_Weight','Mesh_Outline','Armature','UV_UDIMCompensate'])
        
        if not bpy.data.collections['P62_Engeliheart_Upload'] in bpy.context.scene.collection.children_recursive: #hard coded
            bpy.context.scene.collection.children.link(bpy.data.collections['P62_Engeliheart_Upload'])
        
        joined_mesh = join_mesh(objects_list, joined_object_name, bpy.data.collections['P62_Engeliheart_Upload'])
        
        if bpy.context.scene != bpy.data.scenes['05 Upload Scene']:
            bpy.context.scene.collection.children.unlink(bpy.data.collections['P62_Engeliheart_Upload'])

        
        #create_armature_modifier(object, bpy.data.objects['rig_game'], 0)
        
        bpy.ops.ed.undo_push(message = f"Activity: Undo Split fot {joined_mesh.name}")

if __name__ == "__main__":
    main()