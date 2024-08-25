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
        - merge facial bones
        - apply game rig modifier
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



####

scene = bpy.data.scenes['05 Upload Scene']
source_collection = bpy.data.collection['Texture Bake.Final']
copy_suffix = '.Upload'
replace_mesh = True

metarig_armature = bpy.data.armatures.get('metarig',  None)
anim_armature = bpy.data.armatures.get('rig_anim',  None)
game_armature = bpy.data.armatures.get('rig_game',  None)
####

#link_collections_to_scene(scene, scene_collection_names) 

# manual copy for now we'll manage it better so its cleaner with all whe copy things
# just do the duplicate and maybe we can change the "head_arkit_collection" to let all the final be in one collection

def main():
    if game_armature == None:
        create_game_rig() #create the .py for this its only the metarig stripped of the face rig and the helper bones


    set_armature_and_bone_name('ANIMRIG', metarig_armature, anim_armature, head_target_collection.all_objects)
    
    
    
    for source_object in head_target_collection.all_objects: 
        
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
    
