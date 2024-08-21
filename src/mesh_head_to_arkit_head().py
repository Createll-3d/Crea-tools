import bpy

"""
Objective/Purpose
    - for an intermediary scene for testing and to reduce lag
    - Duplicates the weight mesh collection to a target arkit mesh collection

To Do
    - more robust initialize same with the other scene related stuff
    - need to create scene if none
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

####

scene = bpy.data.scenes['03 ARkit Scene']
scene_collection_names = ['_Definitions Empty/Objects', 'Rig']
head_source_collection = bpy.data.collections['head']
head_target_collection = bpy.data.collections['head']
head_arkit_collection = bpy.data.collections['head.ARkit']
copy_suffix = '.ARkit'
replace_mesh = True

metarig_armature = bpy.data.armatures['metarig']
anim_armature = bpy.data.armatures['rig_anim']
####

link_collections_to_scene(scene, scene_collection_names)

def main():
    
    set_armature_and_bone_name('ANIMRIG', metarig_armature, anim_armature, head_target_collection.objects)
    
    for source_object in head_target_collection.objects:
        
        if source_object.get('_use_surface_deform', None) == None:
            source_object['_use_surface_deform'] = False
        
        arkit_mesh = duplicate_mesh_object(source_object, copy_suffix, head_arkit_collection, replace_mesh)
        
        clean_mesh_modifiers(arkit_mesh,['OH_OUTLINE'])
        
        apply_modifiers_till_modifier_type_via_gret(arkit_mesh, 'ARMATURE')
        
        create_armature_modifier(arkit_mesh, bpy.data.objects['rig_anim'], 0)
        
        if source_object.get('_use_surface_deform', False):
            
            sd_mesh = duplicate_mesh_object(arkit_mesh, '.SD', head_arkit_collection, replace_mesh)
            apply_modifiers_via_gret(sd_mesh)
            create_surface_deform_modifier(sd_mesh, arkit_mesh)

if __name__ == "__main__":
    main()
    
