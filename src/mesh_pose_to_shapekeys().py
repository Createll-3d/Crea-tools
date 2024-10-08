import bpy

"""
Objective/Purpose
    - 
	
Requires
	- gret add-on
    - there should be a window on your workspace dedicated for Asset Library with the Poses
        - it needs to be accessible so it wont work if your searching something 

To Do
    - asset window
        - create window if doesnt exists
        - clear search
    - unlink pose on armature before start
    - cleaner selection of stuff that is used to deform
    - account for the source of the pose
        - any deforms
            - displace (how can this be pointed at by an action)
            - lattice
            - self shapekey
        - armature (and determine to what armature)
        - also determine if the action has combinations of these
    - maybe treat the arkit poses as a bit different
        - want the pose names to have a prefix but not the shapekey
    - functions for handling each thing
    - refactor to have switches or stages to keep the SD versions
        - so iteration is faster 
            - by not inducing the bug (saving untargeted shapekeys) to be foreced to happen
            - by also having a one click update shapekeys
    - theres a bug in blender that saves unlinked shapkey blocks
        - and then when it notices it tries to delete them all
        - more relevant to the mesh copy/sync stuff
        - there was a fix mentioned in the docs but I guess it doesnt cover 3.6.14 lts
    - theres a way to store posed values as vertex locations but
        - for transfer
            - need to check how subdiv messes with index
        - or the transfer could be by vertex distace
        - could be geometry node or could be store location via lists
            - for geometry node need to save for self shapekeys
    - for speed
        - track poses that is modified somehow
            - a watchdog for what poses are changed somehow
                - a watchdog might be hard to implement
            - maybe we can use the description to store that it changed
        - arkit only switch for the arkit testing
        - auto switch the arkit test to the image texture version of a material
"""

import sys
import os
import importlib
sys.path.append(bpy.utils.script_paths()[2])

import _createll_script_utils
importlib.reload(_createll_script_utils)

from _createll_script_utils import (
    set_object_active, 
    get_mesh_selection, 
    apply_modifiers_via_gret,
    remove_modifier_by_type,
)


armature = bpy.context.blend_data.objects["rig_anim"]                              # shapekey set name
target_collection = bpy.data.collections['head.ARkit']

# ======================================

Poses = [
    ('Poses_ARkit', ['browInnerUp','browDownLeft','browDownRight','browOuterUpLeft','browOuterUpRight','eyeLookUpLeft','eyeLookUpRight','eyeLookDownLeft','eyeLookDownRight','eyeLookInLeft','eyeLookInRight','eyeLookOutLeft','eyeLookOutRight','eyeBlinkLeft','eyeBlinkRight','eyeSquintRight','eyeSquintLeft','eyeWideLeft','eyeWideRight','cheekPuff','cheekSquintLeft','cheekSquintRight','noseSneerLeft','noseSneerRight','jawOpen','jawForward','jawLeft','jawRight','mouthFunnel','mouthPucker','mouthLeft','mouthRight','mouthRollUpper','mouthRollLower','mouthShrugUpper','mouthShrugLower','mouthClose','mouthSmileLeft','mouthSmileRight','mouthFrownLeft','mouthFrownRight','mouthDimpleLeft','mouthDimpleRight','mouthUpperUpLeft','mouthUpperUpRight','mouthLowerDownLeft','mouthLowerDownRight','mouthPressLeft','mouthPressRight','mouthStretchLeft','mouthStretchRight','tongueOut']),
    ('Poses_Viseme', ['v_sil', 'v_aa', 'v_ee', 'v_ih', 'v_oh', 'v_ou', 'v_pp', 'v_ff', 'v_th', 'v_dd', 'v_kk', 'v_ch', 'v_ss', 'v_nn', 'v_rr', 'v_lookUp', 'v_lookDown', 'v_lookL', 'v_lookR', 'v_blink', 'v_blinkLeft', 'v_blinkRight', 'v_Angry', 'v_Sorrow', 'v_Joy', 'v_Fun', 'v_Suprised']),
    ('Poses_Extra', ['a_defaultSmile']),
    ('Poses_Physics', ['p_eye_mouth_scale_x-','p_eye_mouth_scale_y-','p_eye_scale_IrisX-_L','p_eye_scale_IrisX-_R','p_eye_scale_IrisY-_L','p_eye_scale_IrisY-_R','p_eye_scale_middleX-_L','p_eye_scale_middleX-_R','p_eye_scale_XY_L','p_eye_scale_XY_R','p_eye_scale_Y-_L','p_eye_scale_Y-_R','p_jawDown','p_faceSquishX-','p_mouthUp']),
    ('Poses_Corrective', ['c_jawOpen100+mouthSmileL','c_jawOpen100+mouthSmileR','c_overBite']),
]

#empty poses for testing
#Poses = [
#    ('Poses_ARkit', []),
#    ('Poses_Viseme', []),
#    ('Poses_Extra', []),
#    ('Poses_Generic', []),
#]



def set_pose_action(action_name, IsFlipped, armature): 
    set_object_active(armature)
    bpy.ops.object.mode_set(mode='POSE')
    
    area = [area for window in bpy.context.window_manager.windows for area in window.screen.areas if area.ui_type == 'ASSETS']
    
    bpy.ops.pose.transforms_clear()
    
    w = bpy.context.window
    
    for a in area:
        for s in a.spaces:
            if s.type == 'FILE_BROWSER':
                space = s
    
    with bpy.context.temp_override(window=w, area=area[0]):
        space.deselect_all()
        space.activate_asset_by_id(bpy.data.actions[action_name].id_data)
        bpy.ops.poselib.apply_pose_asset(blend_factor=1,flipped=IsFlipped)
        return()

def add_shape_key_if_empty(object):
    if not object.data.shape_keys:
        object.shape_key_add(name = 'Basis')
    return

def create_shapkey_divider(object, name):
    delete_shapekey_if_exists(object, '=== ' + name + ' ===')
    object.shape_key_add(name = '=== ' + name + ' ===')
    return

def delete_shapekey_if_exists(object, shape_key_name):
    if object.data.shape_keys.key_blocks.get(shape_key_name):
        object.shape_key_remove(object.data.shape_keys.key_blocks.get(shape_key_name))
    return

def apply_Action_to_TargetCollection_Shapekey(action_name, target_mesh_objects):
    
    for target in target_mesh_objects:
        
        if target.hide_render:
            continue
        
        print(f"Activity: Set {action_name} pose to {target.name}")
        
        bpy.ops.object.mode_set(mode='OBJECT')
        set_object_active(target)
        bpy.ops.object.shape_key_clear()

        target.data.shape_keys.name = target.name
        target_shapekey = target.data.shape_keys.name
        
        delete_shapekey_if_exists(target, action_name)
        
        set_object_active(target)
        target.select_set(True)
        
        
        for modifier in target.modifiers:
            if modifier.name == 'SurfaceDeform':
                target_modifier = 'SurfaceDeform'
                break
            else:
                target_modifier = 'Armature'
        try :
            bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=True, modifier=target_modifier, report=False)
            bpy.data.shape_keys[target_shapekey].key_blocks[target_modifier].name = action_name
        except:
            print(target.name + ' ' + action_name)
            pass
        
        
    return print(f"Activity: Finished applying {action_name} to shapekey")

def play_notification():
    try:
        bpy.ops.script.python_file_run(filepath = bpy.utils.script_paths()[2] + "\Script - Play Sound.py")
    except:
        return

# =================================================================== #


def main(): # tried using this main thing but I dont see the point aside from looking abit more readable
    
    target_objects = []
    temp_objects = []
    
    for object in target_collection.objects:

            
        
        target_objects.append(object)
        
        if object.name.endswith('.SD'):
            temp_object = bpy.data.objects.get(object.name.rsplit('.SD',1)[0])
            target_objects.remove(temp_object)
            temp_objects.append((object, temp_object))
    
    for action_category, action_names in Poses:
        
        for object in target_objects:
            add_shape_key_if_empty(object)
        
        for object in target_objects:
            create_shapkey_divider(object, action_category)
        
        for action_name in action_names:
            set_pose_action(action_name, False, armature)
            apply_Action_to_TargetCollection_Shapekey(action_name, target_objects)
        
        bpy.ops.ed.undo_push(message = f"Activity: Undo Split for {object.name}") #to prevent memory crash
        
        
    set_object_active(armature)
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.transforms_clear()
    bpy.ops.object.mode_set(mode='OBJECT')
    
    for object in target_objects:
        bpy.ops.ed.undo_push(message = f"Activity: Undo Split for {object.name}") #to prevent memory crash
        remove_modifier_by_type(object, ['ARMATURE', 'SURFACE_DEFORM', 'NODES'])
        print(f'Applying Modifiers : {object.name}')
        
        apply_modifiers_via_gret(object)
        None
        
    for object, temp_object in temp_objects:
        bpy.data.objects.remove(temp_object)
        object.name = object.name.rsplit('.SD',1)[0]
    
    
if __name__ == "__main__":
    main()


