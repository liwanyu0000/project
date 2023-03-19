# from utils.utils_detect import buildYolo
# from utils.utils_detect import cut_img
# import threading
# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 不显示等级2以下的提示信息
# import matplotlib.pyplot as plt
# # import cv2
# # import numpy as np
# from PIL import Image
# import time


# def one_row(image, row, yolo):
#     for i in range(len(image[row])):
#         yolo.detect_image(image[row][i])

# if __name__ == '__main__':
#     img_shape = [832, 608]
#     yolo = buildYolo('./model/best_epoch_weights.h5',
#                      img_shape, 0.5, 's', 0.3)
#     img = input('Input image filename:')
#     time_s = time.time()
#     # image = Image.open(img)
#     # print(yolo.detect_image(image))
#     image = cut_img(img, [832, 608])
#     ans = []
#     for i in range(len(image)):
#         for j in range(len(image[i])):
#             box, score, classes = yolo.detect_image(image[i][j])
#             for k in range(len(box)):
#                 ans.append([box[k][0] + img_shape[1] * i, 
#                             box[k][1] + img_shape[0] * j, 
#                             box[k][2] + img_shape[1] * i, 
#                             box[k][3] + img_shape[0] * j, 
#                             score[k], classes[k]])
#     print(ans)
#     time_e = time.time()
#     print('time cost:', time_e - time_s, 's')
                
        # threading.Thread(target=one_row, args=(image, i, yolo, )).start()
            # for j in range(len(image[0])):
            #     yolo.detect_image(image[i][j])
        # print(yolo.detect_image(image))
        # image.close()
# if __name__ == '__main__':
#     image = Image.open('street.jpg')
#     out_img = cut_img('1.jpg', [832, 608])
#     x = 1
#     for i in range(len(out_img)):
#         for j in range(len(out_img[i])):
#             plt.subplot(len(out_img), len(out_img[i]), x)
#             plt.imshow(out_img[i][j])
#             x += 1
#     plt.show()

from utils.utilsDetect import draw
# from networks.Yolonet import YOLO
import cv2
# import os
from utils.utilsXml import analyzeXml

if __name__ == '__main__':
    
    # img_path = './'
    # img_name = '197_3_t20201119085029189_CAM1.jpg'
    # img_shape = [832, 608]
    # model = YOLO(img_shape)
    # xml_path = './xmlpath/'
    # if not os.path.isdir(xml_path):
    #     os.mkdir(xml_path)
    # dic = {0:"edge_anomaly",
    #     1:"corner_anomaly",
    #     2:"white_point_blemishes",
    #     3:"light_block_blemishes",
    #     4:"dark_spot_blemishes",
    #     5:"aperture_blemishes"}
    # info = detect(img_path, img_name, img_shape, model, xml_path, dic)
    info = analyzeXml('xmlpath/197_3_t20201119085029189_CAM1_D20230318_T172913.xml')
    color_dict = {
        "edge_anomaly": (238, 238, 0),
        "corner_anomaly": (0, 255, 0),
        "white_point_blemishes": (0, 255, 255),
        "light_block_blemishes": (0, 0, 255),
        "dark_spot_blemishes": (226, 43, 138),
        "aperture_blemishes": (98, 28, 139)}
    img = draw(info, color_dict)
    cv2.imwrite('test_.jpg', img)