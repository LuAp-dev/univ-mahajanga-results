# test_connection.py
import pymysql

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',  # ou 'api_python'
        password='',  # ou votre mot de passe
        database='smartscol',
        charset='utf8mb4'
    )
    print("✅ Connexion MySQL réussie !")
    
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"📋 Tables trouvées : {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
            
except Exception as e:
    print(f"❌ Erreur de connexion : {e}")
finally:
    if 'connection' in locals():
        connection.close()