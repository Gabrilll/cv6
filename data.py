import os
import numpy as np
import copy

res_path = "predict_csrt_3"
to_path = "predict_csrt_final"

total=0

for f in os.listdir(res_path):
    # print(video_path)
    if not f.endswith(".txt"):
        continue
    to_name = f
    f_path = os.path.join(res_path, f)

    pred = []
    left = None
    right = None
    flag = False

    with open(f_path, 'r') as from_file:
        print(f_path)

        lines = from_file.readlines()
        cnt = 0
        #             print(lines)
        pred.append([float(x) for x in lines[0].strip().split(",")])
        for l in lines[1:]:
            cnt += 1
            pos = [float(x) for x in l.strip().split(",")]
            pos = np.array(pos)
            if (pos == 0).all():
                if flag and cnt == len(lines) - 1:
                    right = cnt
                    flag = False
                    dis = []
                    interval = right - left
                    first = []

                    for i in range(8):
                        dis.append((pos[i] - pred[left][i]) / interval)
                        first.append(pred[left][i] + dis[i])
                    pred.append(first)
                    cur = copy.deepcopy(first)
                    for i in range(left + 2, right):
                        for j in range(8):
                            cur[j] = cur[j] + dis[j]
                        # print(cur)
                        pred.append(copy.deepcopy(cur))
                    pred.append(pos)

                elif not flag:
                    left = cnt - 1
                    flag = True
            else:
                if flag:
                    right = cnt
                    flag = False
                    dis = []
                    interval = right - left
                    first = []

                    for i in range(8):
                        dis.append((pos[i] - pred[left][i]) / interval)
                        first.append(pred[left][i] + dis[i])
                    pred.append(first)
                    cur = copy.deepcopy(first)
                    for i in range(left + 2, right):
                        for j in range(8):
                            cur[j] = cur[j] + dis[j]
                        pred.append(copy.deepcopy(cur))
                pred.append(pos)

    to_file = os.path.join(to_path, to_name)
    total+=1
    with open(to_file, 'w') as tf:
        for p in pred:
            tf.write(",".join([str(x) for x in p]) + "\n")

    print(total)