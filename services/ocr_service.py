import easyocr
import cv2
import numpy as np
import logging
from PIL import Image, ImageEnhance, ImageFilter
import io

logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self):
        """Initialize EasyOCR reader"""
        try:
            # Initialize EasyOCR with Vietnamese and English support
            self.reader = easyocr.Reader(['vi', 'en'], gpu=False)
            logger.info("EasyOCR initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize EasyOCR: {e}")
            self.reader = None

    def extract_text_from_image(self, image_path_or_array):
        """
        Extract text from image using multiple advanced preprocessing techniques
        """
        if self.reader is None:
            logger.error("OCR reader not initialized")
            return ""
        
        try:
            # Handle both file path and numpy array inputs
            if isinstance(image_path_or_array, str):
                image = cv2.imread(image_path_or_array)
                if image is None:
                    logger.error(f"Could not load image from path: {image_path_or_array}")
                    return ""
            else:
                image = image_path_or_array.copy()
            
            logger.info(f"Processing image with shape: {image.shape}")
            
            # Try multiple advanced preprocessing approaches
            extracted_texts = []
            
            # Approach 1: Original image with optimal size
            try:
                optimized_original = self._optimize_image_size(image)
                results = self.reader.readtext(optimized_original)
                text1 = self._extract_text_from_results(results, "Optimized Original")
                if text1:
                    extracted_texts.append(text1)
            except Exception as e:
                logger.warning(f"Failed to process optimized original: {e}")
            
            # Approach 2: Enhanced contrast and sharpness
            try:
                enhanced_image = self._enhance_image_quality(image)
                results = self.reader.readtext(enhanced_image)
                text2 = self._extract_text_from_results(results, "Enhanced Quality")
                if text2:
                    extracted_texts.append(text2)
            except Exception as e:
                logger.warning(f"Failed to process enhanced image: {e}")
            
            # Approach 3: Denoised and sharpened
            try:
                denoised_image = self._denoise_and_sharpen(image)
                results = self.reader.readtext(denoised_image)
                text3 = self._extract_text_from_results(results, "Denoised")
                if text3:
                    extracted_texts.append(text3)
            except Exception as e:
                logger.warning(f"Failed to process denoised image: {e}")
            
            # Approach 4: Adaptive threshold with morphology
            try:
                morphed_image = self._adaptive_threshold_with_morphology(image)
                results = self.reader.readtext(morphed_image)
                text4 = self._extract_text_from_results(results, "Morphological")
                if text4:
                    extracted_texts.append(text4)
            except Exception as e:
                logger.warning(f"Failed to process morphological image: {e}")
            
            # Approach 5: Perspective correction (if needed)
            try:
                corrected_image = self._correct_perspective(image)
                if corrected_image is not None:
                    results = self.reader.readtext(corrected_image)
                    text5 = self._extract_text_from_results(results, "Perspective Corrected")
                    if text5:
                        extracted_texts.append(text5)
            except Exception as e:
                logger.warning(f"Failed to process perspective corrected image: {e}")
            
            # Combine and deduplicate extracted texts
            if extracted_texts:
                final_text = self._combine_and_deduplicate_texts(extracted_texts)
                logger.info(f"Successfully extracted text: {len(final_text)} characters")
                logger.debug(f"Extracted text preview: {final_text[:200]}...")
                return final_text
            else:
                logger.warning("No text extracted from any preprocessing approach")
                return ""
            
        except Exception as e:
            logger.error(f"Error extracting text from image: {e}")
            return ""

    def _optimize_image_size(self, image):
        """Optimize image size for better OCR accuracy"""
        height, width = image.shape[:2]
        
        # Target size for optimal OCR (1500-2000 pixels on longer side)
        target_size = 1800
        
        if max(height, width) < target_size:
            # Upscale small images
            scale_factor = target_size / max(height, width)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
            logger.debug(f"Upscaled image to {new_width}x{new_height}")
        elif max(height, width) > target_size * 1.5:
            # Downscale very large images
            scale_factor = target_size / max(height, width)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            logger.debug(f"Downscaled image to {new_width}x{new_height}")
        
        return image

    def _enhance_image_quality(self, image):
        """Enhance image quality using PIL for better OCR"""
        try:
            # Convert OpenCV image to PIL
            if len(image.shape) == 3:
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                rgb_image = image
            
            pil_image = Image.fromarray(rgb_image)
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(pil_image)
            enhanced = enhancer.enhance(1.5)  # Increase contrast by 50%
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(enhanced)
            enhanced = enhancer.enhance(2.0)  # Increase sharpness significantly
            
            # Enhance brightness slightly
            enhancer = ImageEnhance.Brightness(enhanced)
            enhanced = enhancer.enhance(1.1)  # Slight brightness increase
            
            # Apply unsharp mask filter
            enhanced = enhanced.filter(ImageFilter.UnsharpMask(radius=1, percent=150, threshold=3))
            
            # Convert back to OpenCV format
            enhanced_cv = cv2.cvtColor(np.array(enhanced), cv2.COLOR_RGB2BGR)
            
            logger.debug("Enhanced image quality completed")
            return enhanced_cv
            
        except Exception as e:
            logger.error(f"Error enhancing image quality: {e}")
            return image

    def _denoise_and_sharpen(self, image):
        """Advanced denoising and sharpening"""
        try:
            # Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Apply Non-local Means Denoising
            denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
            
            # Apply Gaussian blur to reduce noise further
            blurred = cv2.GaussianBlur(denoised, (3, 3), 0)
            
            # Create unsharp mask for sharpening
            unsharp_mask = cv2.addWeighted(denoised, 1.5, blurred, -0.5, 0)
            
            # Apply adaptive histogram equalization
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(unsharp_mask)
            
            logger.debug("Denoising and sharpening completed")
            return enhanced
            
        except Exception as e:
            logger.error(f"Error in denoising and sharpening: {e}")
            return image

    def _adaptive_threshold_with_morphology(self, image):
        """Apply adaptive thresholding with morphological operations"""
        try:
            # Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Apply bilateral filter to reduce noise while preserving edges
            filtered = cv2.bilateralFilter(gray, 9, 75, 75)
            
            # Apply adaptive threshold
            thresh = cv2.adaptiveThreshold(
                filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
            
            # Morphological operations to clean up
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            
            # Remove noise
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
            
            # Fill gaps
            closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)
            
            logger.debug("Adaptive threshold with morphology completed")
            return closing
            
        except Exception as e:
            logger.error(f"Error in adaptive threshold with morphology: {e}")
            return image

    def _correct_perspective(self, image):
        """Attempt to correct perspective distortion"""
        try:
            # Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Edge detection
            edged = cv2.Canny(blurred, 75, 200)
            
            # Find contours
            contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
            
            # Find the largest rectangular contour
            for contour in contours:
                perimeter = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
                
                if len(approx) == 4:
                    # Found a quadrilateral, apply perspective transform
                    pts = approx.reshape(4, 2).astype(np.float32)
                    
                    # Order points: top-left, top-right, bottom-right, bottom-left
                    rect = self._order_points(pts)
                    
                    # Calculate dimensions of the new image
                    (tl, tr, br, bl) = rect
                    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
                    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
                    maxWidth = max(int(widthA), int(widthB))
                    
                    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
                    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
                    maxHeight = max(int(heightA), int(heightB))
                    
                    # Destination points
                    dst = np.array([
                        [0, 0],
                        [maxWidth - 1, 0],
                        [maxWidth - 1, maxHeight - 1],
                        [0, maxHeight - 1]
                    ], dtype=np.float32)
                    
                    # Apply perspective transform
                    M = cv2.getPerspectiveTransform(rect, dst)
                    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
                    
                    logger.debug("Perspective correction applied")
                    return warped
            
            # No suitable contour found
            return None
            
        except Exception as e:
            logger.error(f"Error in perspective correction: {e}")
            return None

    def _order_points(self, pts):
        """Order points in the order: top-left, top-right, bottom-right, bottom-left"""
        rect = np.zeros((4, 2), dtype=np.float32)
        
        # Sum and difference of coordinates
        s = pts.sum(axis=1)
        diff = np.diff(pts, axis=1)
        
        # Top-left: smallest sum
        rect[0] = pts[np.argmin(s)]
        # Bottom-right: largest sum
        rect[2] = pts[np.argmax(s)]
        # Top-right: smallest difference
        rect[1] = pts[np.argmin(diff)]
        # Bottom-left: largest difference
        rect[3] = pts[np.argmax(diff)]
        
        return rect

    def _combine_and_deduplicate_texts(self, texts):
        """Combine multiple extracted texts and remove duplicates intelligently"""
        # Combine all texts
        all_words = []
        for text in texts:
            words = text.split()
            all_words.extend(words)
        
        # Remove duplicates while preserving order and context
        seen = set()
        unique_words = []
        
        for word in all_words:
            # Clean word for comparison
            clean_word = word.lower().strip('.,!?;:')
            
            # Only add if we haven't seen this word or if it's a number/medicine name
            if clean_word not in seen or self._is_important_word(word):
                unique_words.append(word)
                seen.add(clean_word)
        
        return ' '.join(unique_words)

    def _is_important_word(self, word):
        """Check if a word is important enough to keep duplicates"""
        # Keep numbers, medicine-like words, and medical terms
        if word.isdigit():
            return True
        if any(suffix in word.lower() for suffix in ['mg', 'ml', 'g', 'mcg', 'iu']):
            return True
        if any(suffix in word.lower() for suffix in ['ine', 'ate', 'ide', 'ole', 'cin']):
            return True
        return False

    def _extract_text_from_results(self, results, method_name):
        """Extract text from EasyOCR results with improved confidence handling"""
        extracted_text = []
        for (bbox, text, confidence) in results:
            # Dynamic confidence threshold based on text characteristics
            min_confidence = 0.1
            
            # Higher confidence required for single characters
            if len(text.strip()) == 1:
                min_confidence = 0.3
            # Lower confidence for longer medical terms
            elif len(text.strip()) > 8:
                min_confidence = 0.05
            
            if confidence > min_confidence:
                cleaned_text = text.strip()
                if cleaned_text and len(cleaned_text) > 0:
                    extracted_text.append(cleaned_text)
                    logger.debug(f"{method_name} - Extracted: '{cleaned_text}' (confidence: {confidence:.2f})")
        
        full_text = ' '.join(extracted_text)
        logger.info(f"{method_name} extracted {len(extracted_text)} text segments, {len(full_text)} characters")
        return full_text

    def preprocess_image_for_ocr(self, image):
        """
        Enhanced preprocessing for better OCR accuracy
        """
        try:
            # Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Resize if too small (OCR works better on larger images)
            height, width = gray.shape
            if height < 1000 or width < 1000:
                scale_factor = max(1000 / height, 1000 / width)
                new_width = int(width * scale_factor)
                new_height = int(height * scale_factor)
                gray = cv2.resize(gray, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
                logger.debug(f"Resized image from {width}x{height} to {new_width}x{new_height}")
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            
            # Apply adaptive thresholding
            thresh = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
            
            # Apply morphological operations to clean up
            kernel = np.ones((2, 2), np.uint8)
            cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            logger.debug("Standard preprocessing completed")
            return cleaned
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            return image

    def _create_high_contrast_image(self, image):
        """Create a high contrast version of the image"""
        try:
            # Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            enhanced = clahe.apply(gray)
            
            # Apply binary threshold
            _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            logger.debug("High contrast preprocessing completed")
            return binary
            
        except Exception as e:
            logger.error(f"Error creating high contrast image: {e}")
            return image