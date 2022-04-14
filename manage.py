import tkinter as tk
import tkinter.messagebox as msg
import pymssql
import os
import login

def check_book():
    db = pymssql.connect('LAPTOP-M7P04LP7','','','library',charset = 'utf8')
    cursor = db.cursor()
    a = input_book.get()
    sql = "SELECT * FROM books WHERE bname = '%s'" % (a)
    cursor.execute(sql)
    results = cursor.fetchone()
    if results:
        root3 = tk.Tk()
        root3.title('查询到的书')
        val = "您要查询的书号为：%s" % (results[0])
        print2 = tk.Label(root3, text=val)
        print2.grid(row=1, column=0, padx=10, pady=5)
        val = "您要查询的书名为：%s" % (results[1].encode('latin-1').decode('gbk'))
        print3 = tk.Label(root3, text=val)
        print3.grid(row=2, column=0, padx=10, pady=5)
        val = "您要查询的书的作者为：%s" % (results[2].encode('latin-1').decode('gbk'))
        print4 = tk.Label(root3, text=val)
        print4.grid(row=3, column=0, padx=10, pady=5)
        val = "您要查询的书的库存量为：%s" % (results[3])
        print5 = tk.Label(root3, text=val)
        print5.grid(row=4, column=0, padx=10, pady=5)
    else:
        msg._show(title='错误', message='没有查到您要查询的记录')
    db.close()

def book_print():
    db = pymssql.connect('LAPTOP-M7P04LP7','', '', "library",charset="utf8")  #https://blog.csdn.net/weixin_34010566/article/details/91918437?utm_medium=distribute.pc_relevant.none-task-blog-baidujs_utm_term-0&spm=1001.2101.3001.4242
    cursor = db.cursor()
    sql = "SELECT bname FROM books WHERE bnum=0"
    cursor.execute(sql)
    results = cursor.fetchall()
    print("库存不足的书名如下：")
    for i in results:
        a = i[0]
        print(a.encode('latin-1').decode('gbk'))
    db.close()

def delete_end():
    db = pymssql.connect('LAPTOP-M7P04LP7','','', "library",charset = 'utf8')
    cursor = db.cursor()
    name = input4.get()
    sql = "UPDATE books SET bnum=0 WHERE bname= '%s'"%(name)
    try:
        cursor.execute(sql)
        db.commit()
        msg._show(title='已执行', message='下架成功')
    except:
        db.rollback()
        msg._show(title='系统故障', message='下架失败')
    db.close()

def borrow_end():
    global root3
    root3 = tk.Tk()
    root3.title("借阅记录查询：")
    db = pymssql.connect('LAPTOP-M7P04LP7','','', "library",charset='utf8')
    cursor = db.cursor()
    name = input5.get()
    sql = "SELECT lid,bname,btime,rtime FROM borrow,reader,books WHERE borrow.bno=books.bno AND borrow.rno=reader.rno AND rname='%s'"%(name)
    cursor.execute(sql)
    results = cursor.fetchall()
    cur = 0
    #print(results)
    for i in results:
        tk.Label(root3,text="记录号为：%s 书名为：%s 借阅时间为：%s 还书时间为：%s"%(i[0],i[1].encode('latin-1').decode('gbk'),i[2],i[3]),justify=tk.LEFT,font=36).grid(row=cur,column=0)
        cur=cur+1
    db.close()

def book_delete():
    global root2
    root2 = tk.Tk()
    root2.title("下架图书")
    v1 = tk.StringVar()
    global input4
    labe1 = tk.Label(root2, text="请输入要下架的图书名：", font=36).grid(row=0, column=0)
    input4 = tk.Entry(root2, textvariable=v1)
    input4.grid(row=1, column=0)
    tk.Button(root2, text='确认', width=10, command=delete_end).grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
    tk.Button(root2, text='取消', width=10, command=exit_login3).grid(row=2, column=1, sticky=tk.E, padx=10, pady=5)

def donate_end():
    db = pymssql.connect('LAPTOP-M7P04LP7','','',"library",'utf8')
    cursor = db.cursor()
    name = input10.get()
    author = input11.get()
    num = input12.get()
    #tim = input13.get()
    sql = "SELECT bnum FROM books WHERE bname='%s'" % (name)
    cursor.execute(sql)
    results = cursor.fetchone()
    if results:
        sql = "UPDATE books SET bnum = bnum + %s WHERE bname='%s'" % (num, name)
        try:
            cursor.execute(sql)
            db.commit()
            msg._show(title="成功", message="新进图书更新成功")
        except:
            msg._show(title="系统故障", message="新进图书更新失败")
            db.rollback()
    else:
        sql = "select count(1) from books"
        cursor.execute(sql)
        results = cursor.fetchall()
        num = results[0][0]
        bno = ("0" * (4 - len(str(num))) + str(num+1))
        sql = "INSERT INTO books(bno,bname,bauthor,bnum) VALUES ('%s','%s','%s',%s)" % (bno,name,author,num)
        try:
            cursor.execute(sql)
            db.commit()
            msg._show(title="成功", message="新进图书更新成功")
        except:
            msg._show(title="错误", message="输入信息有误")
            db.rollback()
    db.close()

def borrow_select():
    global root2
    root2 = tk.Tk()
    root2.title("查询借阅记录")
    v1 = tk.StringVar()
    global input5
    labe1 = tk.Label(root2, text="请输入要查询的读者姓名：", font=36).grid(row=0, column=0)
    input5 = tk.Entry(root2, textvariable=v1)
    input5.grid(row=1, column=0)
    tk.Button(root2, text='确认', width=10, command=borrow_end).grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
    tk.Button(root2, text='取消', width=10, command=exit_login3).grid(row=2, column=1, sticky=tk.E, padx=10, pady=5)


def book_select():
    v1=tk.StringVar()
    global root2
    root2=tk.Tk()
    root2.title("查询图书")
    global input_book
    labe1 = tk.Label(root2, text="请输入您要查询的图书名：", font=36).grid(row=0, column=0)
    input_book = tk.Entry(root2,textvariable=v1)
    input_book.grid(row=0,column=1)
    tk.Button(root2, text='确认', width=10, command=check_book).grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
    tk.Button(root2, text='取消', width=10, command=exit_login3).grid(row=1, column=1, sticky=tk.E, padx=10, pady=5)

def book_in():
    global root2
    root2 = tk.Tk()
    root2.title("新进图书")
    v1 = tk.StringVar()
    v2 = tk.StringVar()
    v3 = tk.StringVar()
    v4 = tk.StringVar()
    global input10,input11,input12,input13
    labe10 = tk.Label(root2, text="请输入您要新进的图书名：", font=36).grid(row=0, column=0)
    labe12 = tk.Label(root2, text="请输入您要新进的作者", font=36).grid(row=1, column=0)
    labe13 = tk.Label(root2, text="请输入您要新进的图书的数量：", font=36).grid(row=2, column=0)###############
    input10 = tk.Entry(root2, textvariable=v1)
    input10.grid(row=0, column=1)
    input11 = tk.Entry(root2, textvariable=v2)
    input11.grid(row=1, column=1)
    input12 = tk.Entry(root2, textvariable=v3)
    input12.grid(row=2, column=1)
    #input13 = tk.Entry(root2, textvariable=v4)
    #input13.grid(row=3, column=1)
    tk.Button(root2, text='确认', width=10, command=donate_end).grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
    tk.Button(root2, text='取消', width=10, command=exit_login3).grid(row=4, column=1, sticky=tk.E, padx=10, pady=5)


def success_tip(id):
    global root1
    root.destroy()
    root2.destroy()
    root1 = tk.Tk()
    root1.title('兴梦图书管理系统')
    labe1 = tk.Label(root1, text="欢迎来到兴梦图书管理系统，请选择您要进行的操作：", font=36).grid(row=0, column=0)
    tk.Button(root1, text='打印缺书单', width=50,height=2, command=book_print).grid(row=1, column=0)
    tk.Button(root1, text='下架图书', width=50,height=2,  command=book_delete).grid(row=5, column=0)
    tk.Button(root1, text='查询借阅记录', width=50,height=2, command=borrow_select).grid(row=3, column=0)
    tk.Button(root1, text='新进图书', width=50,height=2,  command=book_in).grid(row=4, column=0)
    tk.Button(root1, text='查询图书信息', width=50,height=2, command=book_select).grid(row=2, column=0)
    tk.Button(root1, text='退出', width=50,height=2, command=exit_loginx).grid(row=6, column=0)

def exit_loginx():
    root1.destroy()
    frame()

def exit_login2():
    root1.destroy()

def login_check():
    db = pymssql.connect('LAPTOP-M7P04LP7','','','library','utf8')
    cursor = db.cursor()
    no =input_id.get()
    name=input2.get()
    sql = "SELECT mpassward FROM mpass WHERE mno ='%s'" % (no)
    cursor.execute(sql)
    results = cursor.fetchone()
    if results:
        if name == results[0]:
            success_tip(no)
        else:
            msg._show(title='错误！',message='账号密码输入错误！')
    else:
        msg._show(title='错误！',message='您输入的用户不存在！')
    db.close()

def auto_login():
    global root2
    root2 = tk.Tk()
    v1 = tk.StringVar()
    v2 = tk.StringVar()
    root2.title("登入")
    labe1=tk.Label(root2,text="职工号：",font=36).grid(row=0, column=0)
    label2=tk.Label(root2,text="密码：",font=36).grid(row=1,column=0)
    global input_id,input2
    input_id = tk.Entry(root2, textvariable=v1)
    input_id.grid(row=0, column=1, padx=10, pady=5)
    input2 = tk.Entry(root2, textvariable=v2, show='*')
    input2.grid(row=1, column=1, padx=10, pady=5)
    tk.Button(root2, text='登录', width=10, command=login_check).grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
    tk.Button(root2, text='退出', width=10, command=exit_login3).grid(row=3, column=1, sticky=tk.E, padx=10, pady=5)

def exit_login():
    root.destroy()
    login.frame()

def exit_login3():
    root2.destroy()


def frame():
    global root
    root = tk.Tk()
    root.title('兴梦图书管理系统登录')
    root.geometry("280x250")
    photo = tk.PhotoImage(file='C:/Users/Sakura/Pictures/Camera Roll/Sekiro 2020_4_2 11_31_23.png')
    theLabel = tk.Label(root, image=photo, compound=tk.CENTER, fg="white").grid(row=2, column=0)
    tk.Button(root, text='登入', width=10,height=2, command=auto_login).grid(row=0, column=0)
    tk.Button(root, text='退出',width=10,height=2,command=exit_login).grid(row=1, column=0)
    root.mainloop()