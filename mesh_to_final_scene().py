import bpy

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
    create_armature_modifier,
    create_surface_deform_modifier,
    get_rig_name,
    write_armature_data_to_custom_properties,
    set_armature_and_bone_name,
    remove_modifier_by_name,   
)

####
scene = bpy.data.scenes['04 Final Scene']
scene_collection_names = ['_Definitions Empty/Objects', 'Rig']
source_collection = bpy.data.collections['Texture Bake']
target_collection = bpy.data.collections['Texture Bake.Final']
copy_suffix = '.Final'
replace_mesh = True

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

def clean_mesh_inactive_modifiers(object, modifier_names): # where we can input stuff we want to delete or adjusts
    set_object_active(object)
    remove_modifier_names = []

    for modifier in object.modifiers: # doing it like this because reading while modifying produces memory targeting errors
        if not modifier.show_viewport : #modifier.name in modifier_names) or (modifier.type == 'NODES') or 
            remove_modifier_names.append(modifier.name)
    
    for modifier_name in remove_modifier_names:
        bpy.ops.object.modifier_remove(modifier = modifier_name)

def create_mesh_outline_modifier(object, modifier_name = 'Mesh_Outline', vertex_group_name = 'OH_Outline_VertexGroup', overwrite = False):
    
    if not object.modifiers.get(modifier_name,False):
        modifier = modifier = object.modifiers.new(modifier_name, 'SOLIDIFY')
    elif overwrite:
        modifier = object.modifiers.get(modifier_name)
    else:
        return
    
    modifier.vertex_group = vertex_group_name
    modifier.use_flip_normals = True
    modifier.material_offset = 999
    modifier.thickness_vertex_group = .005
    modifier.thickness = -.1
    modifier.show_render = False
    modifier.use_rim = False

def create_geometry_nodes_outline_modifier(object, modifier_name = 'Set_Mesh_Outline_Weight', vertex_group_name = 'OH_Outline_VertexGroup', overwrite = False):
    
    if not object.modifiers.get(modifier_name,False):
        modifier = object.modifiers.new(modifier_name, 'NODES')
    elif overwrite:
        modifier = object.modifiers.get(modifier_name)
    else:
        return
    
    modifier.node_group = bpy.data.node_groups['OutlineWeight']
    modifier['Input_8'] = 0.00 # make sure its float
    modifier['Input_5'] = 1.00
    modifier["Output_3_attribute_name"] = vertex_group_name
    modifier["Output_6_attribute_name"] = 'CA - MeshOutlineWidth'

def copy_mesh_modifiers_from_to(source_object, target_object):
    bpy.ops.object.select_all(action='DESELECT')
    set_object_active(source_object)
    target_object.select_set(True)
    for modifier in source_object.modifiers:
        bpy.ops.object.modifier_copy_to_selected(modifier=modifier.name)
    bpy.ops.object.select_all(action='DESELECT')

def create_geometry_nodes_uv_udim_compensate(object, modifier_name = 'UV_UDIMCompensate', overwrite = False):
    if not object.modifiers.get(modifier_name,False):
        modifier = object.modifiers.new(modifier_name, 'NODES')
    elif overwrite:
        modifier = object.modifiers.get(modifier_name)
    else:
        return
    modifier.node_group = bpy.data.node_groups['UV_UDIMCompensate']



# =================================================================== #

current_scene = bpy.context.scene
object_lists = mesh_selection(source_collection)

for object in object_lists:
    # Handle it so we can select either source or copy and properly update it
    source_object_name, target_object_name = infer_source_and_target_from_selection_name(object, copy_suffix) 
    source_object = bpy.data.objects.get(source_object_name, False)
    source_collection_name = source_object.users_collection[0].name.rsplit(copy_suffix,1)[0]
    target_collection_name = source_collection_name + copy_suffix
    source_collection = bpy.data.collections.get(source_collection_name)
    target_collection = bpy.data.collections.get(target_collection_name)
    
    
    # Handles if source no custom properties : sometimes/initially the main mesh doesnt have custom properties
    source_object['_rig_name'] = source_object.get('_rig_name', 'metarig')
    source_object['_rig_mod_index'] = source_object.get('_rig_mod_index', 100)
    
    # Handles if source no armature : sometimes/initially the main mesh doesnt have armatures
    if source_object.modifiers.get('Armature', False): 
        write_armature_data_to_custom_properties(source_object)
        source_object_armature = bpy.data.objects.get(source_object['_rig_name'])
    else:
        source_object_armature = bpy.data.objects.get(source_object['_rig_name'])
        create_armature_modifier(source_object, source_object_armature, source_object['_rig_mod_index'])
        
    # if copy exists for transfer data to source and clean-up
    if bpy.data.objects.get(target_object_name, False): 
        hold_object = bpy.data.objects.get(target_object_name, False)
        
        source_rig_type = 'ANIMRIG' if source_object['_rig_name'] == 'rig_anim' else 'METARIG'
        if source_object['_rig_name'] != hold_object.get('_rig_name'):
            set_armature_and_bone_name(source_rig_type, mesh_lists = [hold_object])
        
        # redundant but for safety since it should be in the right place already
        link_object_to_collection(hold_object, target_collection)
        hold_object.name += 'hold'
        
        print(source_object.name)
        target_object = duplicate_mesh_object(source_object, copy_suffix, target_collection, replace_mesh)
        clean_mesh_inactive_modifiers(target_object,['Armature', 'OH_OUTLINE'])
        
        if len(target_object.modifiers)>0:
         apply_modifiers_via_gret(target_object)
        
        copy_mesh_modifiers_from_to(hold_object,target_object)
        
        bpy.data.objects.remove(hold_object)
    
    else :
        # modifies copy : to be ready for weight paint
        target_object = duplicate_mesh_object(source_object, copy_suffix, target_collection, replace_mesh)
        clean_mesh_inactive_modifiers(target_object,['Armature', 'OH_OUTLINE'])
        
        if len(target_object.modifiers)>0:
         apply_modifiers_via_gret(target_object)
        
        create_geometry_nodes_outline_modifier(target_object)
        create_mesh_outline_modifier(target_object)
        create_armature_modifier(target_object, source_object_armature, 100)
   
    
    
    # set the rigtype were working on
    set_armature_and_bone_name('ANIMRIG', mesh_lists = [source_object,target_object])
    
    # Just a measure to reduce lag
    if False: # a switch
        remove_modifier_by_name(source_object, 'Armature') 
    
    set_object_active(target_object)
    # Note : the custom properties of the source and copy will be different

bpy.context.window.scene = current_scene
