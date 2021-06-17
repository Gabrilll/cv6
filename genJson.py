import json
import os

train_dir = "6-single-object-tracking/trainval/trainval"
gt = {}

for video in os.listdir(train_dir):
    gt[video] = {}
    cur = gt[video]
    cur["video_dir"] = video
    f = None
    img_names = []
    video_dir = os.path.join(train_dir, video)
    for file in os.listdir(video_dir):
        if file.endswith('.txt'):
            file_path = os.path.join(video_dir, file)
            f = open(file_path, 'r')
        elif file.endswith(".jpg"):
            img_names.append(video + "/" + file)

    cur["img_names"] = img_names
    cnt = 0
    if f is not None:
        lines = f.readlines()
        if len(lines) > 0:
            init = lines[0].strip().split(",")
            cur["init_rect"] = [float(x) for x in init]

        gt_rect = []
        for line in lines[:1]:
            gt_rect.append([float(x) for x in line.strip().split(",")])
            cnt += 1

        for i in range(len(gt_rect), len(img_names)):
            gt_rect.append([0, 0, 0, 0, 0, 0, 0, 0])

        cur["gt_rect"] = gt_rect
    cur["camera_motion"] = [0] * len(img_names)
    cur["illum_change"] = [0] * len(img_names)
    cur["motion_change"] = [0] * len(img_names)
    cur["size_change"] = [0] * len(img_names)
    cur["occlusion"] = [0] * len(img_names)

with open("train_no_gt.json", "w") as f:
    json.dump(gt, f)
