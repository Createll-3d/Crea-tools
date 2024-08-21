import bpy

"""
Objective/Purpose
    - for making the rig state the same
    - for toggling between rig states
 
To Do
    - forgot if this foolproof works
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
    get_rig_type_count,
    set_armature_and_bone_name,
)

weight_armature_name = 'metarig'
anim_armature_name = 'rig_anim'

#####

weight_armature = bpy.data.armatures.get(weight_armature_name)
anim_armature = bpy.data.armatures.get(anim_armature_name)

mesh_lists = bpy.data.collections['Texture Bake'].all_objects

set_armature_and_bone_name(get_rig_type_count(mesh_lists,True), weight_armature, anim_armature, mesh_lists)

