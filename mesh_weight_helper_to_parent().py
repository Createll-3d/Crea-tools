import bpy

def create_geometry_node():
    return

def get_mesh_selection():
    selected_objects = []
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            selected_objects.append(obj)
    return selected_objects

def add_weight_via_geometry_node(target_object, parent_bone_name, helper_bone_name):
    print(helper_bone_name + "->" + parent_bone_name)
    
    
    target_object.modifiers.new("_temp_HelperToParent", 'NODES')
    target_object.modifiers[len(target_object.modifiers)-1].node_group = bpy.data.node_groups['Util_HelperToParent']
    target_object.modifiers['_temp_HelperToParent']['Input_2'] = parent_bone_name
    target_object.modifiers['_temp_HelperToParent']['Input_3'] = helper_bone_name
        
    # Set-up Context
    bpy.context.view_layer.objects.active = target_object
    target_object.select_set(True)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Apply
    bpy.ops.object.modifier_move_to_index(modifier="_temp_HelperToParent", index=0)
    if target_object.active_shape_key:
        bpy.ops.gret.shape_key_apply_modifiers(modifier_mask=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    else:
        bpy.ops.object.modifier_apply(modifier="_temp_HelperToParent")

def get_helper_parent(armature, helper_bone_name):
    bpy.ops.object.mode_set(mode='OBJECT')
    helper_bone = armature.data.bones.get(helper_bone_name)
    print (helper_bone)
    if helper_bone:
        if 'helper' in helper_bone.name:
            return get_helper_parent(armature, helper_bone.parent.name)
        else:
            return helper_bone
    else:
        return

def merge_helper_to_parent(object, armature = None):
    if armature is None:
        try:
            armature = object.modifiers['Armature'].object
        except:
            print(f"{object.name} has no armature")
    vetex_group_collection = []
    
    for vertex_group in object.vertex_groups: # Might look redundant but removing will cause a decoding error -> suspected cause -> geometry node function reorders vertex groups in memory (?) 
        vetex_group_collection.append(vertex_group.name)
    
    for vertex_group in vetex_group_collection:
        if 'helper' in str(vertex_group):
            helper_bone_name = vertex_group
            if get_helper_parent(armature, helper_bone_name):
                parent_bone_name = get_helper_parent(armature, helper_bone_name).name
                add_weight_via_geometry_node(object, parent_bone_name, helper_bone_name)

                
create_geometry_node()

selected_objects = get_mesh_selection()
for object in selected_objects:
    merge_helper_to_parent(object)


# TODO:
# add a temporary override fix because for 'rig_anim' the parents are the 'ORG' bones and change it to the 'DEF' in post OR its about using the metarig one (?)
# add a funtion to unlink the shapekeys from the main then one that relinks it after the function is done
  # if we do that remove the gret check
# also it somehow didnt get rid of everything maybe its the parts that 

# DONE
# function for clean-up delete bones from armature 