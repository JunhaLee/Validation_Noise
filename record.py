import os
import warnings
import matplotlib.pyplot as plt
from tkinter import *
from PIL import Image
from random import *
warnings.filterwarnings(action='ignore')

path_dir_train = '/home/rpc/LJH/pose_data/test/Model-Pose_f/'
path_dir_img_train = '/home/rpc/LJH/pose_data/test/Model-Image/'
file_list_train = os.listdir(path_dir_train)
file_list_train.sort()
f = open("/home/rpc/noise_data.txt", 'a')
TRAIN_SIZE = len(file_list_train)
count = 0
index_arr = []

def make_file_list_train():
    train_img_list = [0 for i in range(TRAIN_SIZE)]
    new_train_img_list = [0 for i in range(TRAIN_SIZE)]
    for n in range(TRAIN_SIZE):
        str = file_list_train[n].split('.')[0]
        if(str[len(str)-1] == '0' and str[len(str)-2] == '0' and str[len(str)-3] == '0'):
            index_arr.append(n)

        train_img_list[n] = path_dir_img_train + str + ".jpg"  # 이미지파일 파일명 생성
        new_train_img_list[n] = '/home/rpc/now/' + str + ".png"  # 이미지파일 파일명 생성



    return train_img_list, new_train_img_list

train_img_list, new_train_img_list =make_file_list_train()

def make_image():
    global xn
    global image
    img = Image.open(train_img_list[index_arr[xn]])
    img = img.transpose(Image.ROTATE_270)
    plt.imshow(img)
    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    plt.savefig('/home/rpc/now'+f'{xn}'+'.png', dpi = 150)

def showimg():
    global xn
    global image
    #make_image()
    image = PhotoImage(file=new_train_img_list[index_arr[xn]])
    label_1 = Label(root, text=file_list_train[index_arr[xn]], font="NanumGothic 20")
    label_2 = Label(root, image=image)
    label_1.place(x=0, y=10)
    label_2.place(x=0, y=150)

def showimg_next():
    global xn
    global image
    global random_val
    random_val = randint(1,50)
    #xn = xn + random_val
    xn = xn + 1
    if xn > len(train_img_list)-1:
        xn = len(train_img_list)-1
    #make_image()
    image = PhotoImage(file=new_train_img_list[index_arr[xn]])
    label_1 = Label(root, text=file_list_train[index_arr[xn]], font="NanumGothic 20")
    label_2 = Label(root, image=image)
    label_1.place(x=0, y=10)
    label_2.place(x=0, y=150)

def showimg_prev():
    global xn
    global image
    global random_val
    #xn = xn - random_val
    xn = xn - 1
    if xn < 0:
        xn = 0
    #make_image()
    image = PhotoImage(file=new_train_img_list[index_arr[xn]])
    label_1 = Label(root, text=file_list_train[index_arr[xn]], font="NanumGothic 20")
    label_2 = Label(root, image=image)
    label_1.place(x=0, y=10)
    label_2.place(x=0, y=150)

def save():
    global xn
    global f
    global count
    f.write(file_list_train[index_arr[xn]]+'\n')
    img = Image.open(train_img_list[index_arr[xn]])
    img = img.transpose(Image.ROTATE_270)
    plt.imshow(img)
    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    plt.savefig('/home/rpc/noise_data/'+file_list_train[index_arr[xn]]+'.png')
    count += 1
    print(count, ': ', file_list_train[index_arr[xn]])


def key_input(value):
    global xn
    if value.keysym == 'Right':
        showimg_next()
    elif value.keysym == 'Left':
        showimg_prev()
    elif value.keysym == 'Up':
        print(xn)
    elif value.keysym == 'space':
        save()

print(len(index_arr))
xn=1307
random_val = 0
root=Tk()
root.title("Validation")
root.geometry("1024x1024")
root.bind('<Key>', key_input)
root.resizable(0,0)
make_image()
image=PhotoImage(file=new_train_img_list[index_arr[xn]])



btn = Button(root,text="next",command=showimg_next,width=7,height=1)
btn2 = Button(root,text="previous",command=showimg_prev,width=7,height=1)
label_1 = Label(root,text=file_list_train[index_arr[xn]],font="NanumGothic 20")
label_2 = Label(root, image=image)
label_1.place(x=0,y=10)
label_2.place(x=0,y=150)

btn.place(x=300,y=50)
btn2.place(x=150,y=50)
root.mainloop()
print("close at:" , xn)
f.close()
