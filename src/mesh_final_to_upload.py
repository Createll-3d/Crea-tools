import bpy

"""
Objective/Purpose
    - deadge / depreciated
    - transferred to v2

To Do
    - delete this and remove v2 from mesh_final_to_upload_v2.py
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
source_collection = get_mesh_selection() #bpy.data.collections['Texture Bake.Final']
copy_suffix = '.Upload'
replace_mesh = True

metarig_armature = bpy.data.armatures.get('metarig',  None)
anim_armature = bpy.data.armatures.get('rig_anim',  None)
game_armature = bpy.data.armatures.get('rig_game',  None)
####


def clear_material(object):
    print(f"Activity: Clearing materials of {object.name}")
    
    if not object.get('_bakeTextureGroup',False):
        try:
            object['_bakeTextureGroup'] = object.data.materials[0].name
        except:
            None
    
    object.data.materials.clear()
    

    
def link_material(object, material_name):
    print(f"Activity: link material {object} to {material_name}")
    
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

def rename_for_upload(object):
    object.name.replace(['.Final'],'.Upload')

#link_collections_to_scene(scene, scene_collection_names) 

# manual copy for now we'll manage it better so its cleaner with all whe copy things
# just do the duplicate and maybe we can change the "head_arkit_collection" to let all the final be in one collection




def main(objects_list):
    if game_armature == None:
        None
        # create_game_rig() #create the .py for this its only the metarig stripped of the face rig and the helper bones

        
    for source_object in objects_list: 
        
        set_armature_and_bone_name('METARIG', metarig_armature, anim_armature, [source_object])

        clean_mesh_modifiers(source_object,['OH_OUTLINE','Set_Mesh_Outline_Weight','Mesh_Outline','Armature','UV_UDIMCompensate'])
        
        create_armature_modifier(source_object, bpy.data.objects['metarig'], 0)
        
    

if __name__ == "__main__":

    object_lists = get_mesh_selection()
    if len(object_lists) < 1:
        object_lists = bpy.data.collections['Texture Bake.Upload'].all_objects
    
    #main(object_lists)
    
    for object in object_lists:
        clear_material(object)
        link_material(object, object['_bakeTextureGroup'] + "_Final")
        clean_mesh_modifiers(object,['OH_OUTLINE','Set_Mesh_Outline_Weight','Mesh_Outline','Armature','UV_UDIMCompensate'])
        create_armature_modifier(object, bpy.data.objects['metarig'], 0)
