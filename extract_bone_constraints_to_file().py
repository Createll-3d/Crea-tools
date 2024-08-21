import bpy
import json
import os

"""
Objective/Purpose
    - an attemp at saving bone contraints to a separate file
    - for keeping constrains after re-making metarig
    
 
To Do
    - check if working
    - dont know how i made this
"""

def serialize_constraint(constraint):

    constraint_dict = {"type": type(constraint).__name__}
    for key, value in constraint.bl_rna.properties.items():
        if key.startswith("rna_"):
            continue
        if value.is_readonly:
            continue
        if value.is_array:
            constraint_dict[key] = list(getattr(constraint, key))
        elif value.is_enum:
            constraint_dict[key] = getattr(constraint, key)
        else:
            val = getattr(constraint, key, None)
            if val is not None:
                constraint_dict[key] = val
    return constraint_dict


def save_constraints_to_file(context, filepath=None):

    selected_objects = bpy.context.selected_objects
    selected_bones = [bone for obj in selected_objects if obj.type == 'ARMATURE' for bone in obj.data.bones if bone.select]
    constraint_data = []
    for bone in selected_bones:
        bone_data = {"bone_name": bone.name, "constraints": []}
        for constraint in bone.constraints:
            serialized_constraint = serialize_constraint(constraint)
            bone_data["constraints"].append(serialized_constraint)
        constraint_data.append(bone_data)

    if not filepath:
        blend_filepath = bpy.data.filepath
        if not blend_filepath:
            raise Exception("Blend file must be saved first")
        filepath = os.path.splitext(blend_filepath)[0] + ".json"
    with open(filepath, 'w') as f:
        json.dump(constraint_data, f, indent=4)
    print("Constraints saved to", filepath)


def load_constraints_from_file(context, filepath=None):
   
    if not filepath:
        blend_filepath = bpy.data.filepath
        if not blend_filepath:
            raise Exception("Blend file must be saved first")
        filepath = os.path.splitext(blend_filepath)[0] + ".json"

    with open(filepath, 'r') as f:
        constraint_data = json.load(f)

    for bone_data in constraint_data:
        bone_name = bone_data["bone_name"]
        for obj in context.selected_objects:
            if obj.type == 'ARMATURE':
                bone = obj.data.bones.get(bone_name)
                if bone:
                    for serialized_constraint in bone_data["constraints"]:
                        constraint_type = serialized_constraint["type"]
                        constraint = getattr(bpy.types, constraint_type)()
                        for key, value in serialized_constraint.items():
                            if key != "type":
                                setattr(constraint, key, value)
                        bone.constraints.append(constraint)
                        print(f"Applied {constraint_type} constraint to {bone_name}")

save_constraints_to_file(bpy.context.selected_pose_bones)