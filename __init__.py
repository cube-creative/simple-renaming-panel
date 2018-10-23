import bpy
from .simple_renaming_ui import *


bl_info = {
    "name": "Simple Renaming Panel",
    "description": "This Addon offers a basic functionality to rename a set of objects",
    "author": "Matthias Patscheider",
    "version": (1, 2, 1),
    "blender": (2, 79, 0),
    "location": "View3D > Tools ",
    "warning": "",
    "wiki_url": "https://github.com/Weisl/simple_renaming_panel",
    "tracker_url": "https://github.com/Weisl/simple_renaming_panel/issues",
    "support": "COMMUNITY",
    "category": "Object"
}


def register():
    # addon properties and classes
    simple_renaming_ui.WindowManager.renaming_sufpre_type = simple_renaming_ui.EnumProperty(
        name="Suffix or Prefix by Type",
        items=(('SUF', "Suffix", "suffix"),
               ('PRE', "Prefix", "prefix"),),
        description="Add Prefix or Suffix to type",
    )
    simple_renaming_ui.WindowManager.renaming_object_types = simple_renaming_ui.EnumProperty(
        name="Renaming Objects",
        items=(('OBJECT', "Object", "Scene Objects"),
               ('MATERIAL', "Material", "Materials"),
               ('IMAGE', "Image Textures", "Image Textures"),
               ('GROUP', "Group", "Group"),
               ('DATA', "Data", "Object Data"),
               ('BONE', "Bone", "Bones")),
        description="Which kind of object to rename",
    )
    # ideas UvMaps, vertexgroups, shape keys, blender textures
    windowVariables

    WindowManager.renaming_newName = StringProperty(name="New Name", default='')
    WindowManager.renaming_search = StringProperty(name='Search', default='')
    WindowManager.renaming_replace = StringProperty(name='Replace', default='')
    WindowManager.renaming_suffix = StringProperty(name="Suffix", default='')
    WindowManager.renaming_prefix = StringProperty(name="Prefix", default='')
    WindowManager.rename_only_selection = BoolProperty(
        name="Selected Objects",
        description="Rename Selected Objects",
        default=True,
    )
    WindowManager.rename_matchcase = BoolProperty(
        name="Match Case",
        description="",
        default=True,
    )
    WindowManager.renaming_base_numerate = IntProperty(name="Step Size", default=1)
    WindowManager.renaming_numerate_separator = StringProperty(name="Numerate Separator", default="")
    WindowManager.renaming_digits_numerate = IntProperty(name="Number Length", default=3)
    WindowManager.renaming_cut_size = IntProperty(name="Trim Size", default=3)
    WindowManager.renaming_messages = RenamingMessages()
    WindowManager.renaming_sufpre_material = StringProperty(name='Material', default='')
    WindowManager.renaming_sufpre_geometry = StringProperty(name='Geometry', default='')
    WindowManager.renaming_sufpre_empty = StringProperty(name="Empty", default='')
    WindowManager.renaming_sufpre_group = StringProperty(name="Group", default='')
    WindowManager.renaming_sufpre_curve = StringProperty(name="Curve", default='')
    WindowManager.renaming_sufpre_armature = StringProperty(name="Armature", default='')
    WindowManager.renaming_sufpre_lattice = StringProperty(name="Lattice", default='')
    WindowManager.renaming_sufpre_data = StringProperty(name="Data", default='')
    WindowManager.renaming_sufpre_data_02 = StringProperty(name="Data = Objectname + ", default='')

    WindowManager.renaming_sufpre_surfaces = StringProperty(name="Surfaces", default='')
    WindowManager.renaming_sufpre_cameras = StringProperty(name="Cameras", default='')
    WindowManager.renaming_sufpre_lights = StringProperty(name="Lights", default='')
    WindowManager.renaming_sufpre_bones = StringProperty(name="Bones", default='')


    bpy.utils.register_class(VIEW3D_tools_Renaming_Panel)
    bpy.utils.register_class(Addsuffix)
    bpy.utils.register_class(AddPrefix)
    bpy.utils.register_class(SearchAndReplace)
    bpy.utils.register_class(RenamingNumerate)
    bpy.utils.register_class(AddTypeSufPre)
    bpy.utils.register_class(TrimString)
    bpy.utils.register_class(UseObjectnameForData)
    bpy.utils.register_class(RENAMING_POPUP)
    bpy.utils.register_class(ReplaceName)


def unregister():
    # delete all the addon updaters and so one
    del WindowManager.renaming_search
    del WindowManager.renaming_newName
    del WindowManager.renaming_object_types
    del WindowManager.renaming_replace
    del WindowManager.renaming_suffix
    del WindowManager.renaming_prefix
    del WindowManager.rename_only_selection
    del WindowManager.renaming_base_numerate
    del WindowManager.renaming_numerate_separator
    del WindowManager.renaming_digits_numerate
    del WindowManager.renaming_cut_size

    del WindowManager.renaming_sufpre_material
    del WindowManager.renaming_sufpre_geometry
    del WindowManager.renaming_sufpre_empty
    del WindowManager.renaming_sufpre_group
    del WindowManager.renaming_sufpre_curve
    del WindowManager.renaming_sufpre_armature
    del WindowManager.renaming_sufpre_lattice
    del WindowManager.renaming_sufpre_data

    del WindowManager.renaming_sufpre_data_02

    del WindowManager.renaming_sufpre_lights
    del WindowManager.renaming_sufpre_cameras
    del WindowManager.renaming_sufpre_surfaces
    del WindowManager.renaming_sufpre_bones

    bpy.utils.unregister_class(VIEW3D_tools_Renaming_Panel)
    bpy.utils.unregister_class(AddTypeSufPre)
    bpy.utils.unregister_class(Addsuffix)
    bpy.utils.unregister_class(AddPrefix)
    bpy.utils.unregister_class(SearchAndReplace)
    bpy.utils.unregister_class(RenamingNumerate)
    bpy.utils.unregister_class(TrimString)
    bpy.utils.unregister_class(UseObjectnameForData)
    bpy.utils.unregister_class(ReplaceName)
    bpy.utils.unregister_class(RENAMING_POPUP)
