from tkinter import *
import os
import json
import warnings
warnings.filterwarnings(action='ignore')

path_dir_train = '/home/rpc/new_pose/val/Model-Pose_f/'
path_dir_img_train = '/home/rpc/new_pose/val/Model-Image/'
path_dir_img_remake = '/home/rpc/new_pose/val/new_image/'
file_list_train = os.listdir(path_dir_train)
file_list_train.sort()

TRAIN_SIZE = len(file_list_train)
num_keypoints = 17
keypoints_train = [[[0 for j in range(3)] for i in range(num_keypoints)] for k in range(TRAIN_SIZE)]


def make_file_list_train():
    train_img_list = [0 for i in range(TRAIN_SIZE)]
    train_img_list_remake = [0 for i in range(TRAIN_SIZE)]
    for n in range(TRAIN_SIZE):
        with open(path_dir_train + '/' + file_list_train[n], "r") as st_json:
            load_data = json.load(st_json)

        landmarks = load_data.get('landmarks')
        cnt = 0

        for i in range(num_keypoints):
            for j in range(3):
                keypoints_train[n][i][j] = landmarks[cnt]
                cnt += 1

        str = file_list_train[n].split('.')[0]
        train_img_list[n] = path_dir_img_train + str + ".jpg"  # 이미지파일 파일명 생성
        train_img_list_remake[n] = path_dir_img_remake + str + ".png"  # 이미지파일 파일명 생성

    return train_img_list, train_img_list_remake

train_img_list, train_img_list_remake =make_file_list_train()


def showimg_next():
    global xn
    global image
    xn = xn + 1
    if xn > len(noise_pic)-1:
        xn = len(noise_pic)-1
    image = PhotoImage(file=noise_pic[xn])
    label_1 = Label(root, text=noise_pic_path[xn], font="NanumGothic 20")
    label_2 = Label(root, image=image)
    label_1.place(x=200, y=10)
    label_2.place(x=0, y=150)

def showimg_prev():
    global xn
    global image
    xn = xn - 1
    if xn < 0:
        xn = 0
    image = PhotoImage(file=noise_pic[xn])
    label_1 = Label(root, text=noise_pic_path[xn], font="NanumGothic 20")
    label_2 = Label(root, image=image)
    label_1.place(x=0, y=10)
    label_2.place(x=0, y=150)

def convert():
    global xn
    temp = noise_pic_keypoints[xn][1]
    noise_pic_keypoints[xn][1] = noise_pic_keypoints[xn][2]
    noise_pic_keypoints[xn][2] = temp
    temp = noise_pic_keypoints[xn][3]
    noise_pic_keypoints[xn][3] = noise_pic_keypoints[xn][4]
    noise_pic_keypoints[xn][4] = temp
    temp = noise_pic_keypoints[xn][5]
    noise_pic_keypoints[xn][5] = noise_pic_keypoints[xn][6]
    noise_pic_keypoints[xn][6] = temp
    temp = noise_pic_keypoints[xn][7]
    noise_pic_keypoints[xn][7] = noise_pic_keypoints[xn][8]
    noise_pic_keypoints[xn][8] = temp
    temp = noise_pic_keypoints[xn][9]
    noise_pic_keypoints[xn][9] = noise_pic_keypoints[xn][10]
    noise_pic_keypoints[xn][10] = temp
    temp = noise_pic_keypoints[xn][11]
    noise_pic_keypoints[xn][11] = noise_pic_keypoints[xn][12]
    noise_pic_keypoints[xn][12] = temp
    temp = noise_pic_keypoints[xn][13]
    noise_pic_keypoints[xn][13] = noise_pic_keypoints[xn][14]
    noise_pic_keypoints[xn][14] = temp
    temp = noise_pic_keypoints[xn][15]
    noise_pic_keypoints[xn][15] = noise_pic_keypoints[xn][16]
    noise_pic_keypoints[xn][16] = temp

    with open(path_dir_train + noise_pic_path[xn], 'r') as f:
        json_data = json.load(f)
        json_data['landmarks'] = sum(noise_pic_keypoints[xn], [])
    with open(path_dir_train + noise_pic_path[xn], 'w', encoding='utf-8') as make_file:
        json.dump(json_data, make_file, indent="\t")
    print("complete to convert " + noise_pic_path[xn])

def convert_1(val):
    global xn
    temp = noise_pic_keypoints[xn][val*2-1]
    noise_pic_keypoints[xn][val*2-1] = noise_pic_keypoints[xn][val*2]
    noise_pic_keypoints[xn][val*2] = temp
    with open(path_dir_train + noise_pic_path[xn], 'r') as f:
        json_data = json.load(f)
        json_data['landmarks'] = sum(noise_pic_keypoints[xn], [])
    with open(path_dir_train + noise_pic_path[xn], 'w', encoding='utf-8') as make_file:
        json.dump(json_data, make_file, indent="\t")
    print("complete to convert " + noise_pic_path[xn] + ' - '+ f'{val}')


def key_input(value):
    if value.keysym == 'Right':
        showimg_next()
    elif value.keysym == 'Left':
        showimg_prev()
    elif value.keysym == 'space':
        convert()
    elif value.keysym == '1':
        convert_1(1)
    elif value.keysym == '2':
        convert_1(2)
    elif value.keysym == '3':
        convert_1(3)
    elif value.keysym == '4':
        convert_1(4)
    elif value.keysym == '5':
        convert_1(5)
    elif value.keysym == '6':
        convert_1(6)
    elif value.keysym == '7':
        convert_1(7)
    elif value.keysym == '8':
        convert_1(8)


pose_class = [0,0,0] # 0: 정면 1: 측면 2: 후면
pose_front = []
pose_front_keypoints = []
pose_side = []
pose_side_keypoints = []
pose_back = []
pose_back_keypoints = []
pose_back_path = []
for k in range(TRAIN_SIZE):
    if (keypoints_train[k][5][2] == 1 or keypoints_train[k][5][2] == 2) and (keypoints_train[k][6][2] == 1 or keypoints_train[k][6][2] == 2) and (keypoints_train[k][0][2] == 1 or keypoints_train[k][0][2] == 2) and (keypoints_train[k][1][2] == 1 or keypoints_train[k][1][2] == 2)and (keypoints_train[k][2][2] == 1 or keypoints_train[k][2][2] == 2):
        pose_class[0] +=1
        pose_front.append(train_img_list_remake[k])
        pose_front_keypoints.append(keypoints_train[k]) # 두 어깨와, eyes, 코가 모두 보이면 정면
    elif  (keypoints_train[k][5][2] == 1 or keypoints_train[k][5][2] == 2) and  (keypoints_train[k][6][2] == 1 or keypoints_train[k][6][2] == 2):
        pose_class[2] +=1
        pose_back.append(train_img_list_remake[k])
        pose_back_keypoints.append(keypoints_train[k]) # 두 어깨만 모두 보이면 후면
        pose_back_path.append(file_list_train[k])
    else:
        pose_class[1] +=1
        pose_side.append(train_img_list_remake[k])
        pose_side_keypoints.append(keypoints_train[k]) # 나머지는 측면

print("front : "+ f'{len(pose_front)}')
print("side : "+ f'{len(pose_side)}')
print("back : "+ f'{len(pose_back)}')

noise_pic = []
noise_pic_keypoints = []
noise_pic_path = []
for k in range(len(pose_back)):
    if (pose_back_keypoints[k][5][0] >  pose_back_keypoints[k][6][0]) or (pose_back_keypoints[k][11][0] >  pose_back_keypoints[k][12][0]):
        noise_pic.append(pose_back[k])
        noise_pic_keypoints.append(pose_back_keypoints[k])
        noise_pic_path.append(pose_back_path[k])
print(len(noise_pic))



xn=0
root=Tk()
root.title("Validation")
root.geometry("1024x1024")
root.bind('<Key>', key_input)
root.resizable(0,0)
image=PhotoImage(file=noise_pic[xn])



btn = Button(root,text="next",command=showimg_next,width=7,height=1)
btn2 = Button(root,text="previous",command=showimg_prev,width=7,height=1)
label_1 = Label(root,text=noise_pic_path[xn],font="NanumGothic 20")
label_2 = Label(root, image=image)
label_1.place(x=0,y=10)
label_2.place(x=0,y=150)

btn.place(x=300,y=50)
btn2.place(x=150,y=50)
print(xn)
root.mainloop()

