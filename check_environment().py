import bpy

"""
Objective/Purpose
    - checks add-ons 
    - mainly for checking gret avability since some scripts uses it
   
   
"""
addon_names = [
    ('gret-1_1_0',['Using 1.1.0 @ https://github.com/greisane/gret']),
    ('rigify',['(insert source)']),
    ('magic_uv',['(insert source)']),
    ('node_wrangler',['(insert source)']),
]

def check_addon(addon_name):
    # Iterate through all installed add-ons
    if bpy.context.preferences.addons.find(addon_name) > 0:
        return True
    else :
        return False

for addon_name, addon_source in addon_names:
    if not check_addon(addon_name):
        print(f"Add-on : {addon_name} is not installed. Activate it on preferences. \nAdd-on : {addon_name} is found from : {addon_source}")

