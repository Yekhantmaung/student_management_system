import sqlite3

class StudentManagementSystem:
    def __init__(self):
        # ကျောင်းသား data သိမ်းမယ့် database file နှင့် ချိတ်ဆက်ခြင်း
        self.conn = sqlite3.connect("student_database.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    # Database Table မရှိသေးရင် ဆောက်ပေးမယ့် Function
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age TEXT,
                grade TEXT
            )
        """)
        self.conn.commit()

    # 1. Add New Student (Database ထဲ Data အသစ်ထည့်ခြင်း)
    def add_student(self):
        print("\n--- Add New Student ---")
        student_id = input("Enter Student ID: ").strip()
        
        # ID ရှိပြီးသားလား အရင်စစ်ဆေးခြင်း
        self.cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        if self.cursor.fetchone():
            print("❌ Error: A student with this ID already exists.")
            return
            
        name = input("Enter Name: ").strip()
        age = input("Enter Age: ").strip()
        grade = input("Enter Grade/Class: ").strip()
        
        # SQL Insert Command သုံးပြီး Database ထဲ ထည့်ခြင်း
        self.cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?)", (student_id, name, age, grade))
        self.conn.commit() # Database ထဲ တကယ်သိမ်းဖို့ Commit လုပ်ရပါမယ်
        print(f"✅ Success: Student '{name}' has been saved to database.")

    # 2. View All Students (Database ထဲက Data တွေအကုန် ဆွဲထုတ်ပြခြင်း)
    def view_students(self):
        print("\n--- Student List ---")
        self.cursor.execute("SELECT * FROM students")
        rows = self.cursor.fetchall()
        
        if not rows:
            print("📭 No students found in the database.")
            return
            
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Age: {row[2]} | Grade: {row[3]}")

    # 3. Search Student by ID (ID နဲ့ ကွက်တိ ရှာခြင်း)
    def search_student(self):
        print("\n--- Search Student ---")
        student_id = input("Enter Student ID to search: ").strip()
        
        self.cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        row = self.cursor.fetchone()
        
        if row:
            print("\n🔍 Student Found:")
            print(f"ID: {row[0]} | Name: {row[1]} | Age: {row[2]} | Grade: {row[3]}")
        else:
            print("❌ Error: Student not found with this ID.")

    # 4. Delete Student from Database (စာရင်းဖျက်ခြင်း)
    def delete_student(self):
        print("\n--- Delete Student ---")
        student_id = input("Enter Student ID to delete: ").strip()
        
        # ဖျက်မယ့်ကျောင်းသား ရှိ၊ မရှိ အရင်စစ်ခြင်း
        self.cursor.execute("SELECT name FROM students WHERE student_id = ?", (student_id,))
        row = self.cursor.fetchone()
        
        if row:
            student_name = row[0]
            # SQL Delete Command ဖြင့် ဖျက်ခြင်း
            self.cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
            self.conn.commit()
            print(f"🗑️ Success: Student '{student_name}' has been deleted from database.")
        else:
            print("❌ Error: Student not found with this ID.")

    # Program ပိတ်တဲ့အခါ Database Connection ကို သေသေချာချာ ပိတ်ပေးခြင်း
    def close_connection(self):
        self.conn.close()


# --- Main Program Menu ---
def main():
    sms = StudentManagementSystem()
    
    while True:
        print("\n==============================")
        print("🎓 STUDENT MANAGEMENT SYSTEM (DB) 🎓")
        print("==============================")
        print("1. Add New Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Delete Student")
        print("5. Exit Program")
        
        choice = input("\nPlease select an option (1-5): ").strip()
        
        if choice == '1':
            sms.add_student()
        elif choice == '2':
            sms.view_students()
        elif choice == '3':
            sms.search_student()
        elif choice == '4':
            sms.delete_student()
        elif choice == '5':
            sms.close_connection() # DB ပိတ်မယ်
            print("\n👋 Connection closed. Exiting the program. Have a great day!")
            break
        else:
            print("⚠️ Invalid choice! Please select a number between 1 and 5.")

if __name__ == "__main__":
    main()