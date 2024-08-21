import bpy

"""
Objective/Purpose
    - was the prototype for the workflow
    - maybe depreciate but still useful as an idea
        - keeps the scope of its effects on itself
            - deletes unaffected groups
        - BUT we plan to contain the data in the rig now rather than the mesh

To Do
    - so... deadge?
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
    clean_mesh_modifiers,
    create_armature_modifier,
    create_surface_deform_modifier,
    get_rig_name,
    write_armature_data_to_custom_properties,
    set_armature_and_bone_name,
    remove_modifier_by_name,   
)

####
scene = bpy.data.scenes['02 Rig Scene']
scene_collection_names = ['_Definitions Empty/Objects', 'Rig']
source_collection = bpy.data.collections['Texture Bake']
target_collection = bpy.data.collections['Texture Bake.Weight']
copy_suffix = '.Weight'
replace_mesh = False

####

def mesh_selection(source_collection):
    if len(get_mesh_selection()) == 0:
        mesh_selection = source_collection.all_objects
        return mesh_selection
    else:
        return get_mesh_selection()

def check_rig_space():
    return

def environment_setup():
    'check create scene'
    return

def clear_deform_weights(object, protect_filter = ('_', 'OH_')):
    clearing_lists = []
    for vertex_group in object.vertex_groups: 
        if not vertex_group.name.startswith(tuple(protect_filter)):
            clearing_lists.append(vertex_group.name) # prevents some memory problems with reading while writing
    
    for vertex_group_name in clearing_lists:
        object.vertex_groups.remove(object.vertex_groups.get(vertex_group_name))
    
def copy_vertex_weight_names_and_lock(from_object, to_object):
    vertex_group_lists = []
    
    for vertex_group in from_object.vertex_groups:
        if not vertex_group.name.startswith('_'):
            vertex_group_lists.append((vertex_group.name,vertex_group.lock_weight))
    
    for vertex_group_name, is_lock_weight in vertex_group_lists:
        if to_object.vertex_groups.get(vertex_group_name, False):
            to_object.vertex_groups.get(vertex_group_name).lock_weight = is_lock_weight
        else:
            vg = to_object.vertex_groups.new(name = vertex_group_name)
            vg.lock_weight = is_lock_weight

def infer_source_and_target_from_selection_name(object, copy_suffix):
    source_object_name = object.name.rsplit(copy_suffix,1)[0]
    target_object_name = source_object_name + copy_suffix
    return (source_object_name, target_object_name)



########



for object in mesh_selection(source_collection):
    # Handle it so we can select either source or copy and properly update it
    source_object_name, target_object_name = infer_source_and_target_from_selection_name(object, copy_suffix) 
    
    source_object = bpy.data.objects.get(source_object_name, False)
    
    source_collection_name = source_object.users_collection[0].name.rsplit(copy_suffix,1)[0]
    target_collection_name = source_collection_name + copy_suffix
    
    source_collection = bpy.data.collections.get(source_collection_name)
    target_collection = bpy.data.collections.get(target_collection_name)
    
    
    # Handles if source no custom properties : sometimes/initially the main mesh doesnt have custom properties
    if not source_object.get('_rig_name', False): 
        source_object['_rig_name'] = 'metarig'
    if not source_object.get('_rig_mod_index', False):
        source_object['_rig_mod_index'] = 100
    
    # Handles if source no armature : sometimes/initially the main mesh doesnt have armatures
    if source_object.modifiers.get('Armature', False): 
        write_armature_data_to_custom_properties(source_object)
        source_object_armature = bpy.data.objects.get(source_object['_rig_name'])
    else:
        source_object_armature = bpy.data.objects.get(source_object['_rig_name'])
        create_armature_modifier(source_object, source_object_armature, source_object['_rig_mod_index'])
        
    
    # if copy exists for transfer data to source and clean-up
    if bpy.data.objects.get(target_object_name, False): 
                
        target_object = bpy.data.objects.get(target_object_name, False)
        
        if source_object['_rig_name'] != target_object.get('_rig_name'):
            if source_object['_rig_name'] == 'rig_anim':
                set_armature_and_bone_name('ANIMRIG', mesh_lists = [target_object])
            else:
                set_armature_and_bone_name('METARIG', mesh_lists = [target_object])
        
        link_object_to_collection(target_object, target_collection)
        clear_deform_weights(source_object, ('_', 'OH_'))
        copy_vertex_weight_names_and_lock(target_object, source_object)
        bpy.data.objects.remove(target_object)
    
    # modifies copy : to be ready for weight paint
    target_object = duplicate_mesh_object(source_object, copy_suffix, target_collection, replace_mesh)
    clean_mesh_modifiers(target_object,['Armature', 'OH_OUTLINE'])
    apply_modifiers_via_gret(target_object)
    create_armature_modifier(target_object, source_object_armature, 100)
   
    
    
    # set the rigtype were working on
    set_armature_and_bone_name('ANIMRIG', mesh_lists = [source_object,target_object])
    
    # Just a measure to reduce lag
    if False: # a switch
        remove_modifier_by_name(source_object, 'Armature') 
    
    set_object_active(target_object)
    # Note : the custom properties of the source and copy will be different
    
