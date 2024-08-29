import bpy

"""
Objective/Purpose
    - used to create game rig then to proxy rig
    - cleans up the generated rig and manages the extra objects it makes

Requires
	- gamrerigtools

To Do
    - but we can probably just use the metarig/anim_rig with modifications as the game rig
    - dont rely on game rig tools
        - just duplicate metarig
        - clean-up face rig
        - remove helper bone
    
"""

# SELECT ARNIM RIG :       'rig_anim'
# SELECT FINAL COLLECTION: 'Final Mesh'

try:
    bpy.data.armatures.remove(bpy.data.armatures['rig_deform'])
except KeyError:
    None

try:
    bpy.data.armatures.remove(bpy.data.armatures['rig_proxy'])
except KeyError:
    None

try:
    bpy.context.view_layer.objects.active = bpy.data.objects['rig_anim']
except KeyError:
    None

bpy.ops.gamerigtool.generate_game_rig(Extract_Mode='DEFORM', Flat_Hierarchy=False, Disconnect_Bone=False, Constraint_Type='LOTROT', Animator_Remove_BBone=False, Animator_Disable_Deform=False, Parent_To_Deform_Rig=False, Deform_Armature_Name="rig_deform", Deform_Remove_BBone=True, Deform_Move_Bone_to_Layer1=False, Deform_Set_Inherit_Rotation_True=True, Deform_Set_Inherit_Scale_Full=True, Deform_Set_Local_Location_True=True, Deform_Remove_Non_Deform_Bone=True, Deform_Unlock_Transform=True, Deform_Remove_Shape=True, Deform_Remove_All_Constraints=True, Deform_Copy_Transform=True, Deform_Bind_to_Deform_Rig=True, Remove_Custom_Properties=True, Remove_Animation_Data=True, Show_Advanced=False)

try:
    bpy.data.armatures["rig_anim.001"].name = 'rig_deform'
except KeyError:
    None

rig_deform_pose = bpy.data.objects['rig_deform'].pose
rig_deform_edit = bpy.data.armatures['rig_deform']

facial_bones = [rig_deform_pose.bones["DEF-teeth.T"], rig_deform_pose.bones["DEF-nose.002"], rig_deform_pose.bones["DEF-nose.003"], rig_deform_pose.bones["DEF-nose.L.001"], rig_deform_pose.bones["DEF-nose.R.001"], rig_deform_pose.bones["DEF-eye_master.L"], rig_deform_pose.bones["DEF-lid.B.L"], rig_deform_pose.bones["DEF-lid.B.L.001"], rig_deform_pose.bones["DEF-lid.B.L.002"], rig_deform_pose.bones["DEF-lid.B.L.004"], rig_deform_pose.bones["DEF-lid.B.L.003"], rig_deform_pose.bones["DEF-lid.B.L.005"], rig_deform_pose.bones["DEF-lid.T.L"], rig_deform_pose.bones["DEF-lid.T.L.005"], rig_deform_pose.bones["DEF-lid.T.L.001"], rig_deform_pose.bones["DEF-lid.T.L.002"], rig_deform_pose.bones["DEF-lid.T.L.004"], rig_deform_pose.bones["DEF-lid.T.L.003"], rig_deform_pose.bones["DEF-eye_iris.L"], rig_deform_pose.bones["DEF-eye_master.R"], rig_deform_pose.bones["DEF-lid.B.R"], rig_deform_pose.bones["DEF-lid.B.R.001"], rig_deform_pose.bones["DEF-lid.B.R.002"], rig_deform_pose.bones["DEF-lid.B.R.004"], rig_deform_pose.bones["DEF-lid.B.R.003"], rig_deform_pose.bones["DEF-lid.B.R.005"], rig_deform_pose.bones["DEF-lid.T.R"], rig_deform_pose.bones["DEF-lid.T.R.005"], rig_deform_pose.bones["DEF-lid.T.R.001"], rig_deform_pose.bones["DEF-lid.T.R.002"], rig_deform_pose.bones["DEF-lid.T.R.004"], rig_deform_pose.bones["DEF-lid.T.R.003"], rig_deform_pose.bones["DEF-eye_iris.R"], rig_deform_pose.bones["DEF-teeth.B"], rig_deform_pose.bones["DEF-tongue"], rig_deform_pose.bones["DEF-tongue.001"], rig_deform_pose.bones["DEF-tongue.002"], rig_deform_pose.bones["DEF-jaw_master"], rig_deform_pose.bones["DEF-chin"], rig_deform_pose.bones["DEF-chin.001"], rig_deform_pose.bones["DEF-jaw"], rig_deform_pose.bones["DEF-jaw.L"], rig_deform_pose.bones["DEF-jaw.L.001"], rig_deform_pose.bones["DEF-chin.L"], rig_deform_pose.bones["DEF-jaw.R"], rig_deform_pose.bones["DEF-jaw.R.001"], rig_deform_pose.bones["DEF-chin.R"], rig_deform_pose.bones["DEF-lip.T.L"], rig_deform_pose.bones["DEF-lip.T.L.002"], rig_deform_pose.bones["DEF-lip.T.L.001"], rig_deform_pose.bones["DEF-lip.T.L.003"], rig_deform_pose.bones["DEF-lip.T.R"], rig_deform_pose.bones["DEF-lip.T.R.002"], rig_deform_pose.bones["DEF-lip.T.R.001"], rig_deform_pose.bones["DEF-lip.T.R.003"], rig_deform_pose.bones["DEF-lip.B.L"], rig_deform_pose.bones["DEF-lip.B.L.002"], rig_deform_pose.bones["DEF-lip.B.L.001"], rig_deform_pose.bones["DEF-lip.B.L.003"], rig_deform_pose.bones["DEF-lip.B.R"], rig_deform_pose.bones["DEF-lip.B.R.002"], rig_deform_pose.bones["DEF-lip.B.R.001"], rig_deform_pose.bones["DEF-lip.B.R.003"], rig_deform_pose.bones["DEF-brow.B.L"], rig_deform_pose.bones["DEF-brow.B.L.001"], rig_deform_pose.bones["DEF-brow.B.L.002"], rig_deform_pose.bones["DEF-brow.B.L.003"], rig_deform_pose.bones["DEF-brow.B.L.004"], rig_deform_pose.bones["DEF-nose.L"], rig_deform_pose.bones["DEF-brow.B.R"], rig_deform_pose.bones["DEF-brow.B.R.001"], rig_deform_pose.bones["DEF-brow.B.R.002"], rig_deform_pose.bones["DEF-brow.B.R.003"], rig_deform_pose.bones["DEF-brow.B.R.004"], rig_deform_pose.bones["DEF-nose.R"], rig_deform_pose.bones["DEF-brow.T.L"], rig_deform_pose.bones["DEF-brow.T.L.001"], rig_deform_pose.bones["DEF-brow.T.L.005"], rig_deform_pose.bones["DEF-brow.T.L.004"], rig_deform_pose.bones["DEF-brow.T.L.002"], rig_deform_pose.bones["DEF-brow.T.L.003"], rig_deform_pose.bones["DEF-brow.T.R"], rig_deform_pose.bones["DEF-brow.T.R.001"], rig_deform_pose.bones["DEF-brow.T.R.005"], rig_deform_pose.bones["DEF-brow.T.R.004"], rig_deform_pose.bones["DEF-brow.T.R.002"], rig_deform_pose.bones["DEF-brow.T.R.003"], rig_deform_pose.bones["DEF-cheek.B.L"], rig_deform_pose.bones["DEF-cheek.B.L.001"], rig_deform_pose.bones["DEF-cheek.B.R"], rig_deform_pose.bones["DEF-cheek.B.R.001"], rig_deform_pose.bones["DEF-cheek.T.L"], rig_deform_pose.bones["DEF-cheek.T.L.001"], rig_deform_pose.bones["DEF-cheek.T.R"], rig_deform_pose.bones["DEF-cheek.T.R.001"], rig_deform_pose.bones["DEF-forehead.L"], rig_deform_pose.bones["DEF-forehead.L.001"], rig_deform_pose.bones["DEF-forehead.L.002"], rig_deform_pose.bones["DEF-forehead.L.003"], rig_deform_pose.bones["DEF-forehead.L.004"], rig_deform_pose.bones["DEF-forehead.R"], rig_deform_pose.bones["DEF-forehead.R.001"], rig_deform_pose.bones["DEF-forehead.R.002"], rig_deform_pose.bones["DEF-forehead.R.003"], rig_deform_pose.bones["DEF-forehead.R.004"], rig_deform_pose.bones["DEF-nose"], rig_deform_pose.bones["DEF-nose.001"], rig_deform_pose.bones["DEF-nose.004"], rig_deform_pose.bones["DEF-temple.L"], rig_deform_pose.bones["DEF-temple.R"]]

child_to_parent_bone = [
    [rig_deform_edit.bones["DEF-upper_arm.L"].name, rig_deform_edit.bones["DEF-shoulder.L"].name, True], 
    [rig_deform_edit.bones["DEF-upper_arm.R"].name, rig_deform_edit.bones["DEF-shoulder.R"].name, True], 
    [rig_deform_edit.bones["DEF-pelvis.R"].name, rig_deform_edit.bones["DEF-spine"].name, False], 
    [rig_deform_edit.bones["DEF-pelvis.L"].name, rig_deform_edit.bones["DEF-spine"].name, False], 
    [rig_deform_edit.bones["DEF-thigh.L"].name, rig_deform_edit.bones["DEF-spine"].name, False], 
    [rig_deform_edit.bones["DEF-thigh.R"].name, rig_deform_edit.bones["DEF-spine"].name, False],
    [rig_deform_edit.bones["DEF-shoulder.L"].name, rig_deform_edit.bones["DEF-spine.003"].name, False],
    [rig_deform_edit.bones["DEF-shoulder.R"].name, rig_deform_edit.bones["DEF-spine.003"].name, False],
    [rig_deform_pose.bones["DEF-eye.L"].name, rig_deform_edit.bones["DEF-spine.005"].name, False],
    [rig_deform_pose.bones["DEF-eye.R"].name, rig_deform_edit.bones["DEF-spine.005"].name, False]]

bpy.context.view_layer.objects.active = bpy.data.objects['rig_deform']
bpy.ops.object.mode_set(mode='EDIT')

## DELETE FACIAL BONES

for bone in facial_bones:
    rig_deform_edit.edit_bones.remove(rig_deform_edit.edit_bones.get(bone.name))

## CONNECT BONES

for child, parent, connected in child_to_parent_bone:
    rig_deform_edit.edit_bones[child].parent = rig_deform_edit.edit_bones[parent]
    rig_deform_edit.edit_bones[child].use_connect = connected
    
bpy.ops.object.mode_set(mode='OBJECT')



# CREATE PROXY BONES ------------------------

bpy.ops.object.duplicate()

try:
    bpy.context.view_layer.objects.active = bpy.data.objects["rig_deform.001"]
except KeyError:
    None

try:
    bpy.data.armatures["rig_deform.001"].name = 'rig_proxy'
    bpy.data.objects["rig_deform.001"].name = 'rig_proxy'
except KeyError:
    None

## DELETE NON_HUMANOID BONES

humanoid_bones = [bpy.data.armatures['rig_proxy'].bones["DEF-spine"], bpy.data.armatures['rig_proxy'].bones["DEF-spine.001"], bpy.data.armatures['rig_proxy'].bones["DEF-spine.002"], bpy.data.armatures['rig_proxy'].bones["DEF-spine.003"], bpy.data.armatures['rig_proxy'].bones["DEF-spine.004"], bpy.data.armatures['rig_proxy'].bones["DEF-spine.005"], bpy.data.armatures['rig_proxy'].bones["DEF-thigh.L"], bpy.data.armatures['rig_proxy'].bones["DEF-shin.L"], bpy.data.armatures['rig_proxy'].bones["DEF-foot.L"], bpy.data.armatures['rig_proxy'].bones["DEF-toe.L"], bpy.data.armatures['rig_proxy'].bones["DEF-thigh.R"], bpy.data.armatures['rig_proxy'].bones["DEF-shin.R"], bpy.data.armatures['rig_proxy'].bones["DEF-foot.R"], bpy.data.armatures['rig_proxy'].bones["DEF-toe.R"], bpy.data.armatures['rig_proxy'].bones["DEF-shoulder.L"], bpy.data.armatures['rig_proxy'].bones["DEF-upper_arm.L"], bpy.data.armatures['rig_proxy'].bones["DEF-forearm.L"], bpy.data.armatures['rig_proxy'].bones["DEF-hand.L"], bpy.data.armatures['rig_proxy'].bones["DEF-f_index.01.L"], bpy.data.armatures['rig_proxy'].bones["DEF-f_index.02.L"], bpy.data.armatures['rig_proxy'].bones["DEF-f_index.03.L"], bpy.data.armatures['rig_proxy'].bones["DEF-thumb.01.L"], bpy.data.armatures['rig_proxy'].bones["DEF-thumb.02.L"], bpy.data.armatures['rig_proxy'].bones["DEF-thumb.03.L"], bpy.data.armatures['rig_proxy'].bones["DEF-f_middle.01.L"], bpy.data.armatures['rig_proxy'].bones["DEF-f_middle.02.L"], bpy.data.armatures['rig_proxy'].bones["DEF-f_middle.03.L"], bpy.data.armatures['rig_proxy'].bones["DEF-f_ring.01.L"], bpy.data.armatures['rig_proxy'].bones["DEF-f_ring.02.L"], bpy.data.armatures['rig_proxy'].bones["DEF-f_ring.03.L"], bpy.data.armatures['rig_proxy'].bones["DEF-f_pinky.01.L"], bpy.data.armatures['rig_proxy'].bones["DEF-f_pinky.02.L"], bpy.data.armatures['rig_proxy'].bones["DEF-f_pinky.03.L"], bpy.data.armatures['rig_proxy'].bones["DEF-shoulder.R"], bpy.data.armatures['rig_proxy'].bones["DEF-upper_arm.R"], bpy.data.armatures['rig_proxy'].bones["DEF-forearm.R"], bpy.data.armatures['rig_proxy'].bones["DEF-hand.R"], bpy.data.armatures['rig_proxy'].bones["DEF-f_index.01.R"], bpy.data.armatures['rig_proxy'].bones["DEF-f_index.02.R"], bpy.data.armatures['rig_proxy'].bones["DEF-f_index.03.R"], bpy.data.armatures['rig_proxy'].bones["DEF-thumb.01.R"], bpy.data.armatures['rig_proxy'].bones["DEF-thumb.02.R"], bpy.data.armatures['rig_proxy'].bones["DEF-thumb.03.R"], bpy.data.armatures['rig_proxy'].bones["DEF-f_middle.01.R"], bpy.data.armatures['rig_proxy'].bones["DEF-f_middle.02.R"], bpy.data.armatures['rig_proxy'].bones["DEF-f_middle.03.R"], bpy.data.armatures['rig_proxy'].bones["DEF-f_ring.01.R"], bpy.data.armatures['rig_proxy'].bones["DEF-f_ring.02.R"], bpy.data.armatures['rig_proxy'].bones["DEF-f_ring.03.R"], bpy.data.armatures['rig_proxy'].bones["DEF-f_pinky.01.R"], bpy.data.armatures['rig_proxy'].bones["DEF-f_pinky.02.R"], bpy.data.armatures['rig_proxy'].bones["DEF-f_pinky.03.R"]]

bpy.ops.object.mode_set(mode='EDIT')

for bone in bpy.data.objects['rig_proxy'].data.bones:
   if bone not in humanoid_bones:
       bpy.data.armatures['rig_proxy'].edit_bones.remove(bpy.data.armatures['rig_proxy'].edit_bones.get(bone.name))

for bone in bpy.data.objects['rig_proxy'].data.bones:
    bone.name = 'proxy_' + bone.name

#    if not bone.layers[29]:
#        bpy.data.armatures['rig_proxy'].edit_bones.remove(bpy.data.armatures['rig_proxy'].edit_bones.get(bone.name))
#           if bone not in humanoid_bones:
#               bpy.data.armatures['rig_proxy'].edit_bones.remove(bpy.data.armatures['rig_proxy'].edit_bones.get(bone.name))

bpy.ops.object.mode_set(mode='OBJECT')


# Final Mesh Armeture modifier re-target to deform

for object in bpy.data.collections['Final Mesh'].objects:
    if object.type == 'MESH':
        for modifiers in object.modifiers:
            if modifiers.name == 'Armature':
                object.modifiers['Armature'].object = bpy.data.objects['rig_deform']

