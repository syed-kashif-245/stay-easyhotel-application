from model import Bookings,StandardRoom,DeluxeRoom,SuiteRoom,Guest,Room
from db import get_booking_details,Update_booking,getbooking,create_booking,create_Guest,create_rooms,insert_in_rooms,inserting_booking,inserting_guest,get_bookings,get_rooms,get_guest,get_all_rooms,is_available_room
import re,csv
from datetime import date,datetime,timedelta
class Invalid(Exception):
    pass
class Invalid_booking(Exception):
    pass
class Invalid_guest_name(Exception):
    pass
class duplicate_Room_number(Exception):
    pass
class Invalid_Room(Exception):
    pass
class Unknown_room(Exception):
    pass
class Invalid_phone_number(Exception):
    pass
class Invalid_Gmail(Exception):
    pass
class Invalid_Date(Exception):
    pass

def generate_payroll(check_in_date,check_out_date,room_type):
    delta=check_out_date-check_out_date
    print(delta.days)


def createBooking():
    
    while(True):
        try:
            guest_name=input("enter the name of the Guest : ").strip()
            if(guest_name ==""):
                raise Invalid_guest_name("the name of the Guest cannot be empty")
            phone_number=input("Enter the phone number of the Guest : ").strip()
            if not re.fullmatch(r'[6-9]\d{9}', phone_number):
                raise Invalid_phone_number("Enter a valid 10-digit mobile number")
            
            email_id=input("enter the email adress of the guest : ").strip()
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

            if not re.fullmatch(email_pattern, email_id):
                raise Invalid_Gmail("Enter a valid email address")
            no_of_guest=int(input("enter the no of guests : ").strip())
            if no_of_guest<=0:
                raise Invalid("the guests cannot be lesser than 0")
            guest=Guest(guest_name,phone_number,email_id)

            room_type=input("enter the type of room user wanted : ").strip()
            if(room_type==""):
                raise Invalid_Room("the room type cannot be empty")

            if(room_type not in ("Standard","Deluxe","Suite")):
                raise Invalid_Room("the room_type is not correct it should be Standard,Deluxe,Suite")
            check_in,check_out=check_in_check_out()
            status="CONFIRMED"
            booking=Bookings(guest,None,check_in,check_out,room_type,no_of_guest,status)
            if(not get_guest(phone_number)):
                inserting_guest(guest)
            room_nos=get_all_rooms(room_type)
            flag=True
            flag = True
            room_numbers = [row[0] for row in room_nos]
            for i in room_numbers:
                result = is_available_room(check_in.isoformat(),check_out.isoformat(),i)
                if result:
                    booking.room_no = i
                    inserting_booking(booking)
                    flag = False
                    break

            if flag:
                raise Invalid_Room("No room available for the selected dates")

            print(f"Booking successful! Your room number is {booking.room_no}")
            # if(flag):
            #     raise Invalid_Room("this room is already occupied please try some other room type")
            return booking

        except Invalid as e:
            print(e)
            continue
        except Invalid_Gmail as e:
            print(e)
            continue
        except Invalid_guest_name as e:
            print(e)
            continue
        except Invalid_guest_name as e:
            print(e)
            continue
        except Invalid_phone_number as e:
            print(e)
            continue
        except ValueError as e:
            print(e)
            continue
        except Invalid_Date as e:
            print(e)
            continue
        except  Invalid_Room as e:
            print(e)
            continue
def room_availability():
    try:
        while(True):
            room_type=input("enter the type of room user wanted : ").strip()
            if(room_type==""):
                raise Invalid_Room("the room type cannot be empty")

            if(room_type not in ("Standard","Deluxe","Suite")):
                raise Invalid_Room("the room_type is not correct it should be Standard,Deluxe,Suite")
            
            check_in,check_out=check_in_check_out()
           
            room_types=["Standard","Deluxe","Suite"]
            print("\n\n")

            for i in room_types:

                print("\n")
                print(f"the rooms of type {i} available are : ")
                print("\n")
                room_nos=get_all_rooms(i)
                room_numbers = [row[0] for row in room_nos]

                for j in room_numbers:
                    # check_in=date.today().isoformat()
                    if(is_available_room(check_in.isoformat(),check_out.isoformat(),j)):
                        print(j)
                print("\n")
                print('-'*30)
            break

    except Exception as e:
        print(e)
def check_in_check_out():
    while(True):
        try:
            
            if(room_type not in ("Standard","Deluxe","Suite")):
                raise Invalid_Room("the room_type is not correct it should be Standard,Deluxe,Suite")
            
            check_in=input("enter the date of the stay :").strip()
            date_pattern = r"\d{2}[-]\d{2}[-]\d{4}"
            if not re.fullmatch(date_pattern, check_in):
                raise Invalid_Date("Invalid date format")
            todays_date=date.today()
            check_in=datetime.strptime(check_in, "%d-%m-%Y").date()
            if todays_date>check_in:
                raise Invalid_Date("enter the proper date it cannot be in past")
            if not (todays_date+timedelta(days=180) >=check_in):
                raise Invalid_Date("the check in date cannot be more than 180 from today")
            no_of_days=int(input("Enter the no of days you wanted to stay :").strip())
            if no_of_days<=0 or no_of_days>30:
                raise Invalid("enter the stay days within the range of (1-30)")
            check_out=check_in+timedelta(days=no_of_days)
            return check_in.isoformat(),check_out.isoformat(),room_type
        except Invalid as e:
            print(e)
        except Invalid_Date as e:
            print(e)
        except Invalid_Room as e:
            print(e)

def check_in():
    while(True):
        try:
            phone_number=input("enter the guest phone number :")
            if not re.fullmatch(r'[6-9]\d{9}', phone_number):
                raise Invalid_phone_number("Enter a valid 10-digit mobile number")
            if(not get_guest(phone_number)):
                raise Invalid_phone_number("the guest with this phone number dont exist")
            room_no=input("enter the room no of the guest : ")
            res=getbooking(room_no,phone_number)
            if(res is None):
                raise Invalid_booking("the booking dont exist for this details ")
            check_in_date = date.fromisoformat(res[0])
            if date.today()!=check_in_date:
                raise Invalid_Date("you have registred your booking on some other day not today")
            if res[2]=="CANCELLED":
                raise Invalid_booking("the booking was already cancelled")
            if(res[2]=="CHECKED_IN"):
                raise Invalid_booking("the guest have already checked in")
            if(res[2]=="CHECKED_OUT"):
                raise Invalid_booking("the guest have already checked out")
            
            Update_booking("CHECKED_IN",room_no,phone_number)
            break
        except Invalid_phone_number as e:
            print(e)
            continue
        except Invalid_booking as e:
            print(e)
            continue
        except Invalid_Room as e:
            print(e)
            continue

def check_out():
    while(True):
        try:
            room_no=int(input("enter the room no of the guest").strip())
            phone_number=input("enter the guest phone number :")
            if not re.fullmatch(r'[6-9]\d{9}', phone_number):
                raise Invalid_phone_number("Enter a valid 10-digit mobile number")
            if(not get_guest(phone_number)):
                raise Invalid_phone_number("the guest with this phone number dont exist")      
            res=getbooking(room_no,phone_number)
            check_in_date = date.fromisoformat(res[0])
            check_out_date = date.fromisoformat(res[1])
            if(res is None):
                raise Invalid_booking("the booking dont exist for this details ")
            if(res[2]!="CHECKED_IN"):
                raise Invalid_booking("the guest didnt checked in")
            generate_payroll(check_in_date,check_out_date,res[3])
            Update_booking("CHECKED_OUT",room_no,phone_number)
            
        except Invalid_phone_number as e:
            print(e)
            continue
        except Invalid_booking as e:
            print(e)
            continue

def cancel_booking():
    while(True):
        try:
            room_no=int(input("enter the room no of the guest").strip())
            phone_number=input("enter the guest phone number :")
            if not re.fullmatch(r'[6-9]\d{9}', phone_number):
                raise Invalid_phone_number("Enter a valid 10-digit mobile number")
            if(not get_guest(phone_number)):
                raise Invalid_phone_number("the guest with this phone number dont exist")      
            res=getbooking(room_no,phone_number)
            if(res is None):
                raise Invalid_booking("the booking dont exists")
            check_in_date = date.fromisoformat(res[0])
            if res[2]=="CANCELLED":
                raise Invalid_booking("the booking was already cancelled")
            if(res[2]=="CHECKED_IN"):
                raise Invalid_booking("the guest have already checked in")
            if(res[2]=="CHECKED_OUT"):
                raise Invalid_booking("the guest have already checked out")
            if(date.today()>check_in_date):
                raise Invalid("the guest cannot cancel")
            delta=check_in_check_out-date.today()
            refund=0
            if(delta.days>=7):
                refund=100
            elif(delta.days>=2):
                refund=50
            else:
                refund=0
            
            Update_booking("CANCELLED",room_no,phone_number)
        except Invalid_phone_number as e:
            print(e)
        except Invalid_booking as e:
            print(e)


def view_booking_details():
    bookings=get_booking_details()
    for i in bookings:
        print(f"booking {booking["room_no"]}")
        print(booking["check_in"])
        print(booking["check_out"])
        print(booking["status"])


create_rooms()
create_Guest()
create_booking()

try:
    with open('rooms.csv','r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            room_no=int(row[0])
            room_type=row[1]
            floor=int(row[2])
            
            try:
                if(room_type not in ("Standard","Deluxe","Suite")):
                    raise Invalid("the room type doesnt match")
                if(floor<0):
                    raise Invalid("the floor cannot be negative")
            except Exception as e:
                print(e)
                continue
            room=Room(room_no,room_type,floor)
            if(get_rooms(room_no) is None):
                insert_in_rooms(room)
except FileNotFoundError as e:
    print(e)




while True:
    try:
        choice=int(input("enter the users choice : ").strip())
        if choice==1:
            room_availability()
        elif choice==2:
            booking=createBooking()
        elif choice==3:
            check_in()
        elif choice==4:
            check_out()
        elif choice==5:
            cancel_booking()

        elif choice==6:
            view_booking_details()
        elif choice==11:
            break
        
    except Exception as e:
        print("ERROR:", type(e).__name__, repr(e))