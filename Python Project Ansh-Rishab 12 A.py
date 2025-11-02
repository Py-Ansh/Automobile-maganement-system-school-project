import mysql.connector as sql
import pickle

# Database connection
def connect():
    c = sql.connect(host="localhost", user="root", passwd="ansh", database="auto_db", auth_plugin='mysql_native_password')
    return c

# Setup database and table
def setup():
    try:
        c = sql.connect(host="localhost", user="root", passwd="ansh", auth_plugin='mysql_native_password')
        cur = c.cursor(buffered=True)
        
        # Create database if not exists
        cur.execute("CREATE DATABASE IF NOT EXISTS auto_db")
        cur.execute("USE auto_db")
        
        # Create table if not exists
        q = "CREATE TABLE IF NOT EXISTS vehicles (id INT PRIMARY KEY AUTO_INCREMENT, reg_no VARCHAR(50), model VARCHAR(50), brand VARCHAR(50), year INT, price FLOAT)"
        cur.execute(q)
        
        c.commit()
        cur.close()
        c.close()
        
    except:
        print("Error in database setup!")
        exit()








# Create vehicle (INSERT)
def add():
    print("\n" + "="*60)
    print(" "*20 + "ADD NEW VEHICLE")
    print("="*60)
    
    c = connect()
    cur = c.cursor(buffered=True)
    
    r = input("\nEnter Registration No: ")
    m = input("Enter Model: ")
    b = input("Enter Brand: ")
    y = int(input("Enter Year: "))
    p = float(input("Enter Price: "))
    
    q = "INSERT INTO vehicles (reg_no, model, brand, year, price) VALUES ('" + r + "','" + m + "','" + b + "'," + str(y) + "," + str(p) + ")"
    
    cur.execute(q)
    c.commit()
    
    print("\n" + "-"*60)
    print("✓ Vehicle added successfully!")
    print("-"*60)
    
    cur.close()
    c.close()








# Read all vehicles (SELECT)
def display():
    print("\n" + "="*60)
    print(" "*18 + "ALL VEHICLE RECORDS")
    print("="*60)
    
    c = connect()
    cur = c.cursor(buffered=True)
    
    q = "SELECT * FROM vehicles"
    cur.execute(q)
    
    data = cur.fetchall()
    
    if len(data) == 0:
        print("\n⚠ No records found in database!")
    else:
        print("\nID    REG NO          MODEL           BRAND        YEAR   PRICE")
        print("------------------------------------------------------------")
        for i in data:
            print(str(i[0]) + "     " + str(i[1]) + "                " + str(i[2]) + "             " + str(i[3]) + "            " + str(i[4]) + "         " + str(i[5]))
        print("------------------------------------------------------------")
        print("Total Records: " + str(len(data)))
    
    cur.close()
    c.close()







# Search vehicle
def search():
    print("\n" + "╔" + "═"*58 + "╗")
    print("║" + " "*20 + "SEARCH VEHICLE" + " "*24 + "║")
    print("╚" + "═"*58 + "╝")
    
    c = connect()
    cur = c.cursor(buffered=True)  
    
    r = input("\n➜ Enter Registration No to search: ")
    
    q = "SELECT * FROM vehicles WHERE reg_no = %s"
    cur.execute(q, (r,))
    
    data = cur.fetchone()
    
    if data == None:
        print("\n┌" + "─"*58 + "┐")
        print("│  ⚠  Vehicle not found!" + " "*33 + "│")
        print("└" + "─"*58 + "┘")
    else:
        print("\n╔" + "═"*58 + "╗")
        print("║" + " "*20 + "VEHICLE DETAILS" + " "*23 + "║")
        print("╚" + "═"*58 + "╝")
        print("\n┌" + "─"*57 + "┐")
        print("│  ID              : " + str(data[0]) + " "*(37-len(str(data[0]))) + "│")
        print("│  Registration No : " + str(data[1]) + " "*(37-len(str(data[1]))) + "│")
        print("│  Model           : " + str(data[2]) + " "*(37-len(str(data[2]))) + "│")
        print("│  Brand           : " + str(data[3]) + " "*(37-len(str(data[3]))) + "│")
        print("│  Year            : " + str(data[4]) + " "*(37-len(str(data[4]))) + "│")
        print("│  Price           : Rs." + str(data[5]) + " "*(34-len(str(data[5]))) + "│")
        print("└" + "─"*57 + "┘")
    
    cur.close()
    c.close()







# Update vehicle
def update():
    print("\n" + "="*60)
    print(" "*20 + "UPDATE VEHICLE")
    print("="*60)
    
    c = connect()
    cur = c.cursor(buffered=True)
    
    r = input("\nEnter Registration No to update: ")
    
    # Check if exists
    q1 = "SELECT * FROM vehicles WHERE reg_no = '" + r + "'"
    cur.execute(q1)
    data = cur.fetchone()
    
    if data == None:
        print("\n⚠ Vehicle not found!")
    else:
        print("\n" + "-"*60)
        print("CURRENT DETAILS:")
        print("-"*60)
        print("Model : " + str(data[2]))
        print("Brand : " + str(data[3]))
        print("Year  : " + str(data[4]))
        print("Price : Rs." + str(data[5]))
        print("-"*60)
        
        print("\nEnter New Details:")
        m = input("Enter new Model: ")
        b = input("Enter new Brand: ")
        y = int(input("Enter new Year: "))
        p = float(input("Enter new Price: "))
        
        q2 = "UPDATE vehicles SET model='" + m + "', brand='" + b + "', year=" + str(y) + ", price=" + str(p) + " WHERE reg_no='" + r + "'"
        
        cur.execute(q2)
        c.commit()
        
        print("\n" + "-"*60)
        print("✓ Vehicle updated successfully!")
        print("-"*60)
    
    cur.close()
    c.close()








# Delete vehicle
def delete():
    print("\n" + "="*60)
    print(" "*20 + "DELETE VEHICLE")
    print("="*60)
    
    c = connect()
    cur = c.cursor(buffered=True)
    
    r = input("\nEnter Registration No to delete: ")
    
    q = "DELETE FROM vehicles WHERE reg_no = '" + r + "'"
    cur.execute(q)
    c.commit()
    
    print("\n" + "-"*60)
    if cur.rowcount > 0:
        print("✓ Vehicle deleted successfully!")
    else:
        print("⚠ Vehicle not found!")
    print("-"*60)
    
    cur.close()
    c.close()










# Backup to file using pickle (DUMP)
def backup():
    print("\n" + "="*60)
    print(" "*18 + "BACKUP TO FILE")
    print("="*60)
    
    c = connect()
    cur = c.cursor(buffered=True)
    
    q = "SELECT * FROM vehicles"
    cur.execute(q)
    data = cur.fetchall()
    
    f = open("vehicles.dat", "wb")
    pickle.dump(data, f)
    f.close()
    
    print("\n" + "-"*60)
    print("✓ Backup successful!")
    print("✓ " + str(len(data)) + " records saved to 'vehicles.dat'")
    print("-"*60)
    
    cur.close()
    c.close()







# Restore from file using pickle (LOAD)
def restore():
    print("\n" + "="*60)
    print(" "*17 + "RESTORE FROM FILE")
    print("="*60)
    
    try:
        f = open("vehicles.dat", "rb")
        data = pickle.load(f)
        f.close()
        
        c = connect()
        cur = c.cursor(buffered=True)
        
        # Clear existing data
        q1 = "DELETE FROM vehicles"
        cur.execute(q1)
        
        # Insert backup data
        for i in data:
            q2 = "INSERT INTO vehicles (id, reg_no, model, brand, year, price) VALUES (" + str(i[0]) + ",'" + str(i[1]) + "','" + str(i[2]) + "','" + str(i[3]) + "'," + str(i[4]) + "," + str(i[5]) + ")"
            cur.execute(q2)
        
        c.commit()
        
        print("\n" + "-"*60)
        print("✓ Restore successful!")
        print("✓ " + str(len(data)) + " records restored from 'vehicles.dat'")
        print("-"*60)
        
        cur.close()
        c.close()
        
    except FileNotFoundError:
        print("\n" + "-"*60)
        print("⚠ Backup file 'vehicles.dat' not found!")
        print("-"*60)


# Main menu
def menu():
    while True:
        
        print("\n┌" + "─"*57 + "┐")
        print("│  [1] ➤ Add Vehicle" + " "*38 + "│")
        print("│  [2] ➤ Display All Vehicles" + " "*29 + "│")
        print("│  [3] ➤ Search Vehicle" + " "*35 + "│")
        print("│  [4] ➤ Update Vehicle" + " "*35 + "│")
        print("│  [5] ➤ Delete Vehicle" + " "*35 + "│")
        print("│  [6] ➤ Backup to File (Pickle)" + " "*26 + "│")
        print("│  [7] ➤ Restore from File (Pickle)" + " "*23 + "│")
        print("│  [8] ➤ Exit" + " "*45 + "│")
        print("└" + "─"*57 + "┘")
        
        ch = input("\n➜ Enter your choice (1-8): ")
        
        if ch == "1":
            add()
        elif ch == "2":
            display()
        elif ch == "3":
            search()
        elif ch == "4":
            update()
        elif ch == "5":
            delete()
        elif ch == "6":
            backup()
        elif ch == "7":
            restore()
        elif ch == "8":
            print("\n╔" + "═"*58 + "╗")
            print("║" + " "*58 + "║")
            print("║" + " "*15 + "THANK YOU FOR USING!" + " "*24 + "║")
            print("║" + " "*10 + "AUTOMOBILE MANAGEMENT SYSTEM" + " "*20 + "║")
            print("║" + " "*58 + "║")
            print("╚" + "═"*58 + "╝\n")
            break
        else:
            print("\n┌" + "─"*58 + "┐")
            print("│  ⚠  Invalid choice! Please enter number between 1-8" + " "*4 + "│")
            print("└" + "─"*58 + "┘")


# Run the program
print("\n")
print("╔═════════════════════════════════════════════════════════════════╗")
print("║                                                                 ║")
print("║  ██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗ ║")
print("║  ██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝ ║")
print("║  ██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗   ║")
print("║  ██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝   ║")
print("║  ╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗ ║")
print("║   ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝ ║")
print("║                                                                 ║")
print("║              AUTOMOBILE MANAGEMENT SYSTEM                       ║")
print("║                                                                 ║")
print("╚═════════════════════════════════════════════════════════════════╝")

# Project description
print("\n" + "┌" + "─"*58 + "┐")
print("│" + " "*16 + "PROJECT DESCRIPTION" + " "*23 + "│")
print("└" + "─"*58 + "┘")



print("\n▶ 1. PYTHON-MYSQL CONNECTIVITY")
print("  ├─ Connecting Python with MySQL database")
print("  └─ Executing SQL queries from Python")

print("\n▶ 2. CRUD OPERATIONS (Database Management)")
print("  ├─ [C] CREATE  → Add new vehicle records")
print("  ├─ [R] READ    → Display all vehicle records")
print("  ├─ [U] UPDATE  → Modify existing vehicle details")
print("  ├─ [D] DELETE  → Remove vehicle records")
print("  └─ [S] SEARCH  → Find vehicles by registration number")

print("\n▶ 3. PICKLE MODULE (File Handling)")
print("  ├─ BACKUP  : Export database records to binary file")
print("  ├─ RESTORE : Import records from binary file")
print("  └─ Uses pickle.dump() and pickle.load() functions")

print("\n" + "═"*60)
print("\n⏎  Press Enter to continue...")
input()

# Setup database and table
setup()

menu()