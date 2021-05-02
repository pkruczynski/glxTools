#!/bin/bash

$HOME/Aplikacje/blender-2.92/blender -b -P pycharm-blender/python_api/pypredef_gen.py
rm -rf pycharm-blender/python_api/pypredef-tmp
mv pycharm-blender/python_api/pypredef/ 2.92
