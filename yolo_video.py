import sys
import argparse

import numpy
from pandas._libs import json

from yolo import YOLO, detect_video
from PIL import Image

import glob
import os

base_path = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(base_path, "image")
image_not_path = os.path.join(image_path, "not")
test_path = os.path.join(base_path, "test")


def detect_img(yolo):
    result_json = []
    not_cont = 0
    with open("result_11_25_2.txt", "w") as f:
        k = 0
        # for i in range(50803):
        for file in os.listdir(test_path):
            # path = 'F:/比赛事宜/裂纹识别/复赛数据/challengedataset-semifinal/test/test/{}.jpg'.format(i + 1)
            path = os.path.join(test_path, file)
            img = Image.open(path)
            print(path)
            img, boxes, scores, classes = yolo.detect_image(img)

            i = 0
            for j in classes:
                if j > 20 or j < 0:
                    print(".......j", j)
                    j = 0
                    return
                temp_result = dict(
                    name=file,
                    category=j,
                    bbox=["%.2f" % x for x in boxes[i]],
                    score=scores[i],
                )
                i += 1
                print(json.dumps(temp_result))
                result_json.append(temp_result)
            if i > 0:
                not_cont += 1

            # print(boxes)
            # print("类别为：", classes)
            # print(file)
            save_path = os.path.join(image_path, file)
            save_path_2 = os.path.join(image_not_path, file)
            if (len(boxes) > 0):
                if (len(boxes) == 1):
                    w = boxes[0][3] - boxes[0][1]
                    h = boxes[0][2] - boxes[0][0]
                    ratio = w / h
                    print(ratio)
                    if (boxes[0][0] < 200):  # 此步骤是为了抑制检测出的圆管
                        img.save(save_path)
                        f.write("{} {}\n".format(file, 0))
                        k = k + 1
                    # elif(w*h<10000):#此步骤是为了抑制检测出较小检测框
                    #     img.save('F:/image/test_result_11_25/{}.jpg'.format(i + 1))
                    #     f.write("{}.jpg {}\n".format(i + 1, 0))
                    #     k = k + 1

                    else:
                        img.save(save_path_2)
                        f.write("{} {}\n".format(file, 1))
                        k = k + 1
                else:
                    img.save(save_path_2)
                    f.write("{} {}\n".format(file, 1))
                    k = k + 1
            else:
                img.save(save_path)
                f.write("{} {}\n".format(file, 0))
                k = k + 1

        print(k)
    yolo.close_session()
    res = json.dumps(result_json)
    with open("result.json", "w") as f:
        f.write(res)
    print("save over")
    print(not_cont)


# 这个代码可以进行单张图像的显示
# def detect_img(yolo):
#     while True:
#         img = input('Input image filename:')
#         try:
#             image = Image.open(img)
#         except:
#             print('Open Error! Try again!')
#             continue
#         else:
#             r_image = yolo.detect_image(image)
#             r_image.show()
#     yolo.close_session()


FLAGS = None

if __name__ == '__main__':
    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        '--model', type=str,
        help='path to model weight file, default ' + YOLO.get_defaults("model_path")
    )

    parser.add_argument(
        '--anchors', type=str,
        help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
    )

    parser.add_argument(
        '--classes', type=str,
        help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
    )

    parser.add_argument(
        '--gpu_num', type=int,
        help='Number of GPU to use, default ' + str(YOLO.get_defaults("gpu_num"))
    )

    parser.add_argument(
        '--image', default=True, action="store_true",
        help='Image detection mode, will ignore all positional arguments'
    )
    '''
    Command line positional arguments -- for video detection mode
    '''
    parser.add_argument(
        "--input", nargs='?', type=str, required=False, default='1.mp4',
        help="Video input path"
    )

    parser.add_argument(
        "--output", nargs='?', type=str, required=False, default="11.mp4",
        help="[Optional] Video output path"
    )

    FLAGS = parser.parse_args()

    if FLAGS.image:
        """
        Image detection mode, disregard any remaining command line arguments
        """
        print("Image detection mode")
        if "input" in FLAGS:
            print(" Ignoring remaining command line arguments: " + FLAGS.input + "," + FLAGS.output)
        detect_img(YOLO(**vars(FLAGS)))
    elif "input" in FLAGS:
        detect_video(YOLO(**vars(FLAGS)), FLAGS.input, FLAGS.output)
    else:
        print("Must specify at least video_input_path.  See usage with --help.")
