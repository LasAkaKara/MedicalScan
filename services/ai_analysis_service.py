import google.generativeai as genai
import json
import logging
import os
import re
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class AIAnalysisService:
    def __init__(self):
        """Initialize Gemini AI service"""
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                logger.error("GEMINI_API_KEY not found in environment variables")
                self.model = None
                return
                
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("Gemini AI initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini AI: {e}")
            self.model = None

    def analyze_prescription_text(self, extracted_text):
        """
        Analyze extracted text and convert to structured prescription data
        """
        if self.model is None:
            logger.error("AI model not initialized")
            return None
        
        if not extracted_text or len(extracted_text.strip()) < 10:
            logger.warning(f"Extracted text too short or empty: '{extracted_text}'")
            return None
        
        try:
            logger.info(f"Analyzing text of length: {len(extracted_text)}")
            
            # Pre-process text to improve analysis
            cleaned_text = self._preprocess_text(extracted_text)
            logger.debug(f"Cleaned text: {cleaned_text}")
            
            # Create enhanced prompt with medical context
            prompt = self._create_enhanced_analysis_prompt(cleaned_text)
            
            # Generate response with multiple attempts for better accuracy
            prescription_data = None
            for attempt in range(2):
                try:
                    response = self.model.generate_content(
                        prompt,
                        safety_settings=[
                            {
                                "category": "HARM_CATEGORY_HARASSMENT",
                                "threshold": "BLOCK_NONE"
                            },
                            {
                                "category": "HARM_CATEGORY_HATE_SPEECH",
                                "threshold": "BLOCK_NONE"
                            },
                            {
                                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                                "threshold": "BLOCK_NONE"
                            },
                            {
                                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                                "threshold": "BLOCK_NONE"
                            }
                        ]
                    )
                    
                    logger.info(f"Received response from Gemini AI (attempt {attempt + 1})")
                    logger.debug(f"AI Response: {response.text}")
                    
                    # Parse the response
                    prescription_data = self._parse_ai_response(response.text)
                    
                    if prescription_data and prescription_data.get("medicines"):
                        break
                        
                except Exception as e:
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    if attempt == 1:
                        raise e
            
            if prescription_data:
                # Post-process to improve accuracy
                prescription_data = self._post_process_prescription_data(prescription_data, cleaned_text)
                
                # DEBUG: Print the final data structure
                logger.info("=== FINAL PRESCRIPTION DATA ===")
                logger.info(f"Type: {type(prescription_data)}")
                logger.info(f"Keys: {list(prescription_data.keys()) if isinstance(prescription_data, dict) else 'Not a dict'}")
                
                # Print each field individually to debug
                for key, value in prescription_data.items():
                    logger.info(f"{key}: {type(value)} = {value}")
                    if key == "medicines" and isinstance(value, list):
                        for i, med in enumerate(value):
                            logger.info(f"  Medicine {i}: {type(med)} = {med}")
                            if isinstance(med, dict):
                                for med_key, med_value in med.items():
                                    logger.info(f"    {med_key}: {type(med_value)} = {med_value}")
                
                logger.info("Successfully analyzed prescription text")
            else:
                logger.warning("Failed to parse AI response into valid prescription data")
            
            return prescription_data
            
        except Exception as e:
            logger.error(f"Error analyzing prescription text: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _parse_ai_response(self, response_text):
        """Parse AI response and validate JSON structure"""
        try:
            # Clean the response text
            cleaned_text = response_text.strip()
            
            # Remove any markdown formatting
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.startswith('```'):
                cleaned_text = cleaned_text[3:]
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]
            
            cleaned_text = cleaned_text.strip()
            
            logger.debug(f"Cleaned AI response: {cleaned_text}")
            
            # Parse JSON
            prescription_data = json.loads(cleaned_text)
            
            # DEBUG: Check the parsed data
            logger.debug(f"Parsed JSON type: {type(prescription_data)}")
            logger.debug(f"Parsed JSON content: {prescription_data}")
            
            # Validate and clean the data
            validated_data = self._validate_prescription_data(prescription_data)
            
            return validated_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            logger.error(f"Response text: {response_text}")
            
            # Try to create a fallback response with basic structure
            return self._create_fallback_response()
            
        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")
            return None

    def _validate_prescription_data(self, data):
        """Validate and clean prescription data - ENSURE ALL VALUES ARE STRINGS"""
        try:
            # Ensure required structure exists with proper string conversion
            validated = {
                "patient_name": str(data.get("patient_name", "")) if data.get("patient_name") is not None else "",
                "doctor_name": str(data.get("doctor_name", "")) if data.get("doctor_name") is not None else "",
                "age": str(data.get("age", "")) if data.get("age") is not None else "",
                "weight": str(data.get("weight", "")) if data.get("weight") is not None else "",
                "gender": str(data.get("gender", "")) if data.get("gender") is not None else "",
                "diagnosis": str(data.get("diagnosis", "")) if data.get("diagnosis") is not None else "",
                "hospital_name": str(data.get("hospital_name", "")) if data.get("hospital_name") is not None else "",
                "prescription_date": str(data.get("prescription_date", "")) if data.get("prescription_date") is not None else "",
                "medicines": []
            }
            
            # Validate medicines
            medicines = data.get("medicines", [])
            if not isinstance(medicines, list):
                logger.warning(f"Medicines is not a list: {type(medicines)}")
                medicines = []
            
            for med in medicines:
                if isinstance(med, dict):
                    medicine_name = med.get("medicine_name")
                    if medicine_name is not None:
                        medicine_name = str(medicine_name).strip()
                    else:
                        medicine_name = ""
                    
                    # Only add medicine if it has a name
                    if medicine_name:
                        validated_med = {
                            "medicine_name": medicine_name,
                            "type": str(med.get("type", "Viên")) if med.get("type") is not None else "Viên",
                            "strength": str(med.get("strength", "")) if med.get("strength") is not None else "",
                            "total_quantity": str(med.get("total_quantity", "")) if med.get("total_quantity") is not None else "",
                            "quantity_per_time": str(med.get("quantity_per_time", "1 viên")) if med.get("quantity_per_time") is not None else "1 viên",
                            "duration_days": str(med.get("duration_days", "7")) if med.get("duration_days") is not None else "7",
                            "usage_instruction": str(med.get("usage_instruction", "")) if med.get("usage_instruction") is not None else "",
                            "usage_time": []
                        }
                        
                        # Validate usage_time
                        usage_times = med.get("usage_time", [])
                        if not isinstance(usage_times, list):
                            usage_times = []
                        
                        if not usage_times:
                            # Default usage time if none specified
                            usage_times = [{"time": "Sáng", "quantity": 1}]
                        
                        for usage in usage_times:
                            if isinstance(usage, dict):
                                time_label = usage.get("time", "")
                                if time_label is not None:
                                    time_label = str(time_label)
                                else:
                                    time_label = ""
                                
                                quantity = usage.get("quantity", 1)
                                
                                # Ensure Vietnamese time labels
                                if time_label.lower() in ["morning", "sáng"]:
                                    time_label = "Sáng"
                                elif time_label.lower() in ["noon", "afternoon", "trưa"]:
                                    time_label = "Trưa"
                                elif time_label.lower() in ["evening", "night", "tối"]:
                                    time_label = "Tối"
                                
                                if time_label in ["Sáng", "Trưa", "Tối"]:
                                    try:
                                        quantity_int = int(quantity) if str(quantity).isdigit() else 1
                                    except (ValueError, TypeError):
                                        quantity_int = 1
                                    
                                    validated_med["usage_time"].append({
                                        "time": time_label,
                                        "quantity": quantity_int
                                    })
                        
                        # Ensure at least one usage time
                        if not validated_med["usage_time"]:
                            validated_med["usage_time"] = [{"time": "Sáng", "quantity": 1}]
                        
                        validated["medicines"].append(validated_med)
                else:
                    logger.warning(f"Medicine is not a dict: {type(med)} = {med}")
            
            # If no medicines were extracted, add a placeholder
            if not validated["medicines"]:
                logger.warning("No medicines extracted, adding placeholder")
                validated["medicines"] = [
                    {
                        "medicine_name": "Thuốc được quét",
                        "type": "Viên",
                        "strength": "",
                        "total_quantity": "",
                        "quantity_per_time": "1 viên",
                        "duration_days": "7",
                        "usage_instruction": "",
                        "usage_time": [{"time": "Sáng", "quantity": 1}]
                    }
                ]
            
            # Final validation - ensure all values are properly serializable
            validated_json = json.dumps(validated, ensure_ascii=False)
            validated_parsed = json.loads(validated_json)
            
            logger.debug("Prescription data validation completed")
            logger.info(f"Validated {len(validated['medicines'])} medicines")
            return validated_parsed
            
        except Exception as e:
            logger.error(f"Error validating prescription data: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _preprocess_text(self, text):
        """Preprocess text to improve AI analysis accuracy"""
        # Remove excessive whitespace
        cleaned = re.sub(r'\s+', ' ', text.strip())
        
        # Fix common OCR errors for medical terms
        replacements = {
            # Common OCR mistakes
            '0': 'O',  # Zero to O in medicine names
            'l': 'I',  # lowercase l to uppercase I
            'rng': 'mg',  # common OCR error
            'rnl': 'ml',  # common OCR error
            'viên': 'viên',  # ensure Vietnamese characters
            'ngày': 'ngày',
            'lần': 'lần',
            'buổi': 'buổi',
        }
        
        for old, new in replacements.items():
            cleaned = cleaned.replace(old, new)
        
        # Standardize medical units
        cleaned = re.sub(r'(\d+)\s*(mg|ml|g|mcg|iu)', r'\1\2', cleaned, flags=re.IGNORECASE)
        
        return cleaned

    def _create_enhanced_analysis_prompt(self, text):
        """Create an enhanced prompt with medical context and examples"""
        
        prompt = f"""
You are an expert medical prescription analysis AI with deep knowledge of Vietnamese medical terminology and prescription formats.

CRITICAL INSTRUCTIONS:
1. Extract ALL information accurately, even if partially visible
2. For medicine names, be VERY careful about spelling and dosages
3. Look for patterns like "Tên thuốc + liều lượng + đơn vị" (e.g., "Paracetamol 500mg")
4. Vietnamese time indicators: "sáng" (morning), "trưa" (noon), "chiều/tối" (evening)
5. Quantity indicators: "viên" (tablet), "gói" (packet), "ml" (milliliter)
6. Duration indicators: "ngày" (days), "tuần" (weeks)

MEDICAL CONTEXT KNOWLEDGE:
- Common Vietnamese medicine names: Paracetamol, Amoxicillin, Omeprazole, Cetirizine, Vitamin C, Aspirin
- Common dosages: 250mg, 500mg, 1g, 10mg, 20mg
- Common instructions: "sau khi ăn" (after meals), "trước khi ăn" (before meals), "khi đói" (on empty stomach)

TEXT TO ANALYZE:
{text}

Extract information into this EXACT JSON format:

{{
    "patient_name": "Patient name (look for 'Bệnh nhân:', 'Tên:', 'Họ tên:' or similar)",
    "doctor_name": "Doctor name (look for 'Bác sĩ:', 'BS.', 'Dr.' or similar)", 
    "age": "Age in years (look for numbers + 'tuổi', 'năm', 'years')",
    "weight": "Weight (look for numbers + 'kg', 'kilos')",
    "gender": "Gender (Nam/Nữ/Male/Female)",
    "diagnosis": "Medical diagnosis or condition",
    "hospital_name": "Hospital/clinic name (usually at top of prescription)",
    "prescription_date": "Date in YYYY-MM-DD format if found",
    "medicines": [
        {{
            "medicine_name": "EXACT medicine name as written (be very careful with spelling)",
            "type": "Form (Viên/Tablet/Capsule/Syrup/Gói/etc)",
            "strength": "Dosage strength (e.g., 500mg, 10ml, 250mg)",
            "total_quantity": "Total amount prescribed",
            "quantity_per_time": "Amount per dose (e.g., '1 viên', '2 gói')",
            "duration_days": "Number of days (extract from 'X ngày' or calculate)",
            "usage_instruction": "Special instructions",
            "usage_time": [
                {{"time": "Sáng", "quantity": 1}},
                {{"time": "Trưa", "quantity": 1}},
                {{"time": "Tối", "quantity": 1}}
            ]
        }}
    ]
}}

EXTRACTION RULES:
1. Medicine names: Extract EXACTLY as written, including brand names and generic names
2. Dosages: Always include units (mg, ml, g, etc. )
3. Usage times: Convert to Vietnamese standard: Sáng, Trưa, Tối
4. Quantities: Be precise about "viên", "gói", "ml" etc.
5. If information is unclear, extract what you can see clearly
6. For usage_time, if you see "3 lần/ngày" distribute as Sáng, Trưa, Tối
7. If you see "2 lần/ngày" use Sáng and Tối
8. If you see "1 lần/ngày" use Sáng

RETURN ONLY THE JSON OBJECT, NO OTHER TEXT.
"""
        return prompt

    def _post_process_prescription_data(self, data, original_text):
        """Post-process prescription data to improve accuracy"""
        try:
            # Validate and correct medicine names against common patterns
            if "medicines" in data:
                for medicine in data["medicines"]:
                    # Correct common medicine name patterns
                    medicine_name = medicine.get("medicine_name", "")
                    medicine["medicine_name"] = self._correct_medicine_name(medicine_name, original_text)
                    
                    # Ensure proper dosage format
                    strength = medicine.get("strength", "")
                    medicine["strength"] = self._correct_dosage_format(strength)
                    
                    # Validate usage times
                    usage_times = medicine.get("usage_time", [])
                    medicine["usage_time"] = self._validate_usage_times(usage_times)
            
            # Improve hospital name extraction
            if not data.get("hospital_name") or data["hospital_name"] == "":
                data["hospital_name"] = self._extract_hospital_name(original_text)
            
            # Improve diagnosis extraction
            if not data.get("diagnosis") or data["diagnosis"] == "":
                data["diagnosis"] = self._extract_diagnosis(original_text)
            
            return data
            
        except Exception as e:
            logger.error(f"Error in post-processing: {e}")
            return data

    def _correct_medicine_name(self, name, original_text):
        """Correct common medicine name OCR errors"""
        if not name:
            return name
        
        # Common medicine name corrections
        corrections = {
            'Paracetarnol': 'Paracetamol',
            'Arnoxicillin': 'Amoxicillin',
            'Orneprazole': 'Omeprazole',
            'Cetirizine': 'Cetirizine',
            'Vitarnin': 'Vitamin',
            'Aspirln': 'Aspirin',
        }
        
        corrected_name = name
        for wrong, correct in corrections.items():
            if wrong.lower() in name.lower():
                corrected_name = name.replace(wrong, correct)
                break
        
        return corrected_name

    def _correct_dosage_format(self, strength):
        """Ensure proper dosage format"""
        if not strength:
            return strength
        
        # Standardize dosage units
        strength = re.sub(r'(\d+)\s*(mg|ml|g|mcg|iu)', r'\1\2', strength, flags=re.IGNORECASE)
        
        return strength

    def _validate_usage_times(self, usage_times):
        """Validate and correct usage times"""
        valid_times = ["Sáng", "Trưa", "Tối"]
        validated = []
        
        for usage in usage_times:
            if isinstance(usage, dict):
                time_label = usage.get("time", "")
                quantity = usage.get("quantity", 1)
                
                # Normalize time labels
                if time_label.lower() in ["morning", "sáng", "sang"]:
                    time_label = "Sáng"
                elif time_label.lower() in ["noon", "afternoon", "trưa", "trua"]:
                    time_label = "Trưa"
                elif time_label.lower() in ["evening", "night", "tối", "toi", "chiều"]:
                    time_label = "Tối"
                
                if time_label in valid_times:
                    validated.append({
                        "time": time_label,
                        "quantity": int(quantity) if str(quantity).isdigit() else 1
                    })
        
        # Ensure at least one usage time
        if not validated:
            validated = [{"time": "Sáng", "quantity": 1}]
        
        return validated

    def _extract_hospital_name(self, text):
        """Extract hospital name from text using patterns"""
        # Common hospital patterns
        patterns = [
            r'(Bệnh viện [^,\n]+)',
            r'(Phòng khám [^,\n]+)',
            r'(Trung tâm y tế [^,\n]+)',
            r'(Hospital [^,\n]+)',
            r'(Clinic [^,\n]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""

    def _extract_diagnosis(self, text):
        """Extract diagnosis from text using patterns"""
        # Common diagnosis patterns
        patterns = [
            r'Chẩn đoán[:\s]+([^,\n]+)',
            r'Diagnosis[:\s]+([^,\n]+)',
            r'Bệnh[:\s]+([^,\n]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""

    def analyze_prescription_text(self, extracted_text):
        """
        Analyze extracted text with enhanced medical context understanding
        """
        if self.model is None:
            logger.error("AI model not initialized")
            return None
        
        if not extracted_text or len(extracted_text.strip()) < 10:
            logger.warning(f"Extracted text too short or empty: '{extracted_text}'")
            return None
        
        try:
            logger.info(f"Analyzing text of length: {len(extracted_text)}")
            
            # Pre-process text to improve analysis
            cleaned_text = self._preprocess_text(extracted_text)
            logger.debug(f"Cleaned text: {cleaned_text}")
            
            # Create enhanced prompt with medical context
            prompt = self._create_enhanced_analysis_prompt(cleaned_text)
            
            # Generate response with multiple attempts for better accuracy
            prescription_data = None
            for attempt in range(2):
                try:
                    response = self.model.generate_content(
                        prompt,
                        safety_settings=[
                            {
                                "category": "HARM_CATEGORY_HARASSMENT",
                                "threshold": "BLOCK_NONE"
                            },
                            {
                                "category": "HARM_CATEGORY_HATE_SPEECH",
                                "threshold": "BLOCK_NONE"
                            },
                            {
                                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                                "threshold": "BLOCK_NONE"
                            },
                            {
                                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                                "threshold": "BLOCK_NONE"
                            }
                        ]
                    )
                    
                    logger.info(f"Received response from Gemini AI (attempt {attempt + 1})")
                    logger.debug(f"AI Response: {response.text}")
                    
                    # Parse the response
                    prescription_data = self._parse_ai_response(response.text)
                    
                    if prescription_data and prescription_data.get("medicines"):
                        break
                        
                except Exception as e:
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    if attempt == 1:
                        raise e
            
            if prescription_data:
                # Post-process to improve accuracy
                prescription_data = self._post_process_prescription_data(prescription_data, cleaned_text)
                
                # DEBUG: Print the final data structure
                logger.info("=== FINAL PRESCRIPTION DATA ===")
                logger.info(f"Type: {type(prescription_data)}")
                logger.info(f"Keys: {list(prescription_data.keys()) if isinstance(prescription_data, dict) else 'Not a dict'}")
                
                # Print each field individually to debug
                for key, value in prescription_data.items():
                    logger.info(f"{key}: {type(value)} = {value}")
                    if key == "medicines" and isinstance(value, list):
                        for i, med in enumerate(value):
                            logger.info(f"  Medicine {i}: {type(med)} = {med}")
                            if isinstance(med, dict):
                                for med_key, med_value in med.items():
                                    logger.info(f"    {med_key}: {type(med_value)} = {med_value}")
                
                logger.info("Successfully analyzed prescription text")
            else:
                logger.warning("Failed to parse AI response into valid prescription data")
            
            return prescription_data
            
        except Exception as e:
            logger.error(f"Error analyzing prescription text: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _create_analysis_prompt(self, text):
        """Create a detailed prompt for prescription analysis"""
        
        prompt = f"""
You are a medical prescription analysis AI. Analyze the following text extracted from a prescription image and extract ALL available information.

IMPORTANT: Even if some information is missing, extract whatever you can find. Do not leave the medicines array empty if there are any medicine names in the text.

Text to analyze:
{text}

Extract and structure the information into this JSON format. For missing information, use empty strings but ALWAYS try to extract medicine information:

{{
    "patient_name": "Patient name if found (look for names after 'Patient:', 'Bệnh nhân:', or similar)",
    "doctor_name": "Doctor name if found (look for names after 'Doctor:', 'Bác sĩ:', 'Dr.', or similar)", 
    "age": "Patient age if found (look for numbers followed by 'tuổi', 'years old', 'y/o')",
    "weight": "Patient weight if found (look for numbers followed by 'kg', 'kilos')",
    "gender": "Patient gender if found (Nam/Nữ/Male/Female)",
    "diagnosis": "Medical diagnosis or condition if found",
    "hospital_name": "Hospital, clinic, or medical facility name if found",
    "prescription_date": "Date of prescription if found (convert to YYYY-MM-DD format)",
    "medicines": [
        {{
            "medicine_name": "Name of the medicine (extract ANY medicine names you find)",
            "type": "Type if specified (Viên/Tablet/Capsule/Syrup/ml/mg/etc)",
            "strength": "Strength/dosage if found (e.g., 500mg, 10ml, 250mg)",
            "total_quantity": "Total quantity if found",
            "quantity_per_time": "How much to take each time if found",
            "duration_days": "How many days to take if found",
            "usage_instruction": "Any special instructions",
            "usage_time": [
                {{"time": "Sáng", "quantity": 1}},
                {{"time": "Trưa", "quantity": 1}},
                {{"time": "Tối", "quantity": 1}}
            ]
        }}
    ]
}}

CRITICAL INSTRUCTIONS:
1. ALWAYS extract medicine names even if other details are missing
2. Look for common medicine name patterns (ending in -in, -ol, -ate, -ine, etc. )
3. For usage_time, use Vietnamese: "Sáng" (morning), "Trưa" (noon), "Tối" (evening)
4. If you find "3 times daily" or similar, distribute across Sáng, Trưa, Tối
5. If you find "twice daily", use Sáng and Tối
6. If you find "once daily", use Sáng
7. Extract hospital/clinic names from headers or letterheads
8. Look for prescription names in titles or headers
9. Even partial information is valuable - extract what you can
10. If no specific medicines are found but there are drug-like words, include them

Return ONLY the JSON object, no additional text.
"""
        return prompt

    def _create_fallback_response(self):
        """Create a basic fallback response when AI parsing fails"""
        return {
            "patient_name": "",
            "doctor_name": "",
            "age": "",
            "weight": "",
            "gender": "",
            "diagnosis": "",
            "hospital_name": "Cơ sở y tế",
            "prescription_date": "",
            "medicines": [
                {
                    "medicine_name": "Thuốc được quét",
                    "type": "Viên",
                    "strength": "",
                    "total_quantity": "",
                    "quantity_per_time": "1 viên",
                    "duration_days": "7",
                    "usage_instruction": "",
                    "usage_time": [{"time": "Sáng", "quantity": 1}]
                }
            ]
        }