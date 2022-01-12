import sys
import sqlite3
from sqlite3 import Error
import os
import time
from pyfiglet import Figlet
from termcolor import colored, cprint

class App():
    def __init__(self):
        super().__init__()
        self.clear_terminal()
        self.banner("Pass Vaulter")
        self.main()
        
    def main(self):
        cprint("===================================================","cyan")
        print("\t\tSelect an action: ")
        cprint("===================================================","cyan")
        cprint("\t[1] Save a new password","yellow")
        cprint("\t[2] Search Saved Password","yellow")
        cprint("\t[3] Exit","yellow")
        cprint("===================================================","cyan")
        self.choice = int(input("Enter any choice [1,2,3]: "))
        if (self.choice == 1):
            self.save_pass()
        elif(self.choice == 2):
            self.search_pass()
        elif(self.choice == 3):
            sys.exit()
        else :
            cprint("Invalid Choice.","red")
            time.sleep(2)
            self.clear_terminal()
            self.banner("Pass Vaulter")
            self.main()
    def banner(self,text):
        f = Figlet(font="doom")
        output_txt = colored(f.renderText(text),"blue")
        print(output_txt)
        cprint("Welcome to Pass Vaulter!","yellow")
        cprint("""
App: PassVaulter
Creator: @Raunak Raj
Version: 1.1
        ""","blue")
    def clear_terminal(self):
        os.system("clear")
    def save_pass(self):
        self.clear_terminal()
        self.banner("Pass Vaulter")
        cprint("===================================================","cyan")
        print("\t\tSave a New Password")
        cprint("===================================================","cyan")
        web_nme=str(input("Enter the name of platform(eg.:google)? "))
        email=str(input("Enter your email? "))
        password=str(input("Enter your password? "))
        cprint(f"\nPlatform Name: {web_nme}","red")
        cprint(f"Email for {web_nme}: {email}","red")
        cprint(f"Password for {web_nme}: {password}","red")
        cprint("\nPlesse confirm the above information before saving.","blue")
        verfy = str(input("Do you want to continue(yes/no)? "))
        if verfy == "yes" or verfy == "Yes" or verfy == "y" or verfy == "Y":
            conn = self.create_connection("passDB.db")
            with conn:
                data = (web_nme,email,password)
                if self.save_new_pass(conn, data) != 0:
                    cprint("\nYour password saved successfully.", "green")
                    time.sleep(2)
                    self.clear_terminal()
                    self.banner("Pass Vaulter")
                    self.main()
                else:
                    cprint("\n Error.....", "red")
                    time.sleep(2)
                    self.clear_terminal()
                    self.banner("Pass Vaulter")
                    self.main()
        else:
            self.save_pass()
    def save_new_pass(self,conn,data):
        sql = ''' INSERT INTO password(platform_name,email,password)
              VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS password(
        id INTEGER PRIMARY KEY,
        platform_name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL);
        """)
        cur.execute(sql, data)
        conn.commit()
        return cur.lastrowid
    def search_pass(self):
        self.clear_terminal()
        self.banner("Pass Vaulter")
        cprint("===================================================","cyan")
        print("\t\tSearch Saved Password")
        cprint("===================================================","cyan")
        ser_val = str(input("Enter platform name to search their password : "))
        conn = self.create_connection("passDB.db")
        with conn:
            cprint(f'\nSearch result for "{ser_val}" :-\n','blue')
            self.select_pass(conn,ser_val)
            time.sleep(2)
            self.banner("Pass Vaulter")
            self.main()
    def select_pass(self,conn,query):
        cur = conn.cursor()
        cur.execute("SELECT * FROM password WHERE platform_name = ?",(query,))
        rows = cur.fetchall()
        for row in rows:
            cprint(f"\tId : {row[0]}","magenta")
            cprint(f"\tPlatform : {row[1]}","magenta")
            cprint(f"\tEmail : {row[2]}",'magenta')
            cprint(f"\tPassword : {row[3]}",'magenta')
    
    def create_connection(self,db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except:
            cprint("Error","red")
        return conn

if __name__ == "__main__":
    app = App()