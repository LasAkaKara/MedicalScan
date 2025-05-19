#!/usr/bin/env python3
import json
import random
from datetime import datetime, timedelta
from services.database_service import DatabaseService

def generate_test_prescriptions(user_id=3, num_prescriptions=10):
    """Generate test prescription data for a user"""
    db = DatabaseService()
    
    # Test categories
    categories = [
        'Bệnh mãn tính',
        'Điều trị cấp tính',
        'Thực phẩm chức năng',
        'Thuốc định kỳ',
        'Thuốc đau dạ dày'
    ]
    
    # Ensure categories exist
    category_ids = {}
    for category_name in categories:
        # Check if category exists
        cursor = db.connect().cursor(dictionary=True)
        cursor.execute("SELECT id FROM categories WHERE name = %s AND user_id = %s", 
                      (category_name, user_id))
        result = cursor.fetchone()
        if result:
            category_ids[category_name] = result['id']
        else:
            # Create the category
            cursor.execute("INSERT INTO categories (user_id, name) VALUES (%s, %s)",
                          (user_id, category_name))
            category_ids[category_name] = cursor.lastrowid
        cursor.close()
    
    # Test medicine names and info
    medicines = [
        {"name": "Paracetamol 500mg", "info": "Giảm đau, hạ sốt"},
        {"name": "Amoxicillin 500mg", "info": "Kháng sinh điều trị nhiễm khuẩn"},
        {"name": "Omeprazole 20mg", "info": "Thuốc điều trị đau dạ dày"},
        {"name": "Vitamin C 1000mg", "info": "Tăng cường miễn dịch"},
        {"name": "Cetirizine 10mg", "info": "Thuốc kháng histamine"},
        {"name": "Loratadine 10mg", "info": "Thuốc chống dị ứng"},
        {"name": "Aspirin 81mg", "info": "Chống đông máu"},
        {"name": "Metformin 500mg", "info": "Thuốc điều trị tiểu đường"},
        {"name": "Atorvastatin 10mg", "info": "Thuốc giảm cholesterol"},
        {"name": "Losartan 50mg", "info": "Thuốc điều trị huyết áp cao"}
    ]
    
    # Test hospital names
    hospitals = [
        "Bệnh viện Đa khoa Trung ương",
        "Bệnh viện Bạch Mai",
        "Bệnh viện Chợ Rẫy",
        "Bệnh viện 108",
        "Bệnh viện Đại học Y Dược",
        "Bệnh viện Từ Dũ",
        "Bệnh viện Nhi Đồng",
        "Bệnh viện Việt Đức",
        "Phòng khám Đa khoa Quốc tế",
        "Bệnh viện Quân Y 175"
    ]
    
    # Test usage times
    usage_times = [
        ["sáng"],
        ["sáng", "tối"],
        ["sáng", "trưa", "tối"],
        ["sáng", "trưa", "chiều", "tối"],
        ["trước khi ăn sáng", "trước khi ăn tối"],
        ["sau khi ăn sáng", "sau khi ăn tối"],
        ["8:00", "20:00"],
        ["7:00", "15:00", "23:00"]
    ]
    
    # Test usage instructions
    usage_instructions = [
        "Uống với nhiều nước",
        "Uống sau khi ăn",
        "Uống trước khi ăn 30 phút",
        "Ngậm dưới lưỡi",
        "Hòa với nước ấm uống",
        "Không uống cùng sữa",
        "Uống vào buổi sáng",
        "Uống trước khi đi ngủ",
        "Tránh đồ uống có cồn",
        "Có thể uống cùng thức ăn"
    ]
    
    # Generate test data
    prescription_names = [
        "Điều trị viêm họng",
        "Điều trị đau dạ dày",
        "Thuốc bổ sung vitamin",
        "Điều trị cao huyết áp",
        "Thuốc chống dị ứng",
        "Điều trị nhiễm trùng",
        "Đơn thuốc tiểu đường",
        "Điều trị cảm cúm",
        "Thuốc giảm đau",
        "Thuốc rối loạn tiêu hóa",
        "Đơn thuốc tái khám",
        "Thuốc chăm sóc sau phẫu thuật"
    ]
    
    prescriptions = []
    now = datetime.now()
    
    for i in range(num_prescriptions):
        # Create date in the past (up to 1 year ago)
        days_ago = random.randint(0, 365)
        created_at = now - timedelta(days=days_ago)
        
        # Select random elements
        prescription_name = random.choice(prescription_names)
        hospital_name = random.choice(hospitals)
        category_name = random.choice(categories)
        
        # Create 1-5 medicines for this prescription
        num_medicines = random.randint(1, 5)
        prescription_medicines = []
        
        for j in range(num_medicines):
            medicine = random.choice(medicines)
            usage_time = random.choice(usage_times)
            quantity_per_time = random.randint(1, 3)
            duration_days = random.randint(3, 30)
            
            prescription_medicines.append({
                "medicine_name": medicine["name"],
                "medicine_info": medicine["info"],
                "usage_time": usage_time,
                "quantity_per_time": quantity_per_time,
                "total_quantity": quantity_per_time * len(usage_time) * duration_days,
                "usage_instruction": random.choice(usage_instructions),
                "duration_days": duration_days
            })
        
        # Create the prescription data
        medicine_details = {
            "medicines": prescription_medicines,
            "total_medicines": len(prescription_medicines)
        }
        
        prescription = {
            "created_at": created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "name": f"{prescription_name} #{i+1}",
            "user_id": user_id,
            "hospital_name": hospital_name,
            "category_id": category_ids[category_name],
            "medicine_details": json.dumps(medicine_details)
        }
        
        prescriptions.append(prescription)
    
    # Insert into database
    conn = db.connect()
    cursor = conn.cursor()
    
    try:
        for p in prescriptions:
            cursor.execute("""
                INSERT INTO prescriptions 
                (created_at, name, user_id, hospital_name, category_id, medicine_details)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                p["created_at"],
                p["name"],
                p["user_id"],
                p["hospital_name"],
                p["category_id"],
                p["medicine_details"]
            ))
        
        conn.commit()
        print(f"Successfully inserted {len(prescriptions)} test prescriptions")
    except Exception as e:
        conn.rollback()
        print(f"Error inserting test data: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    user_id = 3  # Replace with desired user ID
    generate_test_prescriptions(user_id, 10)
    print("Test prescription data generated successfully!") 