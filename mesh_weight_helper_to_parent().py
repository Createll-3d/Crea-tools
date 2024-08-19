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

                

def clear_shapekeys(object):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = object
    object.select_set(True)
    bpy.ops.object.shape_key_remove(all=True)
    object.select_set(False)

def extract_shape_keys_vertex_positons(object):
    bpy.ops.object.mode_set(mode='OBJECT')
    shape_keys_vertex_positons = {}
    shape_keys = object.data.shape_keys.key_blocks
    
    for shape_key in shape_keys:
        if shape_key.name != "Basis":
            shape_keys_vertex_positons[shape_key.name] = [shape_key.data[i].co.copy() for i in range(len(shape_key.data))]
    return shape_keys_vertex_positons

def reconstruct_shape_keys_vertex_positons(object, vertex_data):
    """ Reconstruct shape keys in the specified object using extracted vertex data. """
    # Ensure you're in Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # incase we dicide to also get Basis from original state mesh
    if "Basis" in vertex_data:
        for i, vertex_location in enumerate(vertex_data["Basis"]):
            basis_shape_key_data[i].co = vertex_location
    else:
        bpy.context.view_layer.objects.active = object
        object.select_set(True)
        bpy.ops.object.shape_key_add(from_mix=False)
        object.select_set(False)
       

    for shape_key_name, vertices in vertex_data.items():
        if shape_key_name != "Basis":

            new_shape_key = object.shape_key_add(name=shape_key_name, from_mix=False)
            shape_key_data = new_shape_key.data
            
            for i, vertex_location in enumerate(vertices):
                shape_key_data[i].co = vertex_location
        
        print(f"Activity: Reconstructing {shape_key_name}")
    
    object.data.update()
    print(f"Activity: Reconstructing Shapekeys Finished")

print(f"--------------------------------\nActivity: Starting")
create_geometry_node() #if we want it truly automated; also dont forget that we still need to mention that geometryn node

selected_objects = get_mesh_selection()
for object in selected_objects:
    shape_key_vertex_data = extract_shape_keys_vertex_positons(object)
    clear_shapekeys(object)
    merge_helper_to_parent(object)
    reconstruct_shape_keys_vertex_positons(object, shape_key_vertex_data)


# TODO:
# add a temporary override fix because for 'rig_anim' the parents are the 'ORG' bones and change it to the 'DEF' in post OR its about using the metarig one (?)
# also it somehow didnt get rid of everything maybe its the parts that 

# DONE
# function for clean-up delete bones from armature 
# add a funtion to unlink the shapekeys from the main then one that relinks it after the function is done
  # if we do that remove the gret check