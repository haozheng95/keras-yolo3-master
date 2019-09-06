#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: yinhaozheng
@software: PyCharm
@file: json_2_xml.py
@time: 2019-09-05 17:28
"""
import json as js
import os

__mtime__ = '2019-09-05'

import xmltodict

VOCdevkit_path = os.path.dirname(os.path.abspath(__file__))
VOC2007_path = os.path.join(VOCdevkit_path, "VOC2007")
Annotations_path = os.path.join(VOC2007_path, "Annotations")
JPEGImages_path = os.path.join(VOC2007_path, "JPEGImages")
json_path = "anno_train.json"
layout = {
    "annotation": {
        "folder": "image",
        "filename": "4.jpg",
        "path": "image_path",
        "source": {
            "database": "Unknown"
        },
        "size": {
            "width": 1400,
            "height": 1200,
            "depth": 1,
        },
        "segmented": 0,
        "object": []
    }
}


#
# object_str = """
# 	<object>
# 		<name>%s</name>
# 		<pose>Unspecified</pose>
# 		<truncated>0</truncated>
# 		<difficult>0</difficult>
# 		<bndbox>
# 			<xmin>%d</xmin>
# 			<ymin>%d</ymin>
# 			<xmax>%d</xmax>
# 			<ymax>%d</ymax>
# 		</bndbox>
# 	</object>
# """

# name, xmin, ymin, xmax, ymax
def json_set(folder, filename, path, width, height, objects):
    layout["annotation"]["folder"] = folder
    layout["annotation"]["filename"] = filename
    layout["annotation"]["path"] = path

    layout["annotation"]["size"]["width"] = width
    layout["annotation"]["size"]["height"] = height
    objects_data = []

    for line in objects:
        bndbox = dict(
            xmin=line["xmin"],
            ymin=line["ymin"],
            xmax=line["xmax"],
            ymax=line["ymax"]
        )
        row = dict(
            name=line["name"],
            pose="Unspecified",
            truncated=0,
            difficult=0,
            bndbox=bndbox,
        )
        objects_data.append(row)

    layout["annotation"]["object"] = objects_data

    return layout


# json转xml函数
def jsontoxml(jsonstr):
    xmlstr = xmltodict.unparse(jsonstr)
    return xmlstr


test = [
    {
        "name": "9cc16f823cf576e50812117853.jpg",
        "defect_name": "\u4fee\u75d5",
        "bbox": [
            118.58,
            8.74,
            144.14,
            998.15
        ]
    },
    {
        "name": "9cc16f823cf576e50812117853.jpg",
        "defect_name": "\u4fee\u75d5",
        "bbox": [
            171.52,
            6.92,
            208.06,
            997.0
        ]
    },
]


def get_json_data(path=json_path):
    with open(path, encoding="utf-8") as f:
        json_data = js.load(f)
    return json_data


def parser(data):
    for row in data:
        yield row["name"], row["defect_name"], row["bbox"]


def save_xml(xml_str, file):
    with open(file, "w", encoding="utf-8") as f:
        f.write(xml_str)


def main(data):
    p = parser(data)
    group_data = dict()
    for row in p:
        object_data = [
            dict(name=row[1],
                 xmin=row[2][0],
                 ymin=row[2][1],
                 xmax=row[2][2],
                 ymax=row[2][3], )
        ]
        kwargs = dict(
            folder="image",
            filename=row[0],
            path=os.path.join(JPEGImages_path, row[0]),
            width=2446,
            height=1000,
            objects=object_data
        )

        if kwargs["filename"] in group_data:
            group_data[kwargs["filename"]]["objects"].append(kwargs["objects"][0])
        else:
            group_data[kwargs["filename"]] = kwargs

    count = 0
    for k in group_data:
        kwargs = group_data[k]
        jsonstr = json_set(**kwargs)
        xmlstr = jsontoxml(jsonstr)
        save_xml(xmlstr, os.path.join(Annotations_path, kwargs["filename"][:-3] + "xml"))
        count += 1
    print("xml file count = %d" % count)


if __name__ == "__main__":
    # s = jsontoxml(layout)
    # save_xml(s, os.path.join(Annotations_path, "t.xml"))
    json_data = get_json_data()
    main(json_data)
    print("json data length = %d" % len(json_data))
