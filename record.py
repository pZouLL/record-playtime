import ctypes
import sqlite3 
from threading import Thread 
import os 
import time 


conn = sqlite3.connect('db.db' , check_same_thread=False)

c = conn.cursor()

try:
    c.execute("CREATE TABLE files (name text)")
    c.execute("CREATE TABLE playtime (name text , playtime1 text)")
except:
    pass



running = []    

def get_active_window():
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible

    titles = []
    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            titles.append(buff.value)
        return True
    EnumWindows(EnumWindowsProc(foreach_window), 0)


    return titles


print("Welcome")

def play(app):
    os.system(f'start shortcuts/{app.lower()}.lnk')
    while True:
        time.sleep(117)
        c.execute("SELECT * FROM playtime WHERE name =?" , [app])
        current_playtime = c.fetchall()[0][1]
        bener = False 
        thing = get_active_window()
        for x in thing:
            x = x.lower() 
            x = x.replace(" " , "")
            if app.lower() in x:
                bener = True 
                break

        if bener:
            current_playtime = int(current_playtime) + 120
            c.execute("UPDATE playtime SET playtime1 = ? WHERE name = ?", [current_playtime , app.lower()])
            conn.commit()

        else:
            running.pop(running.index(app))
            return




while True:
    print("""
==============================
Options:
1. See all available apps 
2. Add new app
3. Play an app
4. Check playtime
5. Delete app
6. Exit 
==============================
    """)

    choice = int(input('Choice : '))

    if choice == 1:
        c.execute("SELECT * FROM files")
        for x in c.fetchall():
            print(x[0])

    elif choice == 2:
        new_app = input("New App: ").lower()
        c.execute("SELECT * FROM files WHERE name = ?" , [new_app])
        if c.fetchall():
            print("Already Exist")
        else:
            c.execute("INSERT INTO files VALUES (?)" , [new_app.lower()])
            conn.commit()
            c.execute("INSERT INTO playtime VALUES (?,?)" , [new_app.lower(),0])
            conn.commit()
            print("Added")

    elif choice == 3:
        app = input("App Name: ")
        c.execute("SELECT * FROM files WHERE name = ?" , [app.lower()])
        if c.fetchall():
            if app.lower() in running:
                print("Already Running")
            else:
                running.append(app.lower())
                new_thread = Thread(target = play , args = [app]).start()
        else:
            print("Doesn't Exist")

    elif choice == 4:
        app = input("App Name: ")
        c.execute("SELECT * FROM playtime WHERE name = ?" , [app.lower()])   
        thing = c.fetchall()
        if thing != []:
            print(f'{thing[0][0]} = {int(thing[0][1])/3600} Hours')

    elif choice == 5:
        app = input("App Name: ").lower()
        c.execute("DELETE FROM playtime WHERE name = ?" , [app])
        conn.commit()
        c.execute("DELETE FROM files WHERE name = ?" , [app])
        conn.commit()
        print('Deleted')

    elif choice == 6:
        break

    else:
        print("Invalid")







