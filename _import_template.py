import sys
import os
import importlib
sys.path.append(bpy.utils.script_paths()[2]) # change script path on blender or change this 
import _createll_script_utils
importlib.reload(_createll_script_utils)
from _createll_script_utils import (
    # only import whats necessary
)