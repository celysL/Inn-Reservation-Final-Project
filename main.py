
import pymysql
import decimal
from pymysql import converters, FIELD_TYPE
import fileinput
import os
 

def initDB():
    conv = converters.conversions
    conv[FIELD_TYPE.NEWDECIMAL] = float  # convert decimals to float
    config = {
            'host':'127.0.0.1',
            'port':3306,
            'user':'root',
            'password':'123456',
            'database':'inn_reservation',
            'charset':'utf8mb4',
            'conv':conv,
            }
    conn=pymysql.connect(**config)
    return conn

####### DB operator  #########
def GetCustomer(conn,number):
    cur=conn.cursor()
    cur.execute(' select * from inn_customer where `phone_number`="%s"; ' % number)
    cur.close()
    conn.commit()
    return cur.fetchone()

def AddCustomer(conn,first_name,last_name,email,number):
    cur=conn.cursor()
    cur.execute('insert inn_customer (`first_name`,`last_name`,`email`,`phone_number`) values("%s","%s","%s","%s") ;' % (first_name,last_name,email,number))
    cur.close()
    conn.commit()

def GetReservation(conn,number):
    cur=conn.cursor()
    cur.execute(' select `first_name` ,`last_name` , `accommodation_days`,inn_rooms.`room_type`,`cost` ,inn_rooms.`id`,\
    inn_reservation.`id`,inn_customer.`phone_number` from inn_rooms ,inn_reservation,inn_customer \
    where inn_rooms.`id`=inn_reservation.`room_type` and inn_customer.`id`= inn_reservation.`customer_id` and inn_customer.`phone_number`="%s" and `checkout`=0; ' % number) 
    cur.close()
    conn.commit()
    return cur.fetchone()

def AddReservation(conn,customerid,roomid,days,price):
    cur=conn.cursor()
    cur.execute(' insert inn_reservation (`room_type`,`customer_id`,`accommodation_days`,`cost`,`checkout`) values(%d,%d,%d,%f,0) ;' % (int(roomid),int(customerid),int(days),float(price)))
    cur.close()
    conn.commit()

def UpdateReservation(conn,id):
    cur=conn.cursor()
    cur.execute('update inn_reservation set `checkout`=1 where `id`=%d; ' % id)
    cur.close()
    conn.commit()

def IncRoom(conn,id):
    cur=conn.cursor()
    cur.execute('update inn_rooms set `availability`=`availability`+1 where `id`=%d; ' % id)
    cur.close()
    conn.commit()

def DecRoom(conn,id):
    cur=conn.cursor()
    cur.execute('update inn_rooms set `availability`=`availability`-1 where `id`=%d; ' % id)
    cur.close()
    conn.commit()
def GetRoom(conn,roomtype):
    cur=conn.cursor()
    if roomtype==None:
        cur.execute(' select * from inn_rooms where  `availability`>0;')
    else:
        cur.execute(' select * from inn_rooms where `room_type`="%s" and `availability`>0;' % roomtype)
    
    cur.close()
    conn.commit()
    return cur.fetchone()


### read reserevation_file.txt #######
def initData(conn,dir):
    cur=conn.cursor()
    for line in fileinput.input(dir):
        line=line.replace('\n', '')
        data=line.split(',')
        print(data)
        rooms = GetRoom(conn,data[4])
        
        #print(rooms)
        if rooms != None:

            customer = GetCustomer(conn,data[3])
            if customer == None:

                AddCustomer(conn,data[0],data[1],data[2],data[3])
                customer = GetCustomer(conn,data[3])
            if GetReservation(conn,data[3])==None:
                DecRoom(conn,rooms[0])
                AddReservation(conn,customer[0],rooms[0],int(data[5]),rooms[2])
                print("inn add success:"+line)
            else:
                print("inn add fail:"+line)
        else:
            print("inn add fail:"+line)

### Checkout
def Checkout(conn):

    print("\n\n************** Check-out process ************\n")
    number = input('\t\tplease input your phone number:')

    res=GetReservation(conn,number)
    if res is None:
        print("number of inn no exist\n\n")
    else:
        print(res)
        print("Name : %s %s\n" % (res[0],res[1]))
        print("Accomdation: %d  days\n" % res[2])
        print("Room Type : %s\n" % res[3])
        cost=(res[4]*res[2])
        print("Total Cost : %.2f\n" % cost)

        roomid=res[5]
        innid=res[6]
       
        UpdateReservation(conn,innid)
        IncRoom(conn,roomid)
        print("Checkout finish !\n\n")


####  Checkin
def Checkin(conn):
    print("************** Check-in process ************\n")

    rooms=GetRoom(conn,None)
    if rooms==None:
        print("no room can checkin!\n\n")
        return

    standard_rooms=GetRoom(conn,'S')
    if standard_rooms!=None:
        print('- Standard_rooms(S)')

    premium_rooms=GetRoom(conn,'P')
    if premium_rooms!=None:
        print('- Premium_rooms(P)')

    ocean_view_rooms=GetRoom(conn,'O')
    if ocean_view_rooms!=None:
        print('- Ocean_view_rooms(O)')

    number = input('\t\tplease input your phone number:')
    if GetReservation(conn,number)!=None:
        print("You have an order that has not been checked out")
        return
    customer=GetCustomer(conn,number)
    if customer==None:
        print("customer info fault! please input customer info")
        first_name = input('\t\tFirst Name:')
        last_name = input('\t\tLast Name:')
        email = input('\t\tEmail:')
        AddCustomer(conn,first_name,last_name,email,number)
    customer=GetCustomer(conn,number)   
    customer_id=customer[0]


    room_type = input('\t\tplease input room type:')
    room_id=-1
    room_price=-1

    if room_type=='S' and standard_rooms!=None:
        room_id=int(standard_rooms[0])
        room_price=float(standard_rooms[2])

    elif room_type=='P' and premium_rooms!=None:
        room_id=int(premium_rooms[0])
        room_price=float(premium_rooms[2])

    elif room_type=='O' and ocean_view_rooms!=None:
        room_id=int(ocean_view_rooms[0])
        room_price=float(ocean_view_rooms[2])

    else:
        print("room type no exist!\n\n")
        return
    days = input('\t\tplease input days:')
   
    DecRoom(conn,room_id)
    AddReservation(conn,customer_id,room_id,days,room_price)  
    print("Checkin Finish!\n\n")

#### Menu      
def Menu():

    print("*************** welcome to  LIRS system *****************\n")
    print("please input one option\n")
    print("____________________________________\n")
    print("\t\tCheck-out:1\n")
    print("\t\tCheck-in:2\n")
    return input('\t\tyour option:')
    

## main
conn=initDB()
path="reservation_file.txt"
if os.path.exists(path):
    initData(conn,path)
    os.remove(path)
else:
    print(path+" no exist")
while True:
    opt=Menu()
    if opt=='1':
        Checkout(conn)
    elif opt=='2': 
        Checkin(conn)
    else:
        print("option error\n")
conn.close()