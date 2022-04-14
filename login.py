import tkinter as tk
import tkinter.messagebox as msg
import pymssql
import os
import user
import manage
#coding=utf-8

def exit1():
    root.destroy()
    user.frame()

def exit2():
    root.destroy()
    manage.frame()

def frame():
    global root
    root = tk.Tk()
    root.title('兴梦图书系统')
    photo=tk.PhotoImage(file='C:/Users/Sakura/Pictures/Saved Pictures/IMG_-3ji1xw(1).png')  #到时候记得把这个文件地址改掉
    root.geometry("700x200")
    theLabel = tk.Label(root,image = photo,compound = tk.CENTER,fg = "white").grid(row=0,column=0)
    labe1 = tk.Label(root, text="欢迎来到兴梦图书系统，请选择用户类型：", font=36).grid(row=0, column=1)
    tk.Button(root, text='普通用户',width=10,height=2,command=exit1).grid(row=1, column=5,)
    tk.Button(root, text='管理员',width=10,height=2,  command=exit2).grid(row=2, column=5)
    root.mainloop()


if __name__ == '__main__':
    frame()
