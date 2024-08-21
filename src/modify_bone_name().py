import bpy

""" 
Objective/Purpose
    - a renamer for bone DEF-
    - used to be the switcher for anim rig to metarig
    
To Do
    - maybe to depreciated folder
 """
#
# 

HumanoidBones = ['spine', 'spine.001', 'spine.002', 'spine.003', 'spine.004', 'spine.005', 'spine.006', 'pelvis.L', 'pelvis.R', 'thigh.L', 'thigh.L.001', 'shin.L', 'shin.L.001', 'foot.L', 'toe.L', 'thigh.R', 'thigh.R.001', 'shin.R', 'shin.R.001', 'foot.R', 'toe.R', 'teeth.T', 'nose.002', 'nose.003', 'nose.L.001', 'nose.R.001', 'eye_master.L', 'lid.B.L', 'lid.B.L.001', 'lid.B.L.002', 'lid.B.L.004', 'lid.B.L.003', 'lid.B.L.005', 'lid.T.L', 'lid.T.L.005', 'lid.T.L.001', 'lid.T.L.002', 'lid.T.L.004', 'lid.T.L.003', 'lid.T.L.006', 'eye.L', 'eye_iris.L', 'eye_master.R', 'lid.B.R', 'lid.B.R.001', 'lid.B.R.002', 'lid.B.R.004', 'lid.B.R.003', 'lid.B.R.005', 'lid.T.R', 'lid.T.R.005', 'lid.T.R.001', 'lid.T.R.002', 'lid.T.R.004', 'lid.T.R.003', 'lid.T.R.006', 'eye.R', 'eye_iris.R', 'teeth.B', 'tongue', 'tongue.001', 'tongue.002', 'jaw_master', 'chin', 'chin.001', 'jaw', 'jaw.L', 'jaw.L.001', 'chin.L', 'jaw.R', 'jaw.R.001', 'chin.R', 'lip.T.L', 'lip.T.L.002', 'lip.T.L.001', 'lip.T.L.003', 'lip.T.R', 'lip.T.R.002', 'lip.T.R.001', 'lip.T.R.003', 'lip.B.L', 'lip.B.L.002', 'lip.B.L.001', 'lip.B.L.003', 'lip.B.R', 'lip.B.R.002', 'lip.B.R.001', 'lip.B.R.003', 'brow.B.L', 'brow.B.L.001', 'brow.B.L.002', 'brow.B.L.003', 'brow.B.L.004', 'nose.L', 'brow.B.R', 'brow.B.R.001', 'brow.B.R.002', 'brow.B.R.003', 'brow.B.R.004', 'nose.R', 'brow.T.L', 'brow.T.L.001', 'brow.T.L.005', 'brow.T.L.004', 'brow.T.L.002', 'brow.T.L.003', 'brow.T.R', 'brow.T.R.001', 'brow.T.R.005', 'brow.T.R.004', 'brow.T.R.002', 'brow.T.R.003', 'cheek.B.L', 'cheek.B.L.001', 'cheek.B.R', 'cheek.B.R.001', 'cheek.T.L', 'cheek.T.L.001', 'cheek.T.R', 'cheek.T.R.001', 'forehead.L', 'forehead.L.001', 'forehead.L.002', 'forehead.L.003', 'forehead.L.004', 'forehead.R', 'forehead.R.001', 'forehead.R.002', 'forehead.R.003', 'forehead.R.004', 'nose', 'nose.001', 'nose.004', 'temple.L', 'temple.R', 'shoulder.L', 'upper_arm.L', 'upper_arm.L.001', 'forearm.L', 'forearm.L.001', 'hand.L', 'f_index.01.L', 'f_index.02.L', 'f_index.03.L', 'thumb.01.L', 'thumb.02.L', 'thumb.03.L', 'palm.01.L', 'f_middle.01.L', 'f_middle.02.L', 'f_middle.03.L', 'palm.02.L', 'f_ring.01.L', 'f_ring.02.L', 'f_ring.03.L', 'palm.03.L', 'f_pinky.01.L', 'f_pinky.02.L', 'f_pinky.03.L', 'palm.04.L', 'shoulder.R', 'upper_arm.R', 'upper_arm.R.001', 'forearm.R', 'forearm.R.001', 'hand.R', 'f_index.01.R', 'f_index.02.R', 'f_index.03.R', 'thumb.01.R', 'thumb.02.R', 'thumb.03.R', 'palm.01.R', 'f_middle.01.R', 'f_middle.02.R', 'f_middle.03.R', 'palm.02.R', 'f_ring.01.R', 'f_ring.02.R', 'f_ring.03.R', 'palm.03.R', 'f_pinky.01.R', 'f_pinky.02.R', 'f_pinky.03.R', 'palm.04.R']

# add DEF-
def AddPrefix():
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            for ObjectVertexGroup in obj.vertex_groups:
                for TargetVertexGroup in HumanoidBones:
                    if ObjectVertexGroup.name == TargetVertexGroup:
                        ObjectVertexGroup.name = 'DEF-' + ObjectVertexGroup.name
                        break

# remove DEF-
def RemovePrefix():
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            for ObjectVertexGroup in obj.vertex_groups:
                for TargetVertexGroup in HumanoidBones:
                    if ObjectVertexGroup.name == 'DEF-' + TargetVertexGroup:
                        ObjectVertexGroup.name = ObjectVertexGroup.name[4:]
                        break

# ========= #

#AddPrefix()
RemovePrefix()

#TO DO:
#    - add prefix definer w/ auto length reader for thr remove prefix side