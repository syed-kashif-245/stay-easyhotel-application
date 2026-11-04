import sqlite3
def connectdb():
    conn=sqlite3.connect("StayEasy")
    cursor=conn.cursor()
    conn.execute("PRAGMA foreign_keys = ON")
    return conn,cursor

def create_booking():
    conn,cursor=connectdb()
    try:
        cursor.execute('''
    create table if not exists Bookings(
        guest_ph_no varchar(10) not null,
        room_no integer not null,
        check_in text not null,
        check_out text not null,
        room_type text not null,
        status text not null CHECK(status IN ('CONFIRMED','CHECKED_IN','CHECKED_OUT','CANCELLED')),
        no_of_guests Integer not null,
        PRIMARY KEY(room_no,check_in),
        FOREIGN KEY(guest_ph_no) REFERENCES Guest(ph_no),
        FOREIGN KEY(room_no) REFERENCES Rooms(no)
    )''')
        print("table created sucessfully")

    except Exception as e:
        print(e)
    finally:
        conn.close()

def create_Guest():
    conn,cursor=connectdb()
    try:
        cursor.execute('''
create table if not exists Guest(
    name varchar not null,
    ph_no varchar(10) primary key,
    email text not null
)''')
        print("table created sucessfully")

    except Exception as e:
        print(e)
    finally:
        conn.close()

def inserting_guest(guest):
    conn,cursor=connectdb()
    try:
        cursor.execute('''
insert into Guest(name,ph_no,email) values(?,?,?)
''',(guest.name,guest.phone_number,guest.email,))
        conn.commit()
        print("the guest is inserted sucessfully")
    except Exception as e:
        print(e)
    finally:
        conn.close()

def inserting_booking(book):
    conn,cursor=connectdb()
    try:
        cursor.execute('''
insert into Bookings(guest_ph_no,room_no,check_in,check_out,room_type,status,no_of_guests) values(?,?,?,?,?,?,?)
''',(book.guest.phone_number,book.room_no,book.check_in,book.check_out,book.room_type,book.status,book.no_of_guests,))
        conn.commit()
        print("the booking is done sucessfully")
    except Exception as e:
        print(e)
    finally:
        conn.close()

def create_rooms():
    conn,cursor=connectdb()
    try:
        cursor.execute('''
create table if not exists Rooms(
    no Integer primary key,
    type text not null,
    floor integer not null
)
''')
        print("the table is created sucessfully")
    except Exception as e:
        print(e)
    finally:
        conn.close()
def insert_in_rooms(room):
    conn,cursor=connectdb()
    try:
        cursor.execute('''
    insert into Rooms(no,type,floor) values(?,?,?)
''',(room.no,room.type,room.floor,))
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def get_rooms(room_no):
    conn,cursor=connectdb()
    try:
        cursor.execute('''
    select no from Rooms where no=?
''',(room_no,))
        return cursor.fetchone()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def get_guest(ph_no):
    conn,cursor=connectdb()
    try:
        cursor.execute('''
    select 1 from Guest where ph_no=?
''',(ph_no,))
        return cursor.fetchone() is not None
    except Exception as e:
        print(e)
        return False
    finally:
        conn.close()


def is_available_room(check_in_time,check_out_time,room_no):
    conn,cursor=connectdb()
    try:
        cursor.execute('''
select 1 from Bookings where check_in<? and check_out>? and room_no=? and status in('CONFIRMED', 'CHECKED_IN')
''',(check_out_time, check_in_time, room_no,))
        return cursor.fetchone() is None
   
    except Exception as e:
        print(e)
        raise
    finally:
        conn.close()


def get_all_rooms(room_type):
    conn,cursor=connectdb()
    try:
        cursor.execute(
            '''
select no from Rooms where type=? order by no
''',(room_type,))
        return cursor.fetchall()
    except Exception as e:
        print(e)
        return []
    finally:
        conn.close()


def get_bookings():
    conn,cursor=connectdb()
    try:
        cursor.execute('''
select * from Bookings
''')
        return cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def getbooking(room_no,phone_no):
    conn,cursor=connectdb()
    try:
        cursor.execute('''
select check_in,check_out,status,room_type from Bookings where room_no=? and guest_ph_no=?
''',(room_no,phone_no,))
        return cursor.fetchone()
    except Exception as e:
        print(e)
    finally:
        conn.close()


def Update_booking(status,room_no,phone_no):
    conn,cursor=connectdb()
    try:
        cursor.execute('''
update Bookings set status=? where room_no=? and guest_ph_no=?
''',(status,room_no,phone_no))
        conn.commit()
        print(f"the guest had {status} sucessfully!!")
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def get_booking_details():
    conn = sqlite3.connect("StayEasy")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute('''
select * from bookings
''')
        return cursor.fetchall()
    except Exception as e:
        print(e)
        return None
    finally:
        conn.close()