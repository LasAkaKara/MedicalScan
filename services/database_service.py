import mysql.connector
from datetime import datetime, timedelta
import hashlib
from dotenv import load_dotenv
import os
import json
import pytz
import logging

load_dotenv()

Logger = logging.getLogger(__name__)

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
                phone VARCHAR(20) DEFAULT NULL,
                preferences TEXT DEFAULT NULL,
                health_data TEXT DEFAULT NULL,
                avatar_url VARCHAR(255) DEFAULT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            ''')

            # Check if the preferences and health_data columns exist, if not add them
            try:
                cursor.execute("SHOW COLUMNS FROM users LIKE 'preferences'")
                if not cursor.fetchone():
                    cursor.execute("ALTER TABLE users ADD COLUMN preferences TEXT DEFAULT NULL")
                    print("Added preferences column to users table")
                
                cursor.execute("SHOW COLUMNS FROM users LIKE 'health_data'")
                if not cursor.fetchone():
                    cursor.execute("ALTER TABLE users ADD COLUMN health_data TEXT DEFAULT NULL")
                    print("Added health_data column to users table")
            except Exception as e:
                print(f"Error checking/adding columns: {e}")

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

            # Create Notifications table with enhanced status tracking
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicine_notifications (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                prescription_id INT NOT NULL,
                medicines_json TEXT NOT NULL,
                time_label VARCHAR(16) NOT NULL,
                notify_date DATE NOT NULL,
                taken BOOLEAN DEFAULT FALSE,
                taken_at DATETIME DEFAULT NULL,
                status ENUM('pending', 'taken', 'missed') DEFAULT 'pending',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (prescription_id) REFERENCES prescriptions(id),
                INDEX idx_user_date (user_id, notify_date),
                INDEX idx_status_date (status, notify_date)
            );
            ''')

            # Check if status column exists, if not add it
            try:
                cursor.execute("SHOW COLUMNS FROM medicine_notifications LIKE 'status'")
                if not cursor.fetchone():
                    cursor.execute("ALTER TABLE medicine_notifications ADD COLUMN status ENUM('pending', 'taken', 'missed') DEFAULT 'pending'")
                    print("Added status column to medicine_notifications table")
                
                cursor.execute("SHOW COLUMNS FROM medicine_notifications LIKE 'updated_at'")
                if not cursor.fetchone():
                    cursor.execute("ALTER TABLE medicine_notifications ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
                    print("Added updated_at column to medicine_notifications table")
            except Exception as e:
                print(f"Error checking/adding notification columns: {e}")

            # Try to create scans table for tracking scan history
            try:
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS scans (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
                    image_path VARCHAR(255),
                    scan_result TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                ''')
                print("Created scans table if it didn't exist")
            except Exception as e:
                print(f"Error creating scans table: {e}")

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
            # for p in prescriptions:
            #     print(f"Prescription: {p}")
            
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
                    'Đơn thuốc điều trị cảm cúm',
                    user_id,  # Use the actual user_id
                    'Phòng khám Đa khoa Quốc tế',
                    category_id,
                    json.dumps({
                        "patient_name": "Bệnh nhân.176215",
                        "doctor_name": "Bác sỹ.165752",
                        "age": 7,
                        "weight": "58kg",
                        "gender": "Nam",
                        "diagnosis": "Ung Thư Vòm Họng Giai Đoạn Đầu",
                        "medicines": [
                            {
                                "medicine_name": "Metformin Hydrochloride",
                                "type": "Viên",
                                "strength": "850 mg",
                                "total_quantity": "27 Viên",
                                "quantity_per_time": "3 Viên 1 ngày 3 lần.",
                                "duration_days": "9 ngày",
                                "usage_instruction": "",
                                "usage_time": [
                                    {"time": "Sáng", "quantity": 1},
                                    {"time": "Trưa", "quantity": 1},
                                    {"time": "Tối", "quantity": 1},
                                ],
                            },
                            {
                                "medicine_name": "Fexofenadine Hydrochloride",
                                "type": "Viên",
                                "strength": "120 mg",
                                "total_quantity": "27 Viên",
                                "quantity_per_time": "3 Viên 1 ngày 3 lần.",
                                "duration_days": "9 ngày",
                                "usage_instruction": "",
                                "usage_time": [
                                    {"time": "Sáng", "quantity": 1},
                                    {"time": "Trưa", "quantity": 1},
                                    {"time": "Tối", "quantity": 1},
                                ],
                            },
                            {
                                "medicine_name": "Tamsulosin Hydrochloride",
                                "type": "Viên",
                                "strength": "0.4 mg",
                                "total_quantity": "20 Viên",
                                "quantity_per_time": "Sáng 1 Viên, Trưa 1 Viên, trước khi ăn.",
                                "duration_days": "10 ngày",
                                "usage_instruction": "",
                                "usage_time": [
                                    {"time": "Sáng", "quantity": 1},
                                    {"time": "Trưa", "quantity": 1},
                                ],
                            },
                            {
                                "medicine_name": "Carboxymethyl Cellulose + Glycerin",
                                "type": "Viên",
                                "strength": "0.5%+0.9%",
                                "total_quantity": "20 ml",
                                "quantity_per_time": "1 ml khi buồn nôn.",
                                "duration_days": "10 ngày",
                                "usage_instruction": "",
                                "usage_time": [
                                    {"time": "Khi buồn nôn", "quantity": "1ml"},
                                ],
                            }
                        ]
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
        """Hash a password for storing"""
        if not password:
            return ""
        return hashlib.md5(password.encode()).hexdigest()

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

    def check_verification_status(self, email):
        """Check if a user exists but is not verified yet"""
        conn = self.connect()
        if not conn:
            return "unknown"
            
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute('''
                SELECT is_verified 
                FROM users 
                WHERE email = %s
            ''', (email,))
            
            result = cursor.fetchone()
            if not result:
                return "not_found"  # User doesn't exist
                
            if not result['is_verified']:
                return "unverified"  # User exists but not verified
                
            return "verified"  # User exists and is verified
        except Exception as e:
            print(f"Error checking verification status: {e}")
            return "unknown"
        finally:
            cursor.close()
            conn.close()

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
                if 'medicine_details' in prescription and isinstance(prescription['medicine_details'], str):
                    try:
                        details_str = prescription['medicine_details']
                        Logger.info(f"Attempting to parse medicine_details JSON for ID {prescription_id}")
                        prescription['medicine_details'] = json.loads(details_str)
                        Logger.info(f"Successfully parsed medicine_details for ID {prescription_id}")
                    except json.JSONDecodeError as json_err:
                        Logger.error(f"JSONDecodeError parsing medicine_details for ID {prescription_id}: {json_err}")
                        Logger.error(f"Problematic JSON string: {details_str}")
                        # Decide how to handle - maybe return None or prescription with raw string?
                        # For now, let's set it to an empty dict to avoid crashing later stages 
                        # but log the error clearly.
                        prescription['medicine_details'] = {'medicines': []} # Provide default structure
                    except Exception as inner_e:
                         Logger.error(f"Unexpected error during JSON parsing for ID {prescription_id}: {inner_e}")
                         prescription['medicine_details'] = {'medicines': []} # Provide default structure
                elif 'medicine_details' not in prescription:
                     Logger.warning(f"medicine_details field missing for prescription ID {prescription_id}")
                     prescription['medicine_details'] = {'medicines': []} # Provide default structure
                # If it's already a dict (or other type), log a warning but proceed
                elif not isinstance(prescription['medicine_details'], str):
                    Logger.warning(f"medicine_details for ID {prescription_id} is not a string, type: {type(prescription['medicine_details'])}. Assuming already parsed.")
                    # Ensure it has the expected structure if possible
                    if not isinstance(prescription['medicine_details'], dict) or 'medicines' not in prescription['medicine_details']:
                         prescription['medicine_details'] = {'medicines': []} 
                         
                return prescription
            else:
                Logger.warning(f"Prescription with ID {prescription_id} not found in database.")
                return None
        except Exception as e:
            Logger.error(f"Error fetching prescription detail in DB service for ID {prescription_id}: {e}")
            import traceback
            traceback.print_exc() # Print full traceback for DB errors
            return None
        finally:
            cursor.close()
            conn.close()
    
    def get_user_by_email(self, email):
        conn = self.connect()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                # Get prescription count
                cursor.execute("SELECT COUNT(*) as count FROM prescriptions WHERE user_id = %s", (user['id'],))
                result = cursor.fetchone()
                user['prescription_count'] = result['count'] if result else 0
            return user
        except Exception as e:
            print(f"Error fetching user by email: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_current_user(self):
        """Get the current user from the database (placeholder for session management)"""
        conn = self.connect()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            # In a real application, this would use the logged-in user ID
            # For this example, we'll just get the first verified user
            cursor.execute("""
                SELECT id, email, full_name, phone
                FROM users
                WHERE is_verified = TRUE
                LIMIT 1
            """)
            
            user = cursor.fetchone()
            if user:
                # Add username field (using email prefix)
                if user['email'] and '@' in user['email']:
                    user['username'] = user['email'].split('@')[0]
                else:
                    user['username'] = user['email'] or "user"
                
                # Convert None values to empty strings
                for key in user:
                    if user[key] is None:
                        user[key] = ""
            
            return user
        except Exception as e:
            print(f"Error fetching current user: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def update_user_profile(self, username, email, full_name, phone, preferences=None, health_data=None):
        """Update user profile information"""
        conn = self.connect()
        if not conn:
            return False
            
        try:
            cursor = conn.cursor()
            
            # For now we're using the username to identify the user
            # In a real application, you'd use the user ID
            
            # Check if user exists
            cursor.execute("SELECT id FROM users WHERE email = %s", (username,))
            result = cursor.fetchone()
            
            if not result:
                return False
                
            # Update user data
            if preferences is None:
                preferences = '{}'
                
            if health_data is None:
                health_data = '{}'
                
            cursor.execute("""
                UPDATE users 
                SET email = %s, full_name = %s, phone = %s, preferences = %s, health_data = %s
                WHERE email = %s
            """, (email, full_name, phone, preferences, health_data, username))
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error updating user profile: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            if cursor:
                cursor.close()
            conn.close()

    def update_user_avatar(self, user_id, avatar_url):
        conn = self.connect()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE users SET avatar_url = %s WHERE id = %s", (avatar_url, user_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating avatar: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def verify_password(self, username, password):
        """Verify a user's password"""
        conn = self.connect()
        if not conn:
            return False
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            # Check if username is actually an email
            if '@' in username:
                email = username
            else:
                # Try to find the email associated with this username
                cursor.execute("SELECT email FROM users WHERE email LIKE %s", (f"{username}@%",))
                result = cursor.fetchone()
                if not result:
                    return False
                email = result['email']
            
            # Hash the provided password
            hashed_password = self.hash_password(password)
            
            # Check if the credentials match
            cursor.execute("""
                SELECT id FROM users
                WHERE email = %s AND password = %s
            """, (email, hashed_password))
            
            result = cursor.fetchone()
            return result is not None
        except Exception as e:
            print(f"Error verifying password: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def update_password(self, username, new_password):
        """Update a user's password"""
        conn = self.connect()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        try:
            # Check if username is actually an email
            if '@' in username:
                email = username
            else:
                # Try to find the email associated with this username
                cursor.execute("SELECT email FROM users WHERE email LIKE %s", (f"{username}@%",))
                result = cursor.fetchone()
                if not result:
                    return False
                email = result[0]
            
            # Hash the new password
            hashed_password = self.hash_password(new_password)
            
            # Update the password
            cursor.execute("""
                UPDATE users
                SET password = %s
                WHERE email = %s
            """, (hashed_password, email))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating password: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def close(self):
        """Close the database connection"""
        # Since we're using a connection pool, this doesn't have to do anything
        # The connections are automatically returned to the pool when closed
        pass

    def email_exists(self, email):
        """Check if email already exists in the database"""
        conn = self.connect()
        if not conn:
            return True  # Assume it exists if DB connection fails for safety
            
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT COUNT(*) FROM users WHERE email = %s
            ''', (email,))
            
            count = cursor.fetchone()[0]
            return count > 0
        except Exception as e:
            print(f"Error checking if email exists: {e}")
            return True  # Assume it exists on error for safety
        finally:
            cursor.close()
            conn.close()

    def save_reset_code(self, email, reset_code):
        """Save a password reset code for a user"""
        conn = self.connect()
        if not conn:
            return False
            
        cursor = conn.cursor()
        try:
            # Set the reset code and its expiry time (5 minutes)
            expiry = datetime.now() + timedelta(minutes=5)
            
            # Store the reset code in the verification_code field
            cursor.execute('''
                UPDATE users 
                SET verification_code = %s, code_expiry = %s
                WHERE email = %s
            ''', (reset_code, expiry, email))
            
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error saving reset code: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
            
    def verify_reset_code(self, email, code):
        """Verify a password reset code"""
        conn = self.connect()
        if not conn:
            return False
            
        cursor = conn.cursor()
        try:
            # Check if the code matches and hasn't expired
            cursor.execute('''
                SELECT COUNT(*) 
                FROM users 
                WHERE email = %s 
                AND verification_code = %s 
                AND code_expiry > NOW()
            ''', (email, code))
            
            count = cursor.fetchone()[0]
            return count > 0
        except Exception as e:
            print(f"Error verifying reset code: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def add_prescription(self, user_id, name, hospital_name, category_name, medicine_details):
        conn = self.connect()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            # Get or create category_id
            cursor.execute(
                "SELECT id FROM categories WHERE name = %s AND user_id = %s",
                (category_name, user_id)
            )
            category = cursor.fetchone()
            if category:
                category_id = category[0] if isinstance(category, tuple) else category['id']
            else:
                cursor.execute(
                    "INSERT INTO categories (user_id, name) VALUES (%s, %s)",
                    (user_id, category_name)
                )
                conn.commit()
                category_id = cursor.lastrowid

            # Insert prescription
            cursor.execute(
                """
                INSERT INTO prescriptions (created_at, name, user_id, hospital_name, category_id, medicine_details)
                VALUES (NOW(), %s, %s, %s, %s, %s)
                """,
                (name, user_id, hospital_name, category_id, json.dumps(medicine_details, ensure_ascii=False))
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding prescription: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def get_user_by_id(self, user_id):
        conn = self.connect()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching user by id: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def update_user_preferences(self, user_id, preferences_json):
        conn = self.connect()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE users SET preferences = %s WHERE id = %s", (preferences_json, user_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating user preferences: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def generate_today_notifications(self, user_id):
        conn = self.connect()
        if not conn:
            return
        cursor = conn.cursor(dictionary=True)
        today = datetime.now().date()
        try:
            prescriptions = self.get_user_prescriptions(user_id)
            for presc in prescriptions:
                presc_id = presc["id"]
                medicine_details = presc.get("medicine_details", {})
                if isinstance(medicine_details, str):
                    try:
                        medicine_details = json.loads(medicine_details)
                    except Exception:
                        medicine_details = {}
                created_at = presc.get("created_at")
                if isinstance(created_at, str):
                    created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                elif isinstance(created_at, datetime):
                    pass
                else:
                    continue

                # --- Group medicines by time_label for today ---
                time_groups = {}
                for med in medicine_details.get("medicines", []):
                    med_name = med.get("medicine_name", "")
                    qty = med.get("quantity_per_time", "")
                    usage_times = med.get("usage_time", [])
                    duration_days = int(''.join(filter(str.isdigit, str(med.get("duration_days", "1")))) or "1")
                    for t in usage_times:
                        if isinstance(t, dict):
                            time_label = t.get("time", "")
                        else:
                            time_label = t
                        # Calculate the valid days for this medicine
                        for day_offset in range(duration_days):
                            dose_date = created_at.date() + timedelta(days=day_offset)
                            if dose_date == today:
                                if time_label not in time_groups:
                                    time_groups[time_label] = []
                                time_groups[time_label].append({
                                    "medicine_name": med_name,
                                    "quantity_per_time": qty
                                })
                # Insert one notification per time_label
                for time_label, meds in time_groups.items():
                    # Check if notification already exists
                    cursor.execute("""
                        SELECT id FROM medicine_notifications
                        WHERE user_id=%s AND prescription_id=%s AND time_label=%s AND notify_date=%s
                    """, (user_id, presc_id, time_label, today))
                    if not cursor.fetchone():
                        cursor.execute("""
                            INSERT INTO medicine_notifications (user_id, prescription_id, medicines_json, time_label, notify_date)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (user_id, presc_id, json.dumps(meds, ensure_ascii=False), time_label, today))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def generate_notification_for_time(self, user_id, time_label):
        conn = self.connect()
        if not conn:
            return
        cursor = conn.cursor(dictionary=True)
        today = datetime.now().date()
        try:
            prescriptions = self.get_user_prescriptions(user_id)
            for presc in prescriptions:
                presc_id = presc["id"]
                medicine_details = presc.get("medicine_details", {})
                if isinstance(medicine_details, str):
                    try:
                        medicine_details = json.loads(medicine_details)
                    except Exception:
                        medicine_details = {}
                created_at = presc.get("created_at")
                if isinstance(created_at, str):
                    created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                elif isinstance(created_at, datetime):
                    pass
                else:
                    continue

                # Group medicines for this time_label and today
                meds = []
                for med in medicine_details.get("medicines", []):
                    med_name = med.get("medicine_name", "")
                    qty = med.get("quantity_per_time", "")
                    usage_times = med.get("usage_time", [])
                    duration_days = int(''.join(filter(str.isdigit, str(med.get("duration_days", "1")))) or "1")
                    for t in usage_times:
                        t_label = t.get("time", "") if isinstance(t, dict) else t
                        for day_offset in range(duration_days):
                            dose_date = created_at.date() + timedelta(days=day_offset)
                            if dose_date == today and t_label == time_label:
                                meds.append({
                                    "medicine_name": med_name,
                                    "quantity_per_time": qty
                                })
                if meds:
                    # Check if notification already exists
                    cursor.execute("""
                        SELECT id FROM medicine_notifications
                        WHERE user_id=%s AND prescription_id=%s AND time_label=%s AND notify_date=%s
                    """, (user_id, presc_id, time_label, today))
                    if not cursor.fetchone():
                        cursor.execute("""
                            INSERT INTO medicine_notifications (user_id, prescription_id, medicines_json, time_label, notify_date)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (user_id, presc_id, json.dumps(meds, ensure_ascii=False), time_label, today))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def get_today_notifications(self, user_id):
        conn = self.connect()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        today = datetime.now().date()
        try:
            cursor.execute("""
                SELECT n.*, p.name as prescription_name
                FROM medicine_notifications n
                JOIN prescriptions p ON n.prescription_id = p.id
                WHERE n.user_id=%s AND n.notify_date=%s
                ORDER BY n.time_label
            """, (user_id, today))
            notifications = cursor.fetchall()
            for n in notifications:
                n["medicines"] = json.loads(n.get("medicines_json", "[]"))
                n["time"] = n.get("time_label", "")  # Add this line for UI compatibility
            return notifications
        finally:
            cursor.close()
            conn.close()

    def mark_notification_taken(self, notification_id):
        """Mark a notification as taken and update status"""
        conn = self.connect()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE medicine_notifications
                SET taken=1, taken_at=NOW(), status='taken', updated_at=NOW()
                WHERE id=%s
            """, (notification_id,))
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    def mark_notification_untaken(self, notification_id):
        """Mark a notification as not taken (undo taken status)"""
        conn = self.connect()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE medicine_notifications
                SET taken=0, taken_at=NULL, status='pending', updated_at=NOW()
                WHERE id=%s
            """, (notification_id,))
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    def mark_missed_notifications(self, target_date=None):
        """Mark all pending notifications from previous days as missed"""
        conn = self.connect()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            if target_date is None:
                target_date = datetime.now().date()
            
            cursor.execute("""
                UPDATE medicine_notifications 
                SET status='missed', updated_at=NOW()
                WHERE notify_date < %s AND status='pending'
            """, (target_date,))
            
            affected_rows = cursor.rowcount
            conn.commit()
            print(f"Marked {affected_rows} notifications as missed for dates before {target_date}")
            return True
        except Exception as e:
            print(f"Error marking missed notifications: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def get_notification_status_for_date(self, user_id, prescription_id, time_label, date):
        """Get the status of a notification for a specific date and time"""
        conn = self.connect()
        if not conn:
            return 'none'  # No notification exists
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT status, taken, taken_at FROM medicine_notifications
                WHERE user_id=%s AND prescription_id=%s AND time_label=%s AND notify_date=%s
                LIMIT 1
            """, (user_id, prescription_id, time_label, date))
            
            result = cursor.fetchone()
            if not result:
                return 'none'  # No notification exists
            
            return result['status']
        finally:
            cursor.close()
            conn.close()

    def get_all_notification_statuses_for_date(self, user_id, date):
        """Get all notification statuses for a specific date"""
        conn = self.connect()
        if not conn:
            return {}
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT prescription_id, time_label, status, taken, taken_at 
                FROM medicine_notifications
                WHERE user_id=%s AND notify_date=%s
            """, (user_id, date))
            
            results = cursor.fetchall()
            statuses = {}
            for result in results:
                key = (result['prescription_id'], result['time_label'])
                statuses[key] = result['status']
            
            return statuses
        finally:
            cursor.close()
            conn.close()

    def is_time_taken(self, user_id, prescription_id, time_label, date):
        """Check if a specific time slot is marked as taken"""
        conn = self.connect()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT COUNT(*) FROM medicine_notifications
                WHERE user_id=%s AND prescription_id=%s AND time_label=%s AND notify_date=%s AND status='taken'
            """, (user_id, prescription_id, time_label, date))
            taken_count = cursor.fetchone()[0]
            return taken_count > 0
        finally:
            cursor.close()
            conn.close()

    def cleanup_old_notifications(self):
        """Clean up old notifications and mark missed ones"""
        conn = self.connect()
        if not conn:
            return
        cursor = conn.cursor()
        today = datetime.now().date()
        try:
            # First mark pending notifications from previous days as missed
            cursor.execute("""
                UPDATE medicine_notifications 
                SET status='missed', updated_at=NOW()
                WHERE notify_date < %s AND status='pending'
            """, (today,))
            
            missed_count = cursor.rowcount
            
            # Optionally delete very old notifications (older than 30 days)
            old_date = today - timedelta(days=30)
            cursor.execute("DELETE FROM medicine_notifications WHERE notify_date < %s", (old_date,))
            
            deleted_count = cursor.rowcount
            conn.commit()
            
            print(f"Marked {missed_count} notifications as missed, deleted {deleted_count} old notifications")
        finally:
            cursor.close()
            conn.close()

    def get_incomplete_notifications(self, user_id, date):
        """Get incomplete (missed) notifications for a specific date"""
        conn = self.connect()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT * FROM medicine_notifications
                WHERE user_id=%s AND notify_date=%s AND status IN ('pending', 'missed')
            """, (user_id, date))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()