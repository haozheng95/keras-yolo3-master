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
        "object": {
            "name": "neg",
            "pose": "Unspecified",
            "truncated": 0,
            "difficult": 0,
            "bndbox": {
                "xmin": 690,
                "ymin": 548,
                "xmax": 1395,
                "ymax": 653,
            }
        }
    }
}


def json_set(folder, filename, path, width, height, name, xmin, ymin, xmax, ymax):
    layout["annotation"]["folder"] = folder
    layout["annotation"]["filename"] = filename
    layout["annotation"]["path"] = path

    layout["annotation"]["size"]["width"] = width
    layout["annotation"]["size"]["height"] = height

    layout["annotation"]["object"]["name"] = name

    layout["annotation"]["object"]["bndbox"]["xmin"] = xmin
    layout["annotation"]["object"]["bndbox"]["ymin"] = ymin
    layout["annotation"]["object"]["bndbox"]["xmax"] = xmax
    layout["annotation"]["object"]["bndbox"]["ymax"] = ymax

    return layout


# json转xml函数
def jsontoxml(jsonstr):
    xmlstr = xmltodict.unparse(jsonstr)
    return xmlstr


test = [
    {
        "name": "193fdcc3b541bd4c0807102214.jpg",
        "defect_name": "\u65ad\u6c28\u7eb6",
        "bbox": [
            507.61,
            810.27,
            524.61,
            821.6
        ]
    }
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
    count = 0
    for row in p:
        kwargs = dict(
            folder="image",
            filename=row[0],
            path=os.path.join(JPEGImages_path, row[0]),
            width=2446,
            height=1000,
            name=row[1],
            xmin=row[2][0],
            ymin=row[2][1],
            xmax=row[2][2],
            ymax=row[2][3],
        )
        jsonstr = json_set(**kwargs)
        xmlstr = jsontoxml(jsonstr)
        save_xml(xmlstr, os.path.join(Annotations_path, row[0][:-3] + "xml"))
        count += 1
    print("xml file count = %d" % count)


if __name__ == "__main__":
    json_data = get_json_data()
    main(json_data)
    print("json data length = %d" % len(json_data))
