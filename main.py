import mysql.connector
from datetime import datetime

# 1. DATABASE CONNECTION
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", # Keep blank for XAMPP
        database="game_db"
    )

# 2. CREATE TABLE AUTOMATICALLY
def init_db():
    try:
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INT AUTO_INCREMENT PRIMARY KEY,
                player_name VARCHAR(100) NOT NULL,
                score INT NOT NULL,
                played_at DATETIME
            )
        ''')
        db.commit()
        db.close()
        print("✅ Connected to MySQL: Table is ready!")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        print("FIX: Make sure XAMPP MySQL is GREEN and you created 'game_db' in phpMyAdmin.")

# 3. FUNCTION TO ADD DATA
def add_score(name, score):
    db = get_connection()
    cursor = db.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = "INSERT INTO scores (player_name, score, played_at) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, score, now))
    db.commit()
    db.close()
    print(f"✨ Success! {name}'s score is saved.")

# 4. FUNCTION TO READ DATA (LEADERBOARD)
def show_leaderboard():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT player_name, score, played_at FROM scores ORDER BY score DESC")
    results = cursor.fetchall()
    
    print("\n🏆 --- LEADERBOARD --- 🏆")
    print(f"{'Player':<15} {'Score':<10} {'Date':<20}")
    print("-" * 45)
    for row in results:
        print(f"{row[0]:<15} {row[1]:<10} {row[2]}")
    db.close()

# 5. THE MENU SYSTEM
def main():
    init_db()
    while True:
        print("\n--- GAME SCOREBOARD ---")
        print("1. Add Score")
        print("2. View Leaderboard")
        print("3. Exit")
        choice = input("Enter 1, 2, or 3: ")

        if choice == '1':
            n = input("Player Name: ")
            try:
                s = int(input("Score: "))
                add_score(n, s)
            except:
                print("Error: Score must be a number!")
        elif choice == '2':
            show_leaderboard()
        elif choice == '3':
            break

if __name__ == "__main__":
    main()