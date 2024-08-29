import bpy

weight_armature_name = 'metarig'
anim_armature_name = 'rig_anim'

"""
Objective/Purpose
    - used to auto weight selected object with the metarig
 
To Do
    - think of a way to store data with the rig rather than the mesh
"""

def get_mesh_selection():
    selected_objects = []
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            selected_objects.append(obj)
    return selected_objects

def toggle_armature_and_bone_name():
    rig_count = 0
    
    for obj in get_mesh_selection():
        if obj.modifiers.get('Armature').object.name == weight_armature_name:
            rig_count += 1
        else:
            rig_count -= 1
    
    if rig_count >= 0:
        rig_count_type = 'METARIG'
    else:
        rig_count_type = 'ANIMRIG'
    
    set_armature_and_bone_name(rig_count_type)

def set_armature_and_bone_name(rig_type):
    # rig_type = 'ANIMRIG' or 'METARIG'
    standard_rigify_deform_bones = set(['spine', 'pelvis.L', 'pelvis.R', 'thigh.L', 'thigh.L.001', 'shin.L', 'shin.L.001', 'foot.L', 'toe.L', 'thigh.R', 'thigh.R.001', 'shin.R', 'shin.R.001', 'foot.R', 'toe.R', 'temple.L', 'temple.R', 'ear.L', 'ear.L.001', 'ear.L.002', 'ear.L.003', 'ear.L.004', 'ear.R', 'ear.R.001', 'ear.R.002', 'ear.R.003', 'ear.R.004', 'tongue', 'chin', 'chin.001', 'chin.L', 'chin.R', 'jaw', 'jaw.L.001', 'jaw.R.001', 'tongue.001', 'tongue.002', 'cheek.T.L', 'cheek.T.R', 'jaw.L', 'jaw.R', 'nose', 'nose.L', 'nose.R', 'cheek.B.L.001', 'cheek.B.R.001', 'cheek.B.L', 'cheek.B.R',  'nose.002', 'nose.001', 'nose.003', 'nose.004', 'nose.L.001', 'nose.R.001', 'cheek.T.L.001', 'cheek.T.R.001', 'shoulder.L', 'upper_arm.L', 'upper_arm.L.001', 'forearm.L', 'forearm.L.001', 'hand.L', 'f_index.01.L', 'f_index.02.L', 'f_index.03.L', 'thumb.01.L', 'thumb.02.L', 'thumb.03.L', 'palm.01.L', 'f_middle.01.L', 'f_middle.02.L', 'f_middle.03.L', 'palm.02.L', 'f_ring.01.L', 'f_ring.02.L', 'f_ring.03.L', 'palm.03.L', 'f_pinky.01.L', 'f_pinky.02.L', 'f_pinky.03.L', 'palm.04.L', 'shoulder.R', 'upper_arm.R', 'upper_arm.R.001', 'forearm.R', 'forearm.R.001', 'hand.R', 'f_index.01.R', 'f_index.02.R', 'f_index.03.R', 'thumb.01.R', 'thumb.02.R', 'thumb.03.R', 'palm.01.R', 'f_middle.01.R', 'f_middle.02.R', 'f_middle.03.R', 'palm.02.R', 'f_ring.01.R', 'f_ring.02.R', 'f_ring.03.R', 'palm.03.R', 'f_pinky.01.R', 'f_pinky.02.R', 'f_pinky.03.R', 'palm.04.R'])
    standard_rigify_deform_bones_substrings = ['spine.', 'lid.', 'lip.', 'brow.', 'teeth.', 'forehead.', 'heel.']
    
    weight_armature = bpy.data.armatures.get(weight_armature_name)
    anim_armature = bpy.data.armatures.get(anim_armature_name)

    if not weight_armature or not anim_armature:
        print("Armature not found in bpy.data.armatures")
        return

    for bone in weight_armature.bones:
        if 'helper' not in bone.name:
            if any(substring in bone.name for substring in standard_rigify_deform_bones_substrings):
                print(bone.name)
                standard_rigify_deform_bones.add(bone.name)

    for obj in get_mesh_selection():
        obj_aramture_modifier_object = obj.modifiers.get('Armature').object
        
        if rig_type == 'ANIMRIG':
           
            obj.modifiers.get('Armature').object = bpy.data.objects['rig_anim']
            
            for deform_bone in standard_rigify_deform_bones:
                if obj.vertex_groups.get(deform_bone):
                    print(deform_bone + ' to : ' + 'DEF-' + deform_bone)
                    obj.vertex_groups.get(deform_bone).name = 'DEF-' + deform_bone
            
        elif rig_type == 'METARIG':
            
            obj.modifiers.get('Armature').object = bpy.data.objects['metarig']
            
            for deform_bone in standard_rigify_deform_bones:
                if obj.vertex_groups.get('DEF-' + deform_bone):
                    print('DEF-' + deform_bone + ' to : ' + deform_bone)
                    obj.vertex_groups.get('DEF-' + deform_bone).name = deform_bone

def get_main_object_from_object_with_name_suffix(object, suffixes = ['.Weight', '.Final', '.Upload', '.Arkit']):
    for suffix in suffixes:
        if suffix in object.name:
            object_name = object.name
            main_name = object_name.replace(suffix,'')
            main_object = bpy.data.objects.get(main_name ,None)
            if main_object:
                return main_object
    return object
            

set_armature_and_bone_name('METARIG')

for target_mesh in get_mesh_selection():
    weight_armature = bpy.data.objects[weight_armature_name]
    anim_armature = bpy.data.objects[anim_armature_name]
    
    hide_bones = []
    hide_bones.clear()
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    main_object = get_main_object_from_object_with_name_suffix(target_mesh)
    for vgroup in main_object.vertex_groups:
        if vgroup.lock_weight and not vgroup.name.startswith('_'):
            hide_bones.append(vgroup.name)

    target_mesh.select_set(True)
    weight_armature.select_set(True)

    bpy.context.view_layer.objects.active = weight_armature
    bpy.ops.object.mode_set(mode='POSE')
    anim_armature.data.pose_position = 'REST'
    weight_armature.data.pose_position = 'REST'
    bpy.ops.pose.reveal(select=False)
    bpy.ops.pose.select_all(action='DESELECT')

    for hb in hide_bones:
        try:
            weight_armature.pose.bones[hb].bone.hide = True
        except KeyError:
            pass

    bpy.ops.pose.select_all(action='SELECT')

    bpy.context.view_layer.objects.active = target_mesh

    ## Remove Weights From Locked Groups

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    for hb in hide_bones:
        try:
            vg_index = target_mesh.vertex_groups[hb].index
            target_mesh.vertex_groups.active_index = vg_index
            target_mesh.vertex_groups[vg_index].lock_weight = 0
            bpy.ops.object.vertex_group_remove_from(use_all_groups=False, use_all_verts=True)
            target_mesh.vertex_groups[vg_index].lock_weight = 1
        except KeyError:
            pass


    bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
    bpy.ops.paint.weight_from_bones(type='AUTOMATIC')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.ops.ed.undo_push(message = f"Activity: Undo Split fot {target_mesh.name}")
    print(f"Activity: Undo Split for {target_mesh.name}")
    
    # smooth to remove some weight artifacts
    bpy.context.view_layer.objects.active = target_mesh
    target_mesh.select_set(True)
    bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
    smooth_repeat = target_mesh.get('_rigWeight_smoothRepeat', 0)
    target_mesh['_rigWeight_smoothRepeat'] = smooth_repeat
    bpy.ops.object.vertex_group_smooth(group_select_mode='BONE_DEFORM', repeat = smooth_repeat)
    bpy.ops.object.vertex_group_clean(group_select_mode='BONE_DEFORM', limit=.001)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.ops.ed.undo_push(message = f"Activity: Undo Split fot {target_mesh.name}")
    print(f"Activity: Undo Split for {target_mesh.name}")
    
    if True: # a switch for -
        bpy.context.view_layer.objects.active = weight_armature
        bpy.ops.object.mode_set(mode='POSE')
        weight_armature.data.pose_position = 'POSE'
        anim_armature.data.pose_position = 'POSE'
    

set_armature_and_bone_name('METARIG') # rig_type = 'ANIMRIG' or 'METARIG'
