
bl_info = {
    'name'          : 'glxTools',
    'author'        : 'kruk@op.pl',
    'blender'       : (2, 80, 0),
    'category'      : 'Import-Export',
    'location'      : 'View3D > Sidebar [N] > glxTools',
    'description'   : '',
    'version'       : (0, 0, 1),
    'link'          : 'https://github.com/pkruczynski/glxTools'
}

import bpy
import os

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty)

from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup)


def ShowMessage(message=' ', title='Message Box', icon='INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    wm = bpy.context.window_manager
    wm.popup_menu(draw_func=draw, title=title, icon=icon)


# ------------------------------------------------------------------------------
# Scene Properties
# ------------------------------------------------------------------------------

class glxProperties(PropertyGroup):
    glx_bool: BoolProperty(
        name='Bool Value',
        description='A bool property',
        default=False
    )

    glx_int: IntProperty(
        name='Int Value',
        description='IntProperty',
        default=23,
        min=10,
        max=100
    )

    glx_float: FloatProperty(
        name='Float Value',
        description='FloatProperty',
        default=23.7,
        min=0.01,
        max=30.0
    )

    glx_vector: FloatVectorProperty(
        name='Float Vector Value',
        description='FloatVectorProperty',
        default=(0.0, 0.0, 0.0),
        min=0.0,
        max=0.1
    )

    glx_string: StringProperty(
        name='String Value',
        description='StringProperty',
        default='none',
        maxlen=1024
    )

    # noinspection PyUnresolvedReferences
    glx_path: StringProperty(
        name='Directory',
        description='Choose a directory:',
        default='~/Pulpit',
        maxlen=1024,
        subtype='DIR_PATH'
    )

    glx_enum: EnumProperty(
        name='Dropdown:',
        description='Apply Data to attribute.',
        items=[('OP1', 'Option 1', ''),
               ('OP2', 'Option 2', ''),
               ('OP3', 'Option 3', ''),
               ]
    )


# ------------------------------------------------------------------------------
# Operators
# ------------------------------------------------------------------------------

class WM_OT_glxOperator(Operator):
    bl_label = 'Print Values Operator'
    bl_idname = 'wm.glx_operator'

    def dirIterate(self, dir):
        print(dir)

    def execute(self, context):
        glx_tools = context.scene.glx_tools

        print('bool state:', glx_tools.glx_bool)
        print('int value:', glx_tools.glx_int)
        print('float value:', glx_tools.glx_float)
        print('vector value:', glx_tools.glx_vector)
        print('string value:', glx_tools.glx_string)
        print('path value:', glx_tools.glx_path)
        print('enum state:', glx_tools.glx_enum)

        ShowMessage('Values printed.')
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# Menus
# ------------------------------------------------------------------------------

class OBJECT_MT_glxMenu(bpy.types.Menu):
    bl_label = 'Select'
    bl_idname = 'OBJECT_MT_glx_menu'

    def draw(self, context):
        layout = self.layout

        layout.operator('object.select_all', text='Select/Deselect All').action = 'TOGGLE'
        layout.operator('object.select_all', text='Inverse').action = 'INVERT'
        layout.operator('object.select_random', text='Random')


# ------------------------------------------------------------------------------
# Panel in Object Mode
# ------------------------------------------------------------------------------

class OBJECT_PT_glxPanel(Panel):
    bl_label = 'glxPanel'
    bl_idname = 'OBJECT_PT_glxPanel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'glxTools'
    bl_context = 'objectmode'

    @classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        glx_tools = context.scene.glx_tools

        layout.prop(glx_tools, 'glx_bool')
        layout.prop(glx_tools, 'glx_enum', text='Select')
        layout.prop(glx_tools, 'glx_int')
        layout.prop(glx_tools, 'glx_float')
        layout.prop(glx_tools, 'glx_string', text='Type')
        layout.prop(glx_tools, 'glx_vector', text='')
        layout.prop(glx_tools, 'glx_path', text='Select')
        layout.operator('wm.glx_operator')
        layout.menu(OBJECT_MT_glxMenu.bl_idname, text='Presets', icon='SCENE')
        layout.separator()


# ------------------------------------------------------------------------------
# Registration
# ------------------------------------------------------------------------------

classes = (
    glxProperties,
    WM_OT_glxOperator,
    OBJECT_MT_glxMenu,
    OBJECT_PT_glxPanel
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.glx_tools = PointerProperty(type=glxProperties)
    #ShowMessage('glxTools registered.', title='register()', icon='INFO')
    print('INFO: glxTools registered.')

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.glx_tools
    ShowMessage('glxTools unregistered.', title='unregister()', icon='ERROR')
    print('INFO: glxTools unregistered.')

if __name__ == '__main__':
    register()
