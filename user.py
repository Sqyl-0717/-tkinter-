import tkinter as tk
import tkinter.messagebox as msg
import pymssql
import os
import login

#BACK_PATH="resources"+os.sep+"background2.gif"

def check_book():
    db = pymssql.connect('LAPTOP-M7P04LP7','','', "library",charset = 'utf8')
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
        val = "您要查询的书的书名为：%s" % (results[1].encode('latin-1').decode('gbk'))
        print3 = tk.Label(root3, text=val)
        print3.grid(row=2, column=0, padx=10, pady=5)
        val = "您要查询的书的作者为：%s" % (results[2].encode('latin-1').decode('gbk'))
        print4 = tk.Label(root3, text=val)
        print4.grid(row=3, column=0, padx=10, pady=5)
        val = "您要查询的书剩余量为：%s" % (results[3])
        print5 = tk.Label(root3, text=val)
        print5.grid(row=4, column=0, padx=10, pady=5)
        #val = "您要查询的书的出版日期为：%s" % (results[4])
        #print6 = tk.Label(root3, text=val)
        #print6.grid(row=5, column=0, padx=10, pady=5)
    else:
        msg._show(title='错误', message='没有查到您要查询的记录')
    db.close()

def borrow_end():
    db = pymssql.connect('LAPTOP-M7P04LP7','','', "library",charset = 'utf8')
    cursor = db.cursor()
    name = input8.get()
    sql = "select count(1) from borrow"
    cursor.execute(sql)
    results = cursor.fetchall()
    num = results[0][0]
    lid = ("0" * (5 - len(str(num))) + str(num + 1))
    sql = "SELECT bno,bnum FROM books WHERE bname='%s'" % (name)
    cursor.execute(sql)
    results = cursor.fetchone()
    if results:
        if results[1] > 0:
            sql = "INSERT INTO borrow(lid,rno,bno,btime) VALUES(%s,%s,'%s',getdate())" % (lid,id, results[0])
            try:
                cursor.execute(sql)
                db.commit()
                msg._show(title="成功",message="借阅成功！")
            except:
                msg._show(title="系统故障",message="借阅失败！")
        else:
            msg._show(title="库存量不足",message="对不起，您要借阅的图书库存不足！")
    else:
        msg._show(title="失败",message="没有找到您要借的书！")
    db.close()

def return_end():
    db = pymssql.connect('LAPTOP-M7P04LP7','','', "library",charset = 'utf8')
    cursor = db.cursor()
    name = input9.get()
    sql = "SELECT bno FROM books WHERE bname = '%s'" % (name)
    cursor.execute(sql)
    results = cursor.fetchone()
    sql = "SELECT lid FROM borrow WHERE bno=%s AND rno=%s" % (results[0], id)
    cursor.execute(sql)
    result = cursor.fetchone()
    sql = "UPDATE borrow SET rtime = getdate()WHERE lid= %s"%(result[0])
    try:
        cursor.execute(sql)
        db.commit()
        msg._show(title='成功',message='还书成功')
    except:
        msg._show(title='系统故障',message='还书失败')
    db.close()

def donate_end():
    db = pymssql.connect('LAPTOP-M7P04LP7','','', "library",charset = 'utf8')
    cursor = db.cursor()
    name = input10.get()
    amount = input11.get()
    write = input12.get()
    #tim= input13.get()
    sql = "SELECT bnum FROM books WHERE bname='%s'" % (name)
    cursor.execute(sql)
    results = cursor.fetchone()
    if results:
        sql = "UPDATE books SET bnum += %s WHERE bname='%s'" % (amount, name)
        try:
            cursor.execute(sql)
            db.commit()
            msg._show(title="成功",message="捐书成功！谢谢您")
        except:
            msg._show(title="系统故障",message="捐书失败")
            db.rollback()
    else:
        sql = "select count(1) from books"
        cursor.execute(sql)
        results = cursor.fetchall()
        num = results[0][0]
        bno = ("0" * (4 - len(str(num))) + str(num + 1))
        sql = "INSERT INTO books(bno,bauthor,bnum,bname) VALUES ('%s','%s',%s,'%s')" % (bno,write, amount, name)
        try:
            cursor.execute(sql)
            db.commit()
            msg._show(title="成功", message="捐书成功！谢谢您")
        except:
            msg._show(title="错误", message="输入信息有误")
            db.rollback()
    db.close()

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

def book_borrow():
    db = pymssql.connect('LAPTOP-M7P04LP7','','', "library",charset = 'utf8')
    cursor = db.cursor()
    sql = "SELECT rbleft FROM reader WHERE rno = %s" % (id)
    cursor.execute(sql)
    result = cursor.fetchone()
    v_borrow=tk.StringVar()
    if result[0] == 0:
        msg._show(title="错误",message="你已达最大借阅量，借阅失败")
    global root2
    root2 = tk.Tk()
    root2 .title("借阅")
    global input8
    labe1 = tk.Label(root2, text="请输入您要借阅的图书名：", font=36).grid(row=0, column=0)
    input8 = tk.Entry(root2, textvariable=v_borrow)
    input8.grid(row=1,column=0)
    tk.Button(root2, text='确认', width=10, command=borrow_end).grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
    tk.Button(root2, text='取消', width=10, command=exit_login3).grid(row=2, column=1, sticky=tk.E, padx=10, pady=5)
    db.close()

def return_book():
    global root2
    root2 = tk.Tk()
    root2.title("还书")
    v1=tk.StringVar()
    global input9
    labe1 = tk.Label(root2, text="请输入您要还的图书名：", font=36).grid(row=0, column=0)
    input9 = tk.Entry(root2, textvariable=v1)
    input9.grid(row=1, column=0)
    tk.Button(root2, text='确认', width=10, command=return_end).grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
    tk.Button(root2, text='取消', width=10, command=exit_login3).grid(row=2, column=1, sticky=tk.E, padx=10, pady=5)

def donate_book():
    global root2
    root2 = tk.Tk()
    root2.title("捐书")
    v1 = tk.StringVar()
    v2 = tk.StringVar()
    v3 = tk.StringVar()
    v4 = tk.StringVar()
    global input10,input11,input12,input13
    labe1 = tk.Label(root2, text="请输入您要捐赠的图书名：", font=36).grid(row=0, column=0)
    labe12 = tk.Label(root2, text="请输入您要捐赠的图书的数量：", font=36).grid(row=2, column=0)
    labe13 = tk.Label(root2, text="请输入您要捐赠的作者：", font=36).grid(row=1, column=0)
    #labe4 = tk.Label(root2, text="请输入您要捐赠的图书的出版时间：", font=36).grid(row=3, column=0)
    input10 = tk.Entry(root2, textvariable=v1)
    input10.grid(row=0, column=1)
    input11 = tk.Entry(root2, textvariable=v2)
    input11.grid(row=2, column=1)
    input12 = tk.Entry(root2, textvariable=v3)
    input12.grid(row=1, column=1)
    #input13 = tk.Entry(root2, textvariable=v4)
    #input13.grid(row=3, column=1)
    tk.Button(root2, text='确认', width=10, command=donate_end).grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
    tk.Button(root2, text='取消', width=10, command=exit_login3).grid(row=4, column=1, sticky=tk.E, padx=10, pady=5)

def message_reader():
    global root2
    db = pymssql.connect('LAPTOP-M7P04LP7', '', '', 'library', charset='utf8')
    cursor = db.cursor()
    a = id
    sql = "SELECT * FROM reader WHERE rno = '%s'" % (a)
    cursor.execute(sql)
    results = cursor.fetchone()
    root2 = tk.Tk()
    root2.geometry("320x200")
    root2.title('查询到账户信息')
    val = "学号为：%s" % (results[0])
    print2 = tk.Label(root2, text=val)
    print2.grid(row=1, column=0, padx=10, pady=5)
    val = "姓名为：%s" % (results[1].encode('latin-1').decode('gbk'))
    print3 = tk.Label(root2, text=val)
    print3.grid(row=2, column=0, padx=10, pady=5)
    val = "性别为：%s" % (results[2].encode('latin-1').decode('gbk'))
    print4 = tk.Label(root2, text=val)
    print4.grid(row=3, column=0, padx=10, pady=5)
    val = "班级为：%s" % (results[3].encode('latin-1').decode('gbk'))
    print5 = tk.Label(root2, text=val)
    print5.grid(row=4, column=0, padx=10, pady=5)
    db.close()

def success_tip():
    root.destroy()
    root1.destroy()
    global rootx
    rootx = tk.Tk()
    rootx.title('兴梦图书用户系统')
    labe1 = tk.Label(rootx,text="欢迎来到兴梦图书管理系统，请选择您要进行的操作：", font=36).grid(row=0, column=0)
    tk.Button(rootx, text='查询图书',  width=50,height=2, command=book_select).grid(row=1, column=0)
    tk.Button(rootx, text='借阅图书',  width=50,height=2, command=book_borrow).grid(row=2, column=0)
    tk.Button(rootx, text='归还图书',  width=50,height=2, command=return_book).grid(row=3,  column=0)
    tk.Button(rootx, text='捐赠图书',  width=50,height=2, command=donate_book).grid(row=4, column=0)
    tk.Button(rootx, text='查看账户信息', width=50, height=2, command=message_reader).grid(row=5, column=0)
    tk.Button(rootx, text='退出', width=50,height=2,command=exit_loginx).grid(row=6,column=0)
    rootx.mainloop()

def exit_login2():
    root1.destroy()

def exit_loginx():
    rootx.destroy()
    frame()

def login_check():
    db = pymssql.connect('LAPTOP-M7P04LP7','','', "library",charset = 'utf8')
    cursor = db.cursor()
    passward=input2.get()
    global id
    id = input_id.get()
    sql = "SELECT rpassward FROM rpass WHERE rno = '%s'" % (id)
    cursor.execute(sql)
    results = cursor.fetchone()
    if results:
            if passward == results[0]:
                success_tip()
            else:
               msg._show(title='错误！',message='账号密码输入错误！')
    else:
        msg._show(title='错误！',message='您输入的用户不存在！')
    db.close()

def auto_login():
    global root1
    root1 = tk.Tk()
    v1 = tk.StringVar()
    v2 = tk.StringVar()
    root1.title("登入")
    labe1=tk.Label(root1,text="学号：",font=36).grid(row=0, column=0)
    label2=tk.Label(root1,text="密码：",font=36).grid(row=1,column=0)
    global input_id,input2
    input_id = tk.Entry(root1, textvariable=v1)
    input_id.grid(row=0, column=1, padx=10, pady=5)
    input2 = tk.Entry(root1, textvariable=v2, show='*')
    input2.grid(row=1, column=1, padx=10, pady=5)
    tk.Button(root1, text='登录', width=10, command=login_check).grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
    tk.Button(root1, text='退出', width=10, command=exit_login2).grid(row=3, column=1, sticky=tk.E, padx=10, pady=5)

def exit_login():
    root.destroy()
    login.frame()

def exit_login3():
    root2.destroy()

def resiger_end():
    db = pymssql.connect('LAPTOP-M7P04LP7','','', "library",charset = 'utf8')
    cursor = db.cursor()
    rid = input1.get()
    name = input2.get()
    passward = input3.get()
    sex = input4.get()
    clas = input5.get()
    sql = "INSERT INTO reader VALUES(%s,'%s','%s','%s',10)" % (rid, name, sex, clas)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        msg._show(title='错误', message='注册失败！')
    sql = "INSERT INTO rpass VALUES(%s,'%s')" % (rid, passward)
    try:
        cursor.execute(sql)
        db.commit()
        msg._show(title='成功', message='注册成功！')
    except:
        msg._show(title='错误', message='注册失败！')
        db.rollback()
    db.close()

def resiger():
    global  root2
    root2 = tk.Tk()
    root2.title("注册")
    labe1  = tk.Label(root2, text="学号：", font=36).grid(row=0,column=0)
    label2 = tk.Label(root2, text="姓名：", font=36).grid(row=1,column=0)
    label3 = tk.Label(root2, text="密码(6位）：", font=36).grid(row=2,column=0)
    label4 = tk.Label(root2,text="性别：",font=36).grid(row=3,column=0)
    label5 = tk.Label(root2,text="班级：",font=36).grid(row=4,column=0)
    v1 = tk.StringVar()
    v2 = tk.StringVar()
    v3 = tk.StringVar()
    v4 = tk.StringVar()
    v5 = tk.StringVar()
    global input1,input2,input3,input4,input5
    input1 = tk.Entry(root2, textvariable=v1)
    input1.grid(row=0, column=1, padx=10, pady=5)
    input2 = tk.Entry(root2, textvariable=v2)
    input2.grid(row=1, column=1, padx=10, pady=5)
    input3 = tk.Entry(root2, textvariable=v3, show='*')
    input3.grid(row=2, column=1, padx=10, pady=5)
    input4 = tk.Entry(root2, textvariable=v4)
    input4.grid(row=3, column=1, padx=10, pady=5)
    input5 = tk.Entry(root2, textvariable=v5,)
    input5.grid(row=4, column=1, padx=10, pady=5)
    tk.Button(root2, text='确认', width=10, command=resiger_end).grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
    tk.Button(root2, text='取消', width=10, command=exit_login3).grid(row=5, column=1, sticky=tk.E, padx=10, pady=5)

def frame():
    global root
    root = tk.Tk()
    root.title('兴梦图书用户系统登录')
    root.geometry("280x310")
    photo=tk.PhotoImage(file= "C:/Users/Sakura/Pictures/Saved Pictures/2333010a-6196-425a-af51-050c78407555_thumb.png")
    theLabel = tk.Label(root,image = photo,compound = tk.CENTER,fg = "white").grid(row=0,column=0)
    tk.Button(root, text='登入', width=10,height=2, command=auto_login).grid(row=1, column=0,)
    tk.Button(root, text='注册', width=10,height=2, command=resiger).grid(row=2, column=0)
    tk.Button(root, text='退出',width=10,height=2,command=exit_login).grid(row=3, column=0)
    root.mainloop()