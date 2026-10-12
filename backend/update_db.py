import sqlite3

def update():
    conn = sqlite3.connect('lexsentry.db')
    conn.execute("UPDATE documents SET original_url='/Brief1.pdf'")
    conn.commit()
    conn.close()
    print("Updated URLs successfully.")

if __name__ == '__main__':
    update()
