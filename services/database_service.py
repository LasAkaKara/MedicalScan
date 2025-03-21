import mysql.connector
from datetime import datetime, timedelta
import hashlib
from dotenv import load_dotenv
import os
import json
import pytz

load_dotenv()

class DatabaseService:
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'mediscan')
        }
        self.init_db()

    def connect(self):
        try:
            return mysql.connector.connect(**self.config)
        except Exception as e:
            print(f"Database connection error: {e}")
            return None

    def init_db(self):
        try:
            # Create database if not exists
            self.create_database()
            
            conn = self.connect()
            if not conn:
                return
                
            cursor = conn.cursor(dictionary=True)

            # Create Users table first
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                verification_code VARCHAR(6) DEFAULT NULL,
                code_expiry DATETIME DEFAULT NULL,
                is_verified BOOLEAN DEFAULT FALSE,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
                last_login DATETIME DEFAULT NULL,
                full_name VARCHAR(255) DEFAULT NULL,
                phone VARCHAR(20) DEFAULT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            ''')

            # Create Medicine table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicines (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                information TEXT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            ''')

            # Create Categories table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                name VARCHAR(255) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            ''')

            # Create Prescriptions table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS prescriptions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                created_at TIMESTAMP NOT NULL,
                name VARCHAR(255) NOT NULL,
                user_id INT NOT NULL,
                hospital_name VARCHAR(255),
                category_id INT,
                medicine_details TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (category_id) REFERENCES categories(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            ''')

            # Check if data exists
            cursor.execute("SELECT COUNT(*) as count FROM medicines")
            count = cursor.fetchone()['count']
            
            if count == 0:
                print("Inserting example data...")
                self._insert_example_data(cursor)
                conn.commit()
                print("Example data inserted successfully")

            conn.commit()
            cursor.close()
            conn.close()
            
            print("Database initialized successfully")
            
        except Exception as e:
            print(f"Error initializing database: {e}")
            import traceback
            traceback.print_exc()

    def get_user_prescriptions(self, user_id):
        conn = self.connect()
        if not conn:
            return []
            
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT p.*, c.name as category_name 
                FROM prescriptions p 
                LEFT JOIN categories c ON p.category_id = c.id 
                WHERE p.user_id = %s
                ORDER BY p.created_at DESC
            """, (user_id,))
            
            prescriptions = cursor.fetchall()
            print(f"Found {len(prescriptions)} prescriptions")
            for p in prescriptions:
                print(f"Prescription: {p}")
            
            return prescriptions
        except Exception as e:
            print(f"Error fetching prescriptions: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def create_database(self):
        config = self.config.copy()
        config.pop('database', None)
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.config['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error creating database: {e}")

    def _insert_example_data(self, cursor):
        try:
            # Insert example user first
            example_user = ('example@mediscan.com', self.hash_password('example123'))
            cursor.execute(
                "INSERT INTO users (email, password, is_verified) VALUES (%s, %s, TRUE)",
                example_user
            )
            user_id = cursor.lastrowid  # Get the ID of the inserted user

            # Insert example medicines
            medicines = [
                ('Panadol Extra', 'Thuốc giảm đau, hạ sốt'),
                ('Augmentin 1g', 'Thuốc kháng sinh điều trị nhiễm khuẩn'),
                ('Omeprazole 20mg', 'Thuốc điều trị đau dạ dày, trào ngược'),
                ('Moxifloxacin 400mg', 'Thuốc kháng sinh điều trị viêm phổi'),
                ('Vitamin C 500mg', 'Bổ sung vitamin C tăng đề kháng')
            ]
            cursor.executemany(
                "INSERT INTO medicines (name, information) VALUES (%s, %s)", 
                medicines
            )

            # Insert categories using the actual user_id
            categories = [
                (user_id, 'Bệnh mãn tính'),
                (user_id, 'Điều trị cấp tính'),
                (user_id, 'Thực phẩm chức năng'),
                (user_id, 'Thuốc định kỳ'),
                (user_id, 'Thuốc đau dạ dày')
            ]
            cursor.executemany(
                "INSERT INTO categories (user_id, name) VALUES (%s, %s)",
                categories
            )

            # Get category ID for prescriptions
            cursor.execute("SELECT id FROM categories WHERE name = 'Điều trị cấp tính' AND user_id = %s", (user_id,))
            category_id = cursor.fetchone()['id']

            # Example prescriptions with medicine details
            now = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
            prescriptions = [
                (
                    now.strftime('%Y-%m-%d %H:%M:%S'),
                    'Điều trị viêm họng',
                    user_id,  # Use the actual user_id
                    'Bệnh viện Đa khoa Trung ương',
                    category_id,
                    json.dumps({
                        "medicines": [
                            {
                                "medicine_id": 1,
                                "usage_time": ["sáng", "tối"],
                                "quantity_per_time": 1,
                                "total_quantity": 20,
                                "usage_instruction": "Uống sau khi ăn với nhiều nước",
                                "duration_days": 10
                            }
                        ],
                        "total_medicines": 1
                    })
                )
            ]
            
            cursor.executemany("""
                INSERT INTO prescriptions 
                (created_at, name, user_id, hospital_name, category_id, medicine_details)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, prescriptions)

        except Exception as e:
            print(f"Error inserting example data: {e}")
            raise e

    def check_database(self):
        try:
            conn = self.connect()
            if not conn:
                return
                
            cursor = conn.cursor(dictionary=True)
            
            # Check tables
            tables = ['medicines', 'categories', 'prescriptions']
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                count = cursor.fetchone()['count']
                print(f"Table {table} has {count} records")
                
            # Check example data
            cursor.execute("SELECT * FROM prescriptions")
            prescriptions = cursor.fetchall()
            for p in prescriptions:
                print(f"Found prescription: {p}")
                
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error checking database: {e}")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, email, password, verification_code):
        conn = self.connect()
        if conn:
            cursor = conn.cursor()
            try:
                hashed_password = self.hash_password(password)
                expiry = datetime.now() + timedelta(minutes=5)
                cursor.execute('''
                    INSERT INTO users (email, password, verification_code, code_expiry)
                    VALUES (%s, %s, %s, %s)
                ''', (email, hashed_password, verification_code, expiry))
                conn.commit()
                return True
            except mysql.connector.IntegrityError:
                print("Email already exists")
                return False
            except Exception as e:
                print(f"Error registering user: {e}")
                return False
            finally:
                conn.close()

    def verify_code(self, email, code):
        conn = self.connect()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    UPDATE users 
                    SET is_verified = TRUE 
                    WHERE email = %s 
                    AND verification_code = %s 
                    AND code_expiry > NOW()
                    AND is_verified = FALSE
                ''', (email, code))
                conn.commit()
                return cursor.rowcount > 0
            except Exception as e:
                print(f"Error verifying code: {e}")
                return False
            finally:
                conn.close()

    def validate_user(self, email, password):
        conn = self.connect()
        if conn:
            cursor = conn.cursor()
            try:
                hashed_password = self.hash_password(password)
                cursor.execute('''
                    SELECT id FROM users 
                    WHERE email = %s 
                    AND password = %s 
                    AND is_verified = TRUE
                    AND is_active = TRUE
                ''', (email, hashed_password))
                result = cursor.fetchone()
                
                if result:
                    cursor.execute('''
                        UPDATE users 
                        SET last_login = NOW() 
                        WHERE id = %s
                    ''', (result[0],))
                    conn.commit()
                    return True
                return False
            except Exception as e:
                print(f"Error validating user: {e}")
                return False
            finally:
                conn.close()
        return False

    def update_verification_code(self, email, new_code):
        conn = self.connect()
        if conn:
            cursor = conn.cursor()
            try:
                expiry = datetime.now() + timedelta(minutes=5)
                cursor.execute('''
                    UPDATE users 
                    SET verification_code = %s, code_expiry = %s
                    WHERE email = %s
                ''', (new_code, expiry, email))
                conn.commit()
                return cursor.rowcount > 0
            except Exception as e:
                print(f"Error updating verification code: {e}")
                return False
            finally:
                conn.close()
        return False

    def show_users(self):
        conn = self.connect()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    SELECT id, email, is_verified, verification_code, 
                           code_expiry, created_at, last_login 
                    FROM users
                ''')
                users = cursor.fetchall()
                print("\nUsers in database:")
                print("ID | Email | Verified | Code | Expiry | Created | Last Login")
                print("-" * 80)
                for user in users:
                    print(f"{user[0]} | {user[1]} | {'Yes' if user[2] else 'No'} | {user[3]} | {user[4]} | {user[5]} | {user[6]}")
            finally:
                conn.close()

    def get_prescription_detail(self, prescription_id):
        conn = self.connect()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT p.*, c.name as category_name 
                FROM prescriptions p 
                LEFT JOIN categories c ON p.category_id = c.id 
                WHERE p.id = %s
            """, (prescription_id,))
            
            prescription = cursor.fetchone()
            if prescription:
                # Parse medicine_details from JSON
                if 'medicine_details' in prescription:
                    prescription['medicine_details'] = json.loads(prescription['medicine_details'])
                return prescription
            return None
        except Exception as e:
            print(f"Error fetching prescription detail: {e}")
            return None
        finally:
            cursor.close()
            conn.close() 