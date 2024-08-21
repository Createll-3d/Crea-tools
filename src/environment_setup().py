import bpy

""" 
Objective/Purpose
    - setup a blank file to what we need 
    
To Do
    - needs to be changed to work on a fresh file
 """


scene_setup_dict = {
    '01 Main Scene':{'suffix' : None, 'pre_collection' : ''},
    '02 Rig Scene':{'suffix' : '.Weight', 'pre_collection' : ''},
    '03 ARkit Scene':{'suffix' : '.ARkit', 'pre_collection' : ''},
    '04 Final Scene':{'suffix' : '.Final', 'pre_collection' : ''},
}

def create_copy_collections(parent_collection, copy_suffix = '', depth = 0):
    depth += 1
    for children_collection in parent_collection.children:
        
        if len(children_collection.children) > 0:
            if not bpy.data.collections.get(parent_collection.name + copy_suffix, False):
                copy_parent_collection = bpy.data.collections.new(parent_collection.name + copy_suffix)
                copy_children_collection = create_copy_collections(children_collection, copy_suffix, depth)[0]
                copy_parent_collection.children.link(copy_children_collection)
            else:
                copy_parent_collection = bpy.data.collections.get(parent_collection.name + copy_suffix, False)

        elif not bpy.data.collections.get(children_collection.name + copy_suffix, False):
            copy_children_collection = bpy.data.collections.new(children_collection.name + copy_suffix)
            copy_parent_collection.children.link(copy_children_collection)
        else:
            copy_children_collection = bpy.data.collections.get(children_collection.name + copy_suffix, False)

    return [copy_parent_collection, copy_children_collection]

def search_names_by_property(dictionary, property, search_key):
    results = []
    for name, properties in dictionary.items():
        # Check if the suffix matches
        if properties[property] == search_key:
            results.append(name)
    return results


#print (create_copy_collections(bpy.data.collections['Texture Bake'],'.Final')[0].name)

def filter_collections_to_link_by_scene_dictionary(scene_setup_dict, collection_selection = bpy.data.collections ):
    collections_to_link = []
    for collection in collection_selection:
        for scene_name, scene_properties in scene_setup_dict.items():
            suffix = scene_properties.get('suffix')
            scene = bpy.data.scenes.get(scene_name)
            if suffix is None:
                continue # do not change
            elif collection.name.endswith(suffix):
                collections_to_link.append(collection)
    collection_selection = collections_to_link
    return collection_selection

def filter_collections_to_link_by_heirchy(collection_selection):
    collections_to_remove = set()
    
    for collection in collection_selection:
        for collection_child in collection.children_recursive:
            collections_to_remove.add(collection_child)
    
    return [collection for collection in collection_selection if collection not in collections_to_remove]

def filer_existence():
    #??? and filters for if needs update but aaa too much feature creep for being fool proof when we couldve just hard coded it
    

print(filter_collections_to_link_by_heirchy(filter_collections_to_link_by_scene_dictionary(scene_setup_dict)))


print(f'=============================')