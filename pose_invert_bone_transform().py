import bpy

"""
Objective/Purpose
    - mainly used for creating mouthclose blendshape

To Do
    - not really used anymore so because we just eyeball and test and adjust
    
"""

for bone in bpy.context.selected_pose_bones:
    bone.location = -bone.location
    bone.rotation_quaternion[0] = -bone.rotation_quaternion[0]