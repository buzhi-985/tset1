from tkinter import filedialog

import xlrd as xlrd
def xie():
    Filepath = filedialog.askopenfilename()
    print('Filepath:', Filepath)
    data = xlrd.open_workbook(Filepath)
    # data = xlrd.open_workbook(r'E:\Excel导出.xls')
    print(data.sheet_names())  # 输出所有页的名称
    table = data.sheets()[0]  # 获取第一页
    # table = data.sheet_by_index(0)  # 通过索引获得第一页
    # table = data.sheet_by_name('Over')  # 通过名称来获取指定页
    table = data.sheets()[0]  # 获取第一页
    nrows = table.nrows  # 为行数，整形
    ncolumns = table.ncols  # 为列数，整形

    # print(table.row_values(0,1))  # 输出第一行值 为一个列表(行，开始的列，结束的列)
    # 遍历输出所有行值

    # 判断导入的表并写入
    if bm == "Salesman":
        sql = 'insert into Salesman(name,position,gender,phone,age,user,psw) ' \
              'values(?,?,?,?,?,?,?)'
    elif bm == "Customers":
        sql = 'insert into Customers(name,cid,id_number,phone,age,gender,region,note) ' \
              'values(?,?,?,?,?,?,?,?)'
    elif bm == "Reservation":
        sql = 'insert into Reservation(id,room_number,check_in_time,days,early_day,last_day,name,gender,phone,room_price,room_status,status)' \
              'values(?,?,?,?,?,?,?,?,?,?,?,?)'
    elif bm == 'Rooms_info':
        sql = 'insert into Rooms_info(id,type,lou,room_number,bed_number,price,description,room_status,note)' \
              'values(?,?,?,?,?,?,?,?,?)'
    elif bm == 'Orders':
        sql = 'insert into Orders(id,cid,days,time,room_type,room_number,price,discount,disc_reason,prepaid,salesman,note,status)' \
              'values(?,?,?,?,?,?,?,?,?,?,?,?,?)'
    elif bm == 'Bill':
        sql = 'insert into Bill(id,cid,items,total_price,check_in_time,check_out_time,note,status)' \
              'values(?,?,?,?,?,?,?,?)'
    elif bm == 'Services':
        sql = 'insert into Services(id,items,money,note,type)' \
              'values(?,?,?,?,?)'
    for row in range(nrows):
        a = tuple(table.row_values(row, 1))
        conn.create(sql, a)