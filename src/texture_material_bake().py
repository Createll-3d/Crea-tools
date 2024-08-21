import bpy

"""
Objective/Purpose
    - bakes textures 
	
Requires
	- a specific group node that has the first slot named '_BakeLayers'

To Do
    - needs better initializer (?) well everything needs a more consistent initiallizer
        - wcyd these are made on and off for different months 
    - a more robust way to get X node 
        - currently relying on the first output
        - idk the reason we didnt use name
            - because the names used for groups will always be 'Group.001'
    - still has a bug in blender 3.6.14 LTS 
        - after running it a few times it bugs "... cannot do while drawing/rendering ..."
    - was planning to teach this but i think its bad for both of us
"""

import re
import time

## Initialize User Values ##

output_dir = bpy.path.abspath("//Textures")

## Definitions ##

def find_group_node_via_output_index_0(material_name, find_node_identifier):
    # find_node_identifier = output_index_0
    for node in bpy.data.materials[material_name].node_tree.nodes:
        if node.outputs:
            if node.outputs[0].name == find_node_identifier:
                return (node)

def link_nodes_to_material_output(material, group_node, output_name):
    
    # Search using the "find_group_node_via_output_index_0" 
    
    output_socket = group_node.outputs[output_name]
    
    # Target Node // If for Future Usecase // currently targeted to material output
    material_node = find_node_by_base_name(material, 'Material Output')
    input_socket = material_node.inputs[0]
    
    # Creating the link between nodes 
    new_link = material.node_tree.links.new(output_socket, input_socket)

def remove_link_node(material_name, find_node_identifier, output_name):
    # Sample - remove_link_node('PAC062_Hair', '_BakeLayers', '_BakeLayers')
    
    # Searching using the "find_group_node_via_output_index_0"
    group_node = find_group_node_via_output_index_0(material_name, find_node_identifier)
    
    output_socket = group_node.outputs[output_name]
    if output_socket.links:
        while output_socket.links:
            link = output_socket.links[0]
            bpy.data.materials[material_name].node_tree.links.remove(link)

def set_active_node(material_name, find_node_identifier):
    
    # Searching using the "find_group_node_via_output_index_0" // Can change to a generic one in the future
    node = find_group_node_via_output_index_0 (material_name, find_node_identifier)
    
    node.select = True
    bpy.data.materials[material_name].node_tree.nodes.active = node
    
    print('Activity : Set Active Node -> ' + node.name)
    return

def set_active_bake_image_texture(image_layer_name):
    node_group = bpy.data.node_groups['RT_Bake_Group']
    
    for node in node_group.nodes:
        try:
            if node.image.name == image_layer_name:
                node_group.nodes[node.name].select = True
                node_group.nodes.active = node_group.nodes[node.name]
                print('Activity : Set Active Image -> ' + node.image.name)
                return
        except:
            pass
    
    raise RuntimeError("Image Not Found in BakeGroup : " + image_layer_name)

def set_active_image_texture(image_layer_name , node_group):

    for node in node_group.nodes:
        try:
            if node.image.name == image_layer_name:
                node_group.nodes[node.name].select = True
                node_group.nodes.active = node_group.nodes[node.name]
                print('Activity : Set Active Image -> ' + node.image.name)
                return
        except:
            pass
    
    raise RuntimeError(f'Image Not Found in {node_group.name} :  + {image_layer_name}')
    
def create_image_from_object_and_image_layer(object, image_layer_name, use_object_collection_name = False, width = 1024 , height = 1024):
    if use_object_collection_name:
        group_name = object.users_collection[0]
    else:
        group_name = object.name
    image_name = group_name + image_layer_name
    return bpy.data.images.new(image_name, width, height)

def bake_texture(bake_object, bake_texture_name, use_fake_user = True, file_format = 'OPEN_EXR'):        
    target_materials = {}
    
    for material_slot in bake_object.material_slots:
        
        bake_object_material = material_slot.material
        
        if not bpy.data.images.get(bake_texture_name, False):
            image_texture = bpy.data.images.new(bake_texture_name, width = 1024, height = 1024)
        else:
            image_texture = bpy.data.images.get(bake_texture_name)
        
        texture_image_node = bake_object_material.node_tree.nodes.new('ShaderNodeTexImage')
        texture_image_node.image = image_texture
        texture_image_node.select = True
        bake_object_material.node_tree.nodes.active = texture_image_node   
        target_materials[bake_object_material] = texture_image_node
    
    # Safety : Clean-Up
    for obj in bpy.context.scene.objects:
        obj.select_set(False)
    
    # Bake
    bake_object.select_set(True)
    bpy.context.view_layer.objects.active = bake_object
    bake_object_mesh = bpy.data.meshes.get(bake_object.data.name)
    bake_object_mesh.uv_layers.active_index = 0
    bpy.context.scene.render.bake.use_clear = False
    
    bpy.ops.object.bake(type='EMIT') # we are using EMIT only but if you would like to experiment with the ray-traced lights by all means try the other modes
    print('Activity : Baked -> ' + bake_object.name + ' to ' + bake_texture_name)
    time.sleep(2) # an attempt to prevent any bugs because of rendering not ending cleanly
    
    
    image_texture.use_fake_user = use_fake_user
    
    
    
    for material, texture_image_node in target_materials.items():
        material.node_tree.nodes.remove(texture_image_node)
    
    return

def get_previewed_socket(bake_object_material):
    material_output_node = find_node_by_base_name(bake_object_material, 'Material Output')
    previewed_socket = material_output_node.inputs[0].links[0].from_socket
    material_output_socket = material_output_node.inputs[0]
    return [previewed_socket, material_output_socket]

def find_node_by_base_name(material, base_name):
    for node in material.node_tree.nodes:
        if node.name.startswith(base_name):
            return node
    return None

def get_mesh_selection():
    selected_objects = []
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            selected_objects.append(obj)
    return selected_objects

def issue_warning(pop_title, pop_message):
    def draw(self, context):
        self.layout.label(text=pop_message)
        return
    bpy.context.window_manager.popup_menu(lambda self, context: draw(self, context), title=pop_title, icon='ERROR')


### Execution ###

## Initialize ##

bpy.ops.object.mode_set(mode='OBJECT')

initialize_mesh_selection = get_mesh_selection()

# Get current node attached to material output

## Bake ##

for bake_object in initialize_mesh_selection:
    bake_texture_list_completed = []
    texture_lists = set()
    preview_socket_dict = {}
    bake_object.data.uv_layers[0].active_render = True
#    bake_object_material = bake_object.material_slots[0].material # TODO : Raise Warning : were going to use the index 0
#    bake_layer_node = find_group_node_via_output_index_0(bake_object_material.name , '_BakeLayers')
    
    for material_slots in bake_object.material_slots:
        material = material_slots.material
        bake_layer_node = find_group_node_via_output_index_0(material.name , '_BakeLayers')
        preview_socket_dict[material] = get_previewed_socket(material)
        for output in bake_layer_node.outputs:
            if len(output.links) > 0:
                texture_lists.add(output.name)
    
    print(texture_lists)
    
    for output in texture_lists:
        for material_slots in bake_object.material_slots:
            material = material_slots.material
            bake_layer_node = find_group_node_via_output_index_0(material.name , '_BakeLayers')
            link_nodes_to_material_output(material, bake_layer_node, output)
            
            print(f'Activity : Link nodes to material output \t({material.name}, {bake_layer_node.name}, {output})')
            
        output_name_clean = re.sub(r'[^\w]','',output)
            
        if len(bake_object.get('_bakeTextureGroup', '')) <= 0:
            bake_texture_name = bake_object.material_slots[0].material.name + '_' + output_name_clean
        else:
            bake_texture_name = bake_object['_bakeTextureGroup'] + '_' + output_name_clean
        
        bake_texture(bake_object, bake_texture_name)
        
        #save but coded to be open exr
        image_texture = bpy.data.images[bake_texture_name]
        image_texture.file_format = 'OPEN_EXR'
        file_path = output_dir+"\\"+bake_texture_name+".exr"
        image_texture.save_render(filepath=file_path, scene = bpy.data.scenes['04 Final Scene'])
        if image_texture.source != 'FILE':
            image_texture.source = 'FILE'
            image_texture.filepath = file_path
            image_texture.colorspace_settings.name = 'Linear'
        
        bake_texture_list_completed.append(bake_texture_name)
    
    for material_slots in bake_object.material_slots:
        material = material_slots.material
        for material, (from_socket, to_socket) in preview_socket_dict.items():
            material.node_tree.links.new(from_socket, to_socket)

#    for output in bake_layer_node.outputs:
#        if len(output.links) > 0:
#            group_node = find_group_node_via_output_index_0(material_name, find_node_identifier)
#            
#            link_nodes_to_material_output(bake_object_material.name, group_node, output.name)
#            
#            output_name_clean = re.sub(r'[^\w]','',output.name)
#            
#            if len(bake_object.get('_bakeTextureGroup', '')) <= 0:
#                bake_texture_name = bake_object_material.name + '_' + output_name_clean
#            else:
#                bake_texture_name = bake_object['_bakeTextureGroup'] + '_' + output_name_clean
#            
#            bake_texture(bake_object, bake_texture_name)
#            
#            bake_texture_list_completed.append(bake_texture_name)
            
    # Clean-Up - Re-Attach original node to material Output
     
    print("Completed bake for the following : " + ", ".join(bake_texture_list_completed))
    # TODO : check -> create image texture -> organize ? I guess it goes by row -> connect to UV_Bake
    

## Clean-Up ##

# Re-Select Affected Objects
for scene_object in bpy.context.scene.objects:
    scene_object.select_set(False)

for bake_object in initialize_mesh_selection:
    bake_object.select_set(True)
    
# Re-Attach original node to material Output

