#!/usr/bin/env bash

cur_dir=$(pwd)
ui_dir="$cur_dir/Views/UI/"
py_dir="$cur_dir/Views/Widgets/"

for entry in $(ls ${ui_dir})
do
    echo "$entry"
    filename=${entry%.*}
    $(pyuic5 ${ui_dir}${entry} -o ${py_dir}${filename}.py)
done