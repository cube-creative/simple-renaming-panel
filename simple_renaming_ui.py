'''
Copyright (C) 2017 Matthias Patscheider
patscheider.matthias@gmail.com

Created by Matthias Patscheider

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import bpy
import re
import os
from os.path import *

from bpy.types import WindowManager
from bpy.types import Scene


from bpy.props import (
    StringProperty,
    EnumProperty,
    BoolProperty,
    FloatProperty,
    IntProperty
)


#######################################
######### RENAMING
#######################################



class RenamingMessages():
    message = []

    @classmethod
    def addMessage(cls, oldName, newName, obType=False, obIcon=False, warning=False):
        dict = {'oldName': oldName, 'newName': newName, 'obType': obType, 'obIcon': obIcon, 'warning': warning}
        cls.message.append(dict)
        return

    @classmethod
    def getMessages(cls):
        return cls.message

    @classmethod
    def printAll(cls):
        print("Print All " + str(list(cls.message)))
        return

    @classmethod
    def clear(cls):
        cls.message = []


class VIEW3D_tools_Renaming_Panel(bpy.types.Panel):
    """Creates a renaming Panel"""
    bl_label = "Simple Renaming Panel"
    bl_space_type = 'VIEW_3D'  # Choosing Viewport
    bl_region_type = 'TOOLS'  # Choosing tools panel in viewport
    bl_category = "Cube"

    def draw(self, context):



        layout = self.layout
        wm = context.window_manager
        scene = context.scene

        row = layout.row()
        row.prop(wm, "renaming_object_types", expand=True)

        labelStr = "Renaming Mode: "
        row = layout.row()
        if wm.renaming_object_types == 'OBJECT':
            row.label(labelStr + "Object")
        elif wm.renaming_object_types == 'MATERIAL':
            row.label(text=labelStr + "Material")
        elif wm.renaming_object_types == 'GROUP':
            row.label(text=labelStr + "Group")
        elif wm.renaming_object_types == 'IMAGE':
            row.label(text=labelStr + "Image Texture")
        elif wm.renaming_object_types == 'DATA':
            row.label(text=labelStr + "Object Data")
        elif wm.renaming_object_types == 'BONE':
            row.label(text=labelStr + "Bones")

        row = layout.row()
        if str(wm.renaming_object_types) == 'MATERIAL' or str(wm.renaming_object_types) == 'DATA':
            row.prop(wm, "rename_only_selection", text="Only Of Selected Objects")
        elif str(wm.renaming_object_types) == 'OBJECT':
            row.prop(wm, "rename_only_selection", text="Only Selected")
        elif str(wm.renaming_object_types) == 'BONE':
            row.prop(wm, "rename_only_selection", text="Only Selected")

        row.separator()

        row = layout.row()
        row.prop(wm, "renaming_newName")
        row = layout.row()

        row.operator("renaming.name_replace")

        row = layout.row()
        row.prop(wm, "renaming_search")
        row.prop(wm, "renaming_replace")
        row = layout.row()
        row.prop(wm, "rename_matchcase")
        row = layout.row()
        row.operator("renaming.search_replace")

        row = layout.row()
        row.prop(wm, "renaming_prefix")

        row = layout.row()
        row.operator("renaming.add_prefix")

        row = layout.row()
        row.prop(wm, "renaming_suffix")

        row = layout.row()
        row.operator("renaming.add_suffix")

        row = layout.row()
        row.prop(wm,"renaming_numerate_separator")

        row = layout.row()
        # row = box.row()
        # row.prop(wm,"renaming_base_numerate")
        row = layout.row()
        row.prop(wm, "renaming_digits_numerate")
        row = layout.row()
        row.operator("renaming.numerate")

        row = layout.row()
        row.prop(wm, "renaming_cut_size")
        row = layout.row()
        row.operator("renaming.cut_string")

        if str(wm.renaming_object_types) == 'DATA':
            row = layout.row()
            row.prop(wm, "renaming_sufpre_data_02")
            row = layout.row()
            row.operator("renaming.dataname_from_obj")

        box = layout.box()
        row = box.row()
        row.prop(wm, "renaming_sufpre_type", expand=True)
        row = box.row()
        if wm.renaming_sufpre_type == "PRE":
            row.label("Add Type Prefix")
        else:
            row.label("Add Type Suffix")

        row = box.row()
        row.prop(wm, "renaming_sufpre_geometry")
        row = box.row()
        row.prop(wm, "renaming_sufpre_material")
        row = box.row()
        row.prop(wm, "renaming_sufpre_empty")
        row = box.row()
        row.prop(wm, "renaming_sufpre_curve")
        row = box.row()
        row.prop(wm, "renaming_sufpre_armature")
        row = box.row()
        row.prop(wm, "renaming_sufpre_group")
        row = box.row()
        row.prop(wm, "renaming_sufpre_lattice")
        row = box.row()
        row.prop(wm, "renaming_sufpre_data")

        row = box.row()
        row.prop(wm, "renaming_sufpre_surfaces")
        row = box.row()
        row.prop(wm, "renaming_sufpre_cameras")
        row = box.row()
        row.prop(wm, "renaming_sufpre_lights")
        row = box.row()
        row.prop(wm, "renaming_sufpre_bones")

        row = box.row()
        row.operator("renaming.add_sufpre_by_type")


class AddTypeSufPre(bpy.types.Operator):
    """Add Type Suffix"""
    bl_idname = "renaming.add_sufpre_by_type"
    bl_label = "Add Type Suffix or Prefix"
    bl_description = "Adds the above defined Suffixes or Prefixes to all objects in your scene"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):
        wm = context.window_manager

        geo_sufpre = wm.renaming_sufpre_geometry
        mat_suffix = wm.renaming_sufpre_material
        empt_sufpre = wm.renaming_sufpre_empty
        lattice_suffix = wm.renaming_sufpre_lattice
        curve_suffix = wm.renaming_sufpre_curve
        group_suffix = wm.renaming_sufpre_group
        armature_suffix = wm.renaming_sufpre_armature
        data_suffix = wm.renaming_sufpre_data
        surfaces_sufpre = wm.renaming_sufpre_surfaces
        light_sufpre = wm.renaming_sufpre_lights
        bone_sufpre = wm.renaming_sufpre_bones
        camera_sufpre = wm.renaming_sufpre_cameras

        if camera_sufpre is not '' or light_sufpre is not '' or surfaces_sufpre is not '' or geo_sufpre is not '' or empt_sufpre is not '' or lattice_suffix is not '' or data_suffix is not '':
            for obj in bpy.data.objects:
                if light_sufpre is not '':
                    if obj.type == 'LAMP':
                        oldName = obj.name
                        nameIsNew = True
                        if wm.renaming_sufpre_type == 'SUF':
                            if obj.name.endswith(light_sufpre) == False:
                                newName = self.sufpreAdd(context, obj, light_sufpre)
                            else:
                                nameIsNew = False
                        else:
                            if obj.name.startswith(light_sufpre) == False:
                                newName = self.sufpreAdd(context, obj, light_sufpre)
                            else:
                                nameIsNew = False
                        if nameIsNew == True:
                            obj.name = newName
                            wm.renaming_messages.addMessage(oldName, obj.name, 'LAMP', 'LAMP')

                if surfaces_sufpre is not '':
                    if obj.type == 'SURFACE':
                        oldName = obj.name
                        nameIsNew = True
                        if wm.renaming_sufpre_type == 'SUF':
                            if obj.name.endswith(surfaces_sufpre) == False:
                                newName = self.sufpreAdd(context, obj, surfaces_sufpre)
                            else:
                                nameIsNew = False
                        else:
                            if obj.name.startswith(surfaces_sufpre) == False:
                                newName = self.sufpreAdd(context, obj, surfaces_sufpre)
                            else:
                                nameIsNew = False
                        if nameIsNew == True:
                            obj.name = newName
                            wm.renaming_messages.addMessage(oldName, obj.name, 'SURFACE', 'OUTLINER_OB_SURFACE')

                if camera_sufpre is not '':
                    if obj.type == 'CAMERA':
                        oldName = obj.name
                        nameIsNew = True
                        if wm.renaming_sufpre_type == 'SUF':
                            if obj.name.endswith(camera_sufpre) == False:
                                newName = self.sufpreAdd(context, obj, camera_sufpre)
                            else:
                                nameIsNew = False
                        else:
                            if obj.name.startswith(camera_sufpre) == False:
                                newName = self.sufpreAdd(context, obj, camera_sufpre)
                            else:
                                nameIsNew = False
                        if nameIsNew == True:
                            obj.name = newName
                            wm.renaming_messages.addMessage(oldName, obj.name, 'CAMERA', 'OUTLINER_OB_CAMERA')

                if geo_sufpre is not '':
                    if obj.type == 'MESH':
                        oldName = obj.name
                        nameIsNew = True
                        if wm.renaming_sufpre_type == 'SUF':
                            if obj.name.endswith(geo_sufpre) == False:
                                newName = self.sufpreAdd(context, obj, geo_sufpre)
                            else:
                                nameIsNew = False
                        else:
                            if obj.name.startswith(geo_sufpre) == False:
                                newName = self.sufpreAdd(context, obj, geo_sufpre)
                            else:
                                nameIsNew = False
                        if nameIsNew == True:
                            obj.name = newName
                            wm.renaming_messages.addMessage(oldName, obj.name, 'MESH', 'OUTLINER_OB_MESH')

                if empt_sufpre is not '':
                    if obj.type == 'EMPTY':
                        oldName = obj.name
                        nameIsNew = True
                        if wm.renaming_sufpre_type == 'SUF':
                            if obj.name.endswith(empt_sufpre) == False:
                                newName = self.sufpreAdd(context, obj, empt_sufpre)
                            else:
                                nameIsNew = False
                        else:
                            if obj.name.startswith(empt_sufpre) == False:
                                newName = self.sufpreAdd(context, obj, empt_sufpre)
                            else:
                                nameIsNew = False
                        if nameIsNew == True:
                            obj.name = newName
                            wm.renaming_messages.addMessage(oldName, obj.name, 'EMPTY', 'OUTLINER_OB_EMPTY')

                if lattice_suffix is not '':
                    if obj.type == 'LATTICE' and obj.name.endswith(lattice_suffix) == False:
                        oldName = obj.name
                        nameIsNew = True
                        if wm.renaming_sufpre_type == 'SUF':
                            if obj.name.endswith(lattice_suffix) == False:
                                newName = self.sufpreAdd(context, obj, lattice_suffix)
                            else:
                                nameIsNew = False
                        else:
                            if obj.name.startswith(lattice_suffix) == False:
                                newName = self.sufpreAdd(context, obj, lattice_suffix)
                            else:
                                nameIsNew = False

                        if nameIsNew == True:
                            obj.name = newName
                            wm.renaming_messages.addMessage(oldName, obj.name, 'LATTICE', 'OUTLINER_OB_LATTICE')

                if curve_suffix is not '':
                    if obj.type == 'CURVE' and obj.name.endswith(curve_suffix) == False:
                        oldName = obj.name
                        nameIsNew = True
                        if wm.renaming_sufpre_type == 'SUF':
                            if obj.name.endswith(curve_suffix) == False:
                                newName = self.sufpreAdd(context, obj, curve_suffix)
                            else:
                                nameIsNew = False
                        else:
                            if obj.name.startswith(curve_suffix) == False:
                                newName = self.sufpreAdd(context, obj, curve_suffix)
                            else:
                                nameIsNew = False
                        if nameIsNew == True:
                            obj.name = newName
                            wm.renaming_messages.addMessage(oldName, obj.name, 'CURVE', 'OUTLINER_OB_CURVE')

                if data_suffix is not '':
                    if (
                                        obj.type == 'CURVE' or obj.type == 'LATTICE' or obj.type == 'MESH' or obj.type == 'META' or obj.type == 'SURFACE') and obj.data.name.endswith(
                            data_suffix) == False:
                        oldName = obj.name
                        nameIsNew = True
                        if wm.renaming_sufpre_type == 'SUF':
                            if obj.data.name.endswith(data_suffix) == False:
                                newName = self.suffixDataAdd(context, obj, data_suffix)
                            else:
                                nameIsNew = False
                        else:
                            if obj.data.name.startswith(data_suffix) == False:
                                newName = self.suffixDataAdd(context, obj, data_suffix)
                            else:
                                nameIsNew = False

                        if nameIsNew == True:
                            obj.data.name = newName
                            wm.renaming_messages.addMessage(oldName, obj.data.name, 'DATA', 'BLANK1')

        if mat_suffix is not '':
            for mat in bpy.data.materials:
                oldName = mat.name
                nameIsNew = True
                if wm.renaming_sufpre_type == 'SUF':
                    if mat.name.endswith(mat_suffix) == False:
                        newName = self.sufpreMatAdd(context, mat, mat_suffix)
                    else:
                        nameIsNew = False
                else:
                    if mat.name.startswith(mat_suffix) == False:
                        newName = self.sufpreMatAdd(context, mat, mat_suffix)
                    else:
                        nameIsNew = False

                if nameIsNew == True:
                    mat.name = newName
                    wm.renaming_messages.addMessage(oldName, mat.name, 'MATERIAL', 'MATERIAL')

        if group_suffix != '':
            for group in bpy.data.groups:
                nameIsNew = True
                oldName = group.name
                if wm.renaming_sufpre_type == 'SUF':
                    if group.name.endswith(group_suffix) == False:
                        newName = self.suffixGrpAdd(context, group, group_suffix)
                    else:
                        nameIsNew = False
                else:
                    if group.name.startswith(group_suffix) == False:
                        newName = self.suffixGrpAdd(context, group, group_suffix)
                    else:
                        nameIsNew = False
                if nameIsNew == True:
                    group.name = newName
                    wm.renaming_messages.addMessage(oldName, group.name, 'GROUP', 'OUTLINER_OB_GROUP_INSTANCE')

        if armature_suffix is not '' or bone_sufpre is not '':
            for armature in bpy.data.armatures:
                if armature_suffix is not '':
                    nameIsNew = True
                    oldName = armature.name
                    if wm.renaming_sufpre_type == 'SUF':
                        if armature.name.endswith(armature_suffix) == False:
                            newName = self.suffixArmAdd(context, armature, armature_suffix)
                        else:
                            nameIsNew = False
                    else:
                        if armature.name.startswith(armature_suffix) == False:
                            newName = self.suffixArmAdd(context, armature, armature_suffix)
                        else:
                            nameIsNew = False
                    if nameIsNew == True:
                        armature.name = newName
                        wm.renaming_messages.addMessage(oldName, armature.name, 'ARMATURE', 'OUTLINER_OB_ARMATURE')
                if bone_sufpre is not '':
                    for bone in armature.bones:
                        nameIsNew = True
                        oldName = bone.name
                        if wm.renaming_sufpre_type == 'SUF':
                            if bone.name.endswith(bone_sufpre) == False:
                                newName = self.suffixArmAdd(context, bone, bone_sufpre)
                            else:
                                nameIsNew = False
                        else:
                            if bone.name.startswith(bone_sufpre) == False:
                                newName = self.suffixArmAdd(context, bone, bone_sufpre)
                            else:
                                nameIsNew = False
                        if nameIsNew == True:
                            bone.name = newName
                            wm.renaming_messages.addMessage(oldName, bone.name, 'BONE', 'BONE_DATA')

        bpy.ops.renaming.popup('INVOKE_DEFAULT')

        return {'FINISHED'}

    def sufpreAdd(self, context, obj, sufpreName):
        wm = context.window_manager

        nName = obj.name
        if wm.renaming_sufpre_type == 'SUF':
            nName = nName + sufpreName
        else:
            nName = sufpreName + nName

        if nName not in bpy.data.objects:
            obj.name = nName
            return nName
        else:
            i = 1
            while (nName in bpy.data.objects):
                if wm.renaming_sufpre_type == 'SUF':
                    nName = obj.name + "_" + str(i) + sufpreName
                else:
                    nName = sufpreName + obj.name + "_" + str(i)
                i = i + 1

        obj.name = nName
        return nName

    def suffixDataAdd(self, context, obj, sufpreName):
        wm = context.window_manager

        nName = obj.data.name
        if wm.renaming_sufpre_type == 'SUF':
            nName = nName + sufpreName
        else:
            nName = sufpreName + nName

        if nName not in bpy.data.meshes and nName not in bpy.data.lattices and nName not in bpy.data.curves and nName not in bpy.data.metaballs:
            obj.data.name = nName
            return nName
        else:
            i = 1
            while (
                            nName in bpy.data.meshes or nName in bpy.data.lattices or nName in bpy.data.curves or nName in bpy.data.metaballs):
                nName = obj.data.name + "_" + str(i)
                i = i + 1
            return nName

    def sufpreMatAdd(self, context, mat, sufpreName):
        wm = context.window_manager
        nName = mat.name
        if wm.renaming_sufpre_type == 'SUF':
            nName = nName + sufpreName
        else:
            nName = sufpreName + nName

        if nName not in bpy.data.materials:
            mat.name = nName
            return nName
        else:
            i = 1
            while (nName in bpy.data.materials):
                nName = mat.name + "_" + str(i)
                i = i + 1
            return nName

    def suffixGrpAdd(self, context, grp, sufpreName):
        wm = context.window_manager

        nName = grp.name
        if wm.renaming_sufpre_type == 'SUF':
            nName = nName + sufpreName
        else:
            nName = sufpreName + nName

        if nName not in bpy.data.groups:
            grp.name = nName
            return nName
        else:
            i = 1
            while (nName in bpy.data.groups):
                nName = grp.name + "_" + str(i)
                i = i + 1
            return nName

    def suffixArmAdd(self, context, arm, sufpreName):
        wm = context.window_manager

        nName = arm.name
        if wm.renaming_sufpre_type == 'SUF':
            nName = nName + sufpreName
        else:
            nName = sufpreName + nName

        if nName not in bpy.data.armatures:
            arm.name = nName
            return nName
        else:
            i = 1
            while (nName in bpy.data.armatures):
                nName = arm.name + "_" + str(i)
                i = i + 1
            return nName


class SearchAndReplace(bpy.types.Operator):
    bl_idname = "renaming.search_replace"
    bl_label = "Search and Replace"
    bl_description = "replaces parts in the object names"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):
        wm = context.window_manager

        renamingList = []
        renamingList = getRenamingList(self, context)
        print("--------------------------------------------")
        print(renamingList)
        if len(renamingList) > 0:
            for entity in renamingList:
                if entity is not None:
                    if wm.renaming_search is not '':
                        if wm.rename_matchcase:
                            oldName = entity.name
                            newName = str(entity.name).replace(wm.renaming_search, wm.renaming_replace)
                            entity.name = newName
                            wm.renaming_messages.addMessage(oldName,entity.name )
                        else:
                            oldName = entity.name
                            replaceSearch = re.compile(re.escape(wm.renaming_search), re.IGNORECASE)
                            newName = replaceSearch.sub(wm.renaming_replace, entity.name)
                            entity.name = newName
                            print(oldName)
                            print(entity.name)
                            print(newName)

                            wm.renaming_messages.addMessage(oldName, entity.name)

        bpy.ops.renaming.popup('INVOKE_DEFAULT')
        return {'FINISHED'}


class ReplaceName(bpy.types.Operator):
    bl_idname = "renaming.name_replace"
    bl_label = "Replace Names"
    bl_description = "replaces the names of the objects"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):
        wm = context.window_manager
        replaceName = wm.renaming_newName
        renamingList = getRenamingList(self, context)

        if len(str(replaceName)) > 0:
            digits = 3

            if len(renamingList) > 0:

                for entity in renamingList:
                    if entity is not None:
                        i = 1
                        if wm.renaming_object_types == 'GROUP' or wm.renaming_object_types == 'IMAGE':
                            i = 0

                        oldName = entity.name
                        newName = ""

                        dataList = []
                        boneList = []

                        if wm.renaming_object_types == 'BONE':
                            for arm in bpy.data.armatures:
                                for bone in arm.bones:
                                    boneList.append(bone.name)

                        if wm.renaming_object_types == 'DATA':
                            for obj in bpy.data.objects:
                                if obj.data is not None:
                                    dataList.append(obj.data.name)

                        while True:
                            print("Entered While " + str(i))
                            newName = replaceName + wm.renaming_numerate_separator + ('{num:{fill}{width}}'.format(num=i, fill='0', width=digits))

                            if wm.renaming_object_types == 'OBJECT':
                                if newName in bpy.data.objects and newName != entity.name:
                                    i = i + 1
                                else:
                                    break
                            elif wm.renaming_object_types == 'MATERIAL':
                                if newName in bpy.data.materials and newName != entity.name:
                                    i = i + 1
                                else:
                                    break
                            elif wm.renaming_object_types == 'GROUP':
                                if newName in bpy.data.groups and newName != entity.name:
                                    i = i + 1
                                else:
                                    break
                            elif wm.renaming_object_types == 'IMAGE':
                                if newName in bpy.data.images and newName != entity.name:
                                    i = i + 1
                                else:
                                    break
                            elif wm.renaming_object_types == 'DATA':
                                if newName in dataList and newName != entity.name:
                                    i = i + 1
                                else:
                                    break
                            elif wm.renaming_object_types == 'BONE':
                                if newName in boneList and newName != entity.name:
                                    i = i + 1
                                else:
                                    break

                        newName = replaceName + wm.renaming_numerate_separator + ('{num:{fill}{width}}'.format(num=i, fill='0', width=digits))
                        entity.name = newName
                        wm.renaming_messages.addMessage(oldName, entity.name)
                        i = i + 1

        else:  # len(str(replaceName)) <= 0
            wm.renaming_messages.addMessage(None, None, "Insert a valid string to replace names")

        i = 0
        bpy.ops.renaming.popup('INVOKE_DEFAULT')
        return {'FINISHED'}


def trimString(string, size):
    list1 = string
    list2 = list1[:-size]
    return ''.join(list2)


class TrimString(bpy.types.Operator):
    bl_idname = "renaming.cut_string"
    bl_label = "Trim End of String"
    bl_description = "Deletes the in the trim size specified amount of characters at the end of object names"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):
        wm = context.window_manager
        renamingList = []
        renamingList = getRenamingList(self, context)

        if len(renamingList) > 0:
            for entity in renamingList:
                if entity is not None:
                    oldName = entity.name
                    newName = trimString(entity.name, wm.renaming_cut_size)
                    entity.name = newName
                    wm.renaming_messages.addMessage(oldName, entity.name)

        bpy.ops.renaming.popup('INVOKE_DEFAULT')
        return {'FINISHED'}


class Addsuffix(bpy.types.Operator):
    bl_idname = "renaming.add_suffix"
    bl_label = "Add suffix"
    bl_description = "Adds a suffix to object names"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):

        wm = context.window_manager
        suffix = wm.renaming_suffix

        renamingList = []
        renamingList = getRenamingList(self, context)

        if len(renamingList) > 0:
            for entity in renamingList:
                if entity is not None:
                    if entity.name.endswith(suffix) is not True:
                        oldName = entity.name
                        newName = entity.name + suffix
                        entity.name = newName
                        wm.renaming_messages.addMessage(oldName, entity.name)
        else:
            wm.renaming_messages.addMessage(None, None, "Insert Valide String")

        bpy.ops.renaming.popup('INVOKE_DEFAULT')
        return {'FINISHED'}


class AddPrefix(bpy.types.Operator):
    bl_idname = "renaming.add_prefix"
    bl_label = "Add Prefix"
    bl_description = "Adds a prefix to object names"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        wm = context.window_manager
        pre = wm.renaming_prefix

        renamingList = []
        renamingList = getRenamingList(self, context)

        if len(renamingList) > 0:
            for entity in renamingList:
                if entity is not None:
                    if entity.name.startswith(pre) is not True:
                        oldName = entity.name
                        newName = pre + entity.name
                        entity.name = newName
                        wm.renaming_messages.addMessage(oldName, entity.name)

        bpy.ops.renaming.popup('INVOKE_DEFAULT')
        return {'FINISHED'}


class RenamingNumerate(bpy.types.Operator):
    bl_idname = "renaming.numerate"
    bl_label = "Numerate"
    bl_description = "adds a growing number to the object names with the amount of digits specified in Number Lenght"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):
        wm = context.window_manager
        i = 1
        step = wm.renaming_base_numerate
        digits = wm.renaming_digits_numerate

        renamingList = []
        renamingList = getRenamingList(self, context)

        if len(renamingList) > 0:
            for entity in renamingList:
                if entity is not None:
                    oldName = entity.name
                    newName = entity.name + wm.renaming_numerate_separator + ('{num:{fill}{width}}'.format(num=i * step, fill='0', width=digits))
                    entity.name = newName
                    wm.renaming_messages.addMessage(oldName, entity.name)
                    i = i + 1

        bpy.ops.renaming.popup('INVOKE_DEFAULT')
        return {'FINISHED'}


def getRenamingList(self, context):
    wm = context.window_manager
    renamingList = []

    if wm.renaming_object_types == 'OBJECT':
        if wm.rename_only_selection == True:
            for obj in bpy.context.selected_objects:
                renamingList.append(obj)
        else:
            renamingList = list(bpy.data.objects)

    elif wm.renaming_object_types == 'DATA':
        if wm.rename_only_selection == True:
            for obj in bpy.context.selected_objects:
                if obj.data not in renamingList:
                    renamingList.append(obj.data)
        else:
            for obj in bpy.data.objects:
                if obj.data not in renamingList:
                    renamingList.append(obj.data)

    elif wm.renaming_object_types == 'MATERIAL':
        if wm.rename_only_selection == True:
            for obj in bpy.context.selected_objects:
                for mat in obj.material_slots:
                    if mat is not None and mat.name != '':
                        renamingList.append(bpy.data.materials[mat.name])
        else:
            renamingList = list(bpy.data.materials)

    elif wm.renaming_object_types == 'IMAGE':
        renamingList = list(bpy.data.images)

    elif wm.renaming_object_types == 'GROUP':
        renamingList = list(bpy.data.groups)

    elif wm.renaming_object_types == 'BONE':
        if wm.rename_only_selection == True:
            mode = bpy.context.mode
            bpy.ops.object.mode_set(mode='POSE')
            for pose_bone in bpy.context.selected_pose_bones:
                print(pose_bone)
                renamingList.append(pose_bone)
            bpy.ops.object.mode_set(mode=mode)
        else:
            for arm in bpy.data.armatures:
                for bone in arm.bones:
                    print(bone)
                    renamingList.append(bone)

    return renamingList


windowVariables = []


class RENAMING_POPUP(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "renaming.popup"
    bl_label = "Renaming Panel"
    # bl_options = {'REGISTER', 'UNDO'}
    context = None

    def invoke(self, context, event):
        width = 800 * bpy.context.user_preferences.system.pixel_size
        status = context.window_manager.invoke_props_dialog(self, width=width)
        self.context = context
        return status

    def draw(self, context):
        wm = bpy.context.window_manager
        layout = self.layout
        box = layout.box()

        if len(wm.renaming_messages.message) <= 0:
            box.label("No Objects Renamed", icon="INFO")
        else:

            i = 0
            for msg in wm.renaming_messages.message:
                if msg is not None:
                    if msg['warning'] == False:
                        if (msg['newName'] is not None and msg['oldName'] is not None) and msg['oldName'] != msg[
                            'newName']:

                            if i == 0:
                                row = box.row(align=True)
                                row.alignment = 'EXPAND'
                                row.label("OBJECT TYPE")
                                row.label("NEW NAME")
                                row.label("OLD NAME")
                                row.separator()

                            row = box.row(align=True)
                            row.alignment = 'EXPAND'

                            if msg['obType'] is not False and msg['obIcon'] is not False:
                                row.label(str(msg['obType']), icon=msg['obIcon'])
                            else:
                                row.label(str(wm.renaming_object_types))

                            row.label(str(msg['newName']), icon='FILE_TICK')
                            row.label(str(msg['oldName']))
                            # box.label("Successfully changed to " + str(msg['newName'])+ " (" + str(msg['oldName']) + ")", icon = "FILE_TICK")

                            i += 1
                            print("i = " + str(i))

                    else:
                        if msg['newName'] is not None and msg['oldName'] is not None:
                            box.label("Warning", icon="ERROR")
                            box.label("       " + "Name: " + str(msg['oldName']))
                            box.label("       " + msg['warning'])
                        else:
                            box.label("Warning", icon="ERROR")
                            box.label("       " + msg['warning'])
            if i == 0:
                print("Entered")
                box.label("No Objects Renamed", icon="INFO")
        wm.renaming_messages.clear()

    def execute(self, context):
        wm = context.window_manager
        return {'FINISHED'}


class UseObjectnameForData(bpy.types.Operator):
    bl_idname = "renaming.dataname_from_obj"
    bl_label = "Data Name from Object"
    bl_description = "Renames the object data according to the object name and adds the in the data textfield specified suffix."
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):
        wm = context.window_manager
        suffix_data = wm.renaming_sufpre_data_02

        if wm.rename_only_selection == True:
            for obj in bpy.context.selected_objects:

                objName = obj.name + suffix_data
                if suffix_data is not '':
                    if (
                                        obj.type == 'CURVE' or obj.type == 'LATTICE' or obj.type == 'MESH' or obj.type == 'META' or obj.type == 'SURFACE'):
                        oldName = obj.data.name
                        newName = objName
                        obj.data.name = newName
                        wm.renaming_messages.addMessage(oldName, obj.data.name)
        else:
            for obj in bpy.data.objects:
                objName = obj.name + suffix_data
                if suffix_data is not '':
                    if (
                                        obj.type == 'CURVE' or obj.type == 'LATTICE' or obj.type == 'MESH' or obj.type == 'META' or obj.type == 'SURFACE'):
                        oldName = obj.data.name
                        newName = objName
                        obj.data.name = newName
                        wm.renaming_messages.addMessage(oldName, obj.data.name)

        bpy.ops.renaming.popup('INVOKE_DEFAULT')
        return {'FINISHED'}
