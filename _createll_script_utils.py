import bpy

# probably need to break this down

# Selection Utility
def get_mesh_selection():
    selected_objects = []
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            selected_objects.append(obj)
    print(f"Activity: Get selected objects : {selected_objects}")
    return selected_objects

def set_object_active(object):
    if not bpy.context.window.scene in object.users_scene:
        bpy.context.window.scene = object.users_scene[0]
        
    bpy.context.view_layer.objects.active = object
    return object

# Mesh Functions

def apply_modifiers_till_modifier_type_via_gret(object, modifier_type):
    index = 0
    set_object_active(object)
    object.select_set(True)
    
    for modifier in object.modifiers:
        if modifier.type == modifier_type:
            modifier_index = index
            modifier_mask = tuple(modifier_index >= i for i in range(32))
            try:
                bpy.ops.gret.shape_key_apply_modifiers(modifier_mask=modifier_mask)
                return
            except:
                raise print('Please Install Gret Add-on')
        index += 1

def apply_modifiers_via_gret(object):
    if object and object.type == 'MESH':
        set_object_active(object)
        try:
            bpy.ops.gret.shape_key_apply_modifiers()
        except:
            raise print('Please Install Gret Add-on')
    return

def clean_mesh_modifiers(object, modifier_names): # where we can input stuff we want to delete or adjusts
    set_object_active(object)
    remove_modifier_names = []

    for modifier in object.modifiers: # doing it like this because reading while modifying produces memory targeting errors
        if (modifier.name in modifier_names) or (modifier.type == 'NODES') or (not modifier.show_viewport) :
            remove_modifier_names.append(modifier.name)
    
    for modifier_name in remove_modifier_names:
        bpy.ops.object.modifier_remove(modifier = modifier_name)

def remove_modifier_by_type(object, modifier_type_lists): # 'ARMATURE', 'SURFACE_DEFORM', 'NODES'
    set_object_active(object)
    remove_modifier_names = []

    for modifier in object.modifiers: # doing it like this because reading while modifying produces memory targeting errors
        if (modifier.type in modifier_type_lists) :
            remove_modifier_names.append(modifier.name)
    
    for modifier_name in remove_modifier_names:
        bpy.ops.object.modifier_remove(modifier = modifier_name)

def remove_modifier_by_name(object, modifier_name): 
    if object.modifiers.get(modifier_name).type == 'ARMATURE':
        write_armature_data_to_custom_properties(object)
    
    set_object_active(object)
    bpy.ops.object.modifier_remove(modifier = modifier_name)


def create_surface_deform_modifier(object, target_object, mod_index = 0):
    set_object_active(object)
    
    mod_index = min(mod_index, len(object.modifiers)-1)
    
    modifier = object.modifiers.new('SurfaceDeform', 'SURFACE_DEFORM')
    
    modifier.target = target_object
    bpy.ops.object.modifier_move_to_index(modifier = modifier.name, index = mod_index)
    bpy.ops.object.surfacedeform_bind(modifier = modifier.name)

def duplicate_mesh_object(object, copy_suffix = '.duplicate', copy_collection = None, replace_mesh = False): #bpy.context.collection
    if copy_collection is None:
        copy_collection = object.users_collection[0]
    
    if object and object.type == 'MESH':
        if replace_mesh or not bpy.data.objects.get(object.name + copy_suffix, False):
            if bpy.data.objects.get(object.name + copy_suffix, False):
                new_object = bpy.data.objects.get(object.name + copy_suffix, False)
                if not new_object.data.shape_keys == None:
                    new_object.shape_key_clear()
                bpy.data.objects.remove(new_object)
            
            new_object = object.copy()
            new_object.data = object.data.copy()
            new_object.animation_data_clear()
            new_object.name = object.name + copy_suffix
            
            copy_collection.objects.link(new_object)
            return new_object
        else:
            new_obj = bpy.data.objects.get(object.name + copy_suffix)
            link_object_to_collection(new_object, copy_collection)
            return new_object
    else:
        print("Select a mesh object to duplicate.")


# Object Functions


def change_customProperty_name(object, new_name, old_name):
    if old_name in object.keys():
        object[new_name] = object[old_name]
        del object[old_name]
        

def link_collections_to_scene(scene, collection_names_lists):
    for collection_name in collection_names_lists:
        try:
            scene.collection.children.link(bpy.data.collections.get(collection_name))
        except:
            None
            
def link_object_to_collection(object, target_collection):
    try:
        for collection in object.users_collection:
            collection.objects.unlink(object)
        
        target_collection.objects.link(object)
    except:
        None

# Rig toggles

def get_rig_type_count(mesh_lists = get_mesh_selection(), is_toggle = False):
    rig_count = 0
    for object in mesh_lists:
        if object.modifiers.get('Armature', False):
            if get_rig_name(object) == 'metarig':
                rig_count += 1
            else:
                rig_count -= 1
        else:
            continue
    if is_toggle:
        rig_count_type = 'METARIG' if rig_count < 0 else 'ANIMRIG'
    else:
        rig_count_type = 'ANIMRIG' if rig_count < 0 else 'METARIG'
    return rig_count_type

def get_rig_name(object):
    " Used for a secure rig state check "
    if object.modifiers.get('Armature',False):
        object['_rig_name'] = object.modifiers.get('Armature').object.name
    elif object.get('_rig_name',False):
        object['_rig_name'] = object['_rig_name']
    else :
        object['_rig_name'] = 'metarig'
    return object['_rig_name']

def get_modifier_index_by_name(object, modifier_name):
    index = 0
    for modifier in object.modifiers:
        if modifier.name == modifier_name:
            return index
        index += 1
    return None

def create_armature_modifier(object, armature_object = None, mod_index = 0):

    if armature_object is None:
        armature_object = bpy.data.objects.get(object['_rig_name'])
    
    set_object_active(object)
    mod_index = min(mod_index, len(object.modifiers))
    modifier = object.modifiers.new('Armature', 'ARMATURE')

    modifier.object = armature_object #bpy.data.objects['rig_anim']
    bpy.ops.object.modifier_move_to_index(modifier = modifier.name, index = mod_index)
    
    write_armature_data_to_custom_properties(object, modifier.name)

def write_armature_data_to_custom_properties(object, modifier_name = 'Armature'):
    armature_modifier = object.modifiers.get(modifier_name, False)
    if armature_modifier:
        object['_rig_name'] = armature_modifier.object.name
        object['_rig_mod_index'] = get_modifier_index_by_name(object, modifier_name)
        print (f"Activity: Set {object.name}['_rig_name'] = {object['_rig_name']}")
        print (f"Activity: Set {object.name}['_rig_mod_index'] = {object['_rig_mod_index']}")


def set_armature_and_bone_name(rig_type, weight_armature = bpy.data.armatures['metarig'], anim_armature = bpy.data.armatures['rig_anim'], mesh_lists = get_mesh_selection()):
    # rig_type = 'ANIMRIG' or 'METARIG'
    print(f"Activity: Setting Rig Style to {rig_type}")
    
    standard_rigify_deform_bones = set(['spine', 'pelvis.L', 'pelvis.R', 'thigh.L', 'thigh.L.001', 'shin.L', 'shin.L.001', 'foot.L', 'toe.L', 'thigh.R', 'thigh.R.001', 'shin.R', 'shin.R.001', 'foot.R', 'toe.R', 'temple.L', 'temple.R', 'tongue', 'chin', 'chin.001', 'chin.L', 'chin.R', 'jaw', 'jaw.L.001', 'jaw.R.001', 'tongue.001', 'tongue.002', 'cheek.T.L', 'cheek.T.R', 'jaw.L', 'jaw.R', 'nose', 'nose.L', 'nose.R', 'cheek.B.L.001', 'cheek.B.R.001', 'cheek.B.L', 'cheek.B.R',  'nose.002', 'nose.001', 'nose.003', 'nose.004', 'nose.L.001', 'nose.R.001', 'cheek.T.L.001', 'cheek.T.R.001', 'shoulder.L', 'upper_arm.L', 'upper_arm.L.001', 'forearm.L', 'forearm.L.001', 'hand.L', 'f_index.01.L', 'f_index.02.L', 'f_index.03.L', 'thumb.01.L', 'thumb.02.L', 'thumb.03.L', 'palm.01.L', 'f_middle.01.L', 'f_middle.02.L', 'f_middle.03.L', 'palm.02.L', 'f_ring.01.L', 'f_ring.02.L', 'f_ring.03.L', 'palm.03.L', 'f_pinky.01.L', 'f_pinky.02.L', 'f_pinky.03.L', 'palm.04.L', 'shoulder.R', 'upper_arm.R', 'upper_arm.R.001', 'forearm.R', 'forearm.R.001', 'hand.R', 'f_index.01.R', 'f_index.02.R', 'f_index.03.R', 'thumb.01.R', 'thumb.02.R', 'thumb.03.R', 'palm.01.R', 'f_middle.01.R', 'f_middle.02.R', 'f_middle.03.R', 'palm.02.R', 'f_ring.01.R', 'f_ring.02.R', 'f_ring.03.R', 'palm.03.R', 'f_pinky.01.R', 'f_pinky.02.R', 'f_pinky.03.R', 'palm.04.R'])
    standard_rigify_deform_bones_substrings = ['spine.', 'lid.', 'lip.', 'brow.', 'teeth.', 'forehead.', 'heel.', 'ear.']

    if not weight_armature or not anim_armature:
        print("Armature not found in bpy.data.armatures")
        return

    for bone in weight_armature.bones:
        if 'helper' not in bone.name:
            if any(substring in bone.name for substring in standard_rigify_deform_bones_substrings):
                standard_rigify_deform_bones.add(bone.name)

    for obj in mesh_lists:
        
        if not obj.modifiers.get('Armature', False):
            continue
        
        obj_aramture_modifier_object = obj.modifiers.get('Armature').object
        
        print(f"Activity: Setting Rig Style of {obj.name} to {rig_type}")
        
        if rig_type == 'ANIMRIG' or rig_type == 'rig_anim':
            
            obj['_rig_name'] = 'rig_anim'
            obj.modifiers.get('Armature').object = bpy.data.objects.get(obj['_rig_name'])
            write_armature_data_to_custom_properties(obj)
            
            for deform_bone in standard_rigify_deform_bones:
                if obj.vertex_groups.get(deform_bone):
                    obj.vertex_groups.get(deform_bone).name = 'DEF-' + deform_bone
            
        elif rig_type == 'METARIG' or rig_type == 'rig_metarig':
            
            obj['_rig_name'] = 'metarig'
            obj.modifiers.get('Armature').object = bpy.data.objects.get(obj['_rig_name'])
            write_armature_data_to_custom_properties(obj)
            
            for deform_bone in standard_rigify_deform_bones:
                if obj.vertex_groups.get('DEF-' + deform_bone):
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