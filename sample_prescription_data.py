#!/usr/bin/env python3
import json
from datetime import datetime, timedelta
from services.database_service import DatabaseService

def insert_sample_prescriptions(user_id=3):
    """Insert predefined sample prescription data"""
    db = DatabaseService()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)
    
    # First, check if the user exists, and create it if not
    cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
    user_exists = cursor.fetchone()
    
    if not user_exists:
        print(f"User with ID {user_id} doesn't exist. Creating test user...")
        # Create a test user
        cursor.execute("""
            INSERT INTO users (id, email, password, is_verified, is_active, full_name)
            VALUES (%s, %s, %s, TRUE, TRUE, %s)
        """, (
            user_id,
            f"testuser{user_id}@example.com",
            db.hash_password("password123"),
            f"Test User {user_id}"
        ))
        conn.commit()
        print(f"Created test user with ID {user_id}")
    
    # Ensure categories exist
    categories = {
        'Bệnh mãn tính': None,
        'Điều trị cấp tính': None,
        'Thực phẩm chức năng': None,
        'Thuốc định kỳ': None
    }
    
    for category_name in categories:
        cursor.execute("SELECT id FROM categories WHERE name = %s AND user_id = %s", 
                      (category_name, user_id))
        result = cursor.fetchone()
        if result:
            categories[category_name] = result['id']
        else:
            cursor.execute("INSERT INTO categories (user_id, name) VALUES (%s, %s)",
                          (user_id, category_name))
            conn.commit()
            categories[category_name] = cursor.lastrowid
            print(f"Created category: {category_name}")
    
    # Create sample prescription data
    now = datetime.now()
    
    sample_prescriptions = [
        # Diabetes management prescription
        {
            "created_at": (now - timedelta(days=5)).strftime('%Y-%m-%d %H:%M:%S'),
            "name": "Điều trị đái tháo đường",
            "user_id": user_id,
            "hospital_name": "Bệnh viện Đa khoa Trung ương",
            "category_id": categories['Bệnh mãn tính'],
            "medicine_details": json.dumps({
                "medicines": [
                    {
                        "medicine_name": "Metformin 500mg",
                        "medicine_info": "Thuốc điều trị tiểu đường",
                        "usage_time": ["sáng", "tối"],
                        "quantity_per_time": 1,
                        "total_quantity": 60,
                        "usage_instruction": "Uống sau khi ăn",
                        "duration_days": 30
                    },
                    {
                        "medicine_name": "Gliclazide 60mg",
                        "medicine_info": "Thuốc kiểm soát đường huyết",
                        "usage_time": ["sáng"],
                        "quantity_per_time": 1,
                        "total_quantity": 30,
                        "usage_instruction": "Uống trước khi ăn sáng 30 phút",
                        "duration_days": 30
                    }
                ],
                "total_medicines": 2
            })
        },
        
        # Hypertension prescription
        {
            "created_at": (now - timedelta(days=15)).strftime('%Y-%m-%d %H:%M:%S'),
            "name": "Điều trị tăng huyết áp",
            "user_id": user_id,
            "hospital_name": "Bệnh viện Bạch Mai",
            "category_id": categories['Bệnh mãn tính'],
            "medicine_details": json.dumps({
                "medicines": [
                    {
                        "medicine_name": "Amlodipine 5mg",
                        "medicine_info": "Thuốc hạ huyết áp",
                        "usage_time": ["sáng"],
                        "quantity_per_time": 1,
                        "total_quantity": 30,
                        "usage_instruction": "Uống vào buổi sáng",
                        "duration_days": 30
                    },
                    {
                        "medicine_name": "Losartan 50mg",
                        "medicine_info": "Thuốc điều trị huyết áp cao",
                        "usage_time": ["tối"],
                        "quantity_per_time": 1,
                        "total_quantity": 30,
                        "usage_instruction": "Uống vào buổi tối trước khi đi ngủ",
                        "duration_days": 30
                    }
                ],
                "total_medicines": 2
            })
        },
        
        # Cold & flu prescription
        {
            "created_at": (now - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'),
            "name": "Điều trị cảm cúm",
            "user_id": user_id,
            "hospital_name": "Phòng khám Đa khoa Quốc tế",
            "category_id": categories['Điều trị cấp tính'],
            "medicine_details": json.dumps({
                "medicines": [
                    {
                        "medicine_name": "Paracetamol 500mg",
                        "medicine_info": "Giảm đau, hạ sốt",
                        "usage_time": ["sáng", "trưa", "tối"],
                        "quantity_per_time": 1,
                        "total_quantity": 15,
                        "usage_instruction": "Uống khi có triệu chứng sốt hoặc đau",
                        "duration_days": 5
                    },
                    {
                        "medicine_name": "Cetirizine 10mg",
                        "medicine_info": "Thuốc kháng histamine",
                        "usage_time": ["tối"],
                        "quantity_per_time": 1,
                        "total_quantity": 5,
                        "usage_instruction": "Uống trước khi đi ngủ",
                        "duration_days": 5
                    },
                    {
                        "medicine_name": "Ambroxol 30mg",
                        "medicine_info": "Thuốc long đờm",
                        "usage_time": ["sáng", "tối"],
                        "quantity_per_time": 1,
                        "total_quantity": 10,
                        "usage_instruction": "Uống sau khi ăn",
                        "duration_days": 5
                    }
                ],
                "total_medicines": 3
            })
        },
        
        # Vitamin supplement prescription
        {
            "created_at": (now - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'),
            "name": "Bổ sung vitamin",
            "user_id": user_id,
            "hospital_name": "Bệnh viện Đại học Y Dược",
            "category_id": categories['Thực phẩm chức năng'],
            "medicine_details": json.dumps({
                "medicines": [
                    {
                        "medicine_name": "Vitamin C 1000mg",
                        "medicine_info": "Tăng cường miễn dịch",
                        "usage_time": ["sáng"],
                        "quantity_per_time": 1,
                        "total_quantity": 30,
                        "usage_instruction": "Uống sau bữa sáng",
                        "duration_days": 30
                    },
                    {
                        "medicine_name": "Vitamin D3 2000IU",
                        "medicine_info": "Bổ sung vitamin D",
                        "usage_time": ["trưa"],
                        "quantity_per_time": 1,
                        "total_quantity": 30,
                        "usage_instruction": "Uống cùng bữa ăn có chất béo",
                        "duration_days": 30
                    },
                    {
                        "medicine_name": "Multivitamin",
                        "medicine_info": "Bổ sung đa vitamin và khoáng chất",
                        "usage_time": ["sáng"],
                        "quantity_per_time": 1,
                        "total_quantity": 30,
                        "usage_instruction": "Uống sau bữa sáng",
                        "duration_days": 30
                    }
                ],
                "total_medicines": 3
            })
        },
        
        # Gastrointestinal issue prescription
        {
            "created_at": (now - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S'),
            "name": "Điều trị đau dạ dày",
            "user_id": user_id,
            "hospital_name": "Bệnh viện 108",
            "category_id": categories['Điều trị cấp tính'],
            "medicine_details": json.dumps({
                "medicines": [
                    {
                        "medicine_name": "Omeprazole 20mg",
                        "medicine_info": "Thuốc điều trị đau dạ dày",
                        "usage_time": ["sáng", "tối"],
                        "quantity_per_time": 1,
                        "total_quantity": 28,
                        "usage_instruction": "Uống trước bữa ăn 30 phút",
                        "duration_days": 14
                    },
                    {
                        "medicine_name": "Domperidone 10mg",
                        "medicine_info": "Thuốc chống nôn và trào ngược",
                        "usage_time": ["sáng", "trưa", "tối"],
                        "quantity_per_time": 1,
                        "total_quantity": 42,
                        "usage_instruction": "Uống trước bữa ăn 15-30 phút",
                        "duration_days": 14
                    }
                ],
                "total_medicines": 2
            })
        }
    ]
    
    # Insert the prescriptions
    try:
        for prescription in sample_prescriptions:
            cursor.execute("""
                INSERT INTO prescriptions 
                (created_at, name, user_id, hospital_name, category_id, medicine_details)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                prescription["created_at"],
                prescription["name"],
                prescription["user_id"],
                prescription["hospital_name"],
                prescription["category_id"],
                prescription["medicine_details"]
            ))
        
        conn.commit()
        print(f"Successfully inserted {len(sample_prescriptions)} sample prescriptions")
    except Exception as e:
        conn.rollback()
        print(f"Error inserting sample data: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    user_id = 3  # Replace with desired user ID
    insert_sample_prescriptions(user_id)
    print("Sample prescription data created successfully!") 