import sys
import os
import bpy

blend_dir = os.path.basename(bpy.data.filepath)
if blend_dir not in sys.path:
   sys.path.append(blend_dir)

blend_dir = "/home/stepcut/n-heptane/projects/blender/gothedral2.0"
if blend_dir not in sys.path:
   sys.path.append(blend_dir)

