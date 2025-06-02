# from kivy.uix.screenmanager import Screen
# from kivy.properties import ObjectProperty, ListProperty, BooleanProperty, NumericProperty
# from kivy.clock import Clock
# from kivy.graphics.texture import Texture
# from kivy.uix.image import Image
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.filechooser import FileChooserListView
# from kivy.uix.popup import Popup
# from kivy.uix.button import Button
# from kivy.graphics import Color, Line, InstructionGroup
# from kivy.uix.scatter import Scatter
# from kivymd.uix.button import MDFloatingActionButton, MDRaisedButton
# from kivymd.uix.dialog import MDDialog
# from kivymd.uix.snackbar import MDSnackbar
# from kivymd.uix.label import MDLabel
# from kivy.core.window import Window
# from kivy.metrics import dp
# import cv2
# import numpy as np
# import time
# import os
# import threading
# import logging

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# class CornerMarker(Scatter):
#     """Improved draggable corner marker for manual cropping"""
#     def __init__(self, corner_index=0, **kwargs):
#         super(CornerMarker, self).__init__(**kwargs)
#         self.corner_index = corner_index
#         self.do_rotation = False
#         self.do_scale = False
#         self.do_translation = True
#         self.size_hint = (None, None)
#         self.size = (30, 30)  # Larger for easier touch
        
#         # Set different colors for each corner to make them easier to identify
#         colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 0, 1)]
#         self.color = colors[corner_index % 4]

#     def on_touch_down(self, touch):
#         if self.collide_point(*touch.pos):
#             touch.grab(self)
#             return True
#         return super().on_touch_down(touch)

#     def on_touch_move(self, touch):
#         if touch.grab_current is self:
#             self.pos = (touch.x - self.width/2, touch.y - self.height/2)
#             # Update crop points in parent
#             if self.parent and hasattr(self.parent.parent, 'update_crop_point'):
#                 marker_id = self.id.replace('_', '')  # Convert 'top_left' to 'topleft'
#                 self.parent.parent.update_crop_point(marker_id, touch.pos)
#             return True
#         return super().on_touch_move(touch)

#     def on_touch_up(self, touch):
#         if touch.grab_current is self:
#             touch.ungrab(self)
#             return True
#         return super().on_touch_up(touch)


# class ScanScreen(Screen):
#     camera = ObjectProperty(None)
#     crop_points = ListProperty([(0, 0), (0, 0), (0, 0), (0, 0)])
#     is_processing = BooleanProperty(False)
#     is_cropping = BooleanProperty(False)
#     has_image = BooleanProperty(False)
#     rotation_angle = NumericProperty(0)
    
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         logger.debug("Initializing ScanScreen")
#         # Create prescriptions directory if it doesn't exist
#         self.prescriptions_dir = 'prescriptions'
#         if not os.path.exists(self.prescriptions_dir):
#             os.makedirs(self.prescriptions_dir)
        
#         self.current_image = None
#         self.corner_markers = []
#         self.capture = None
#         self.frame_available = False
#         self.frame = None
#         self.camera_initialized = False
#         self.crop_lines = InstructionGroup()
#         self.texture = None
#         self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
#         if self._keyboard:
#             self._keyboard.bind(on_key_down=self._on_key_down)
#         self.original_image = None
#         self.rotation_angle = 180  # Set initial rotation to 180 degrees
        
#         # Don't start camera here, wait for on_enter
    
#     def _on_keyboard_closed(self):
#         self._keyboard.unbind(on_key_down=self._on_key_down)
#         self._keyboard = None

#     def _on_key_down(self, keyboard, keycode, text, modifiers):
#         if keycode[1] == 'r':  # Press 'r' to rotate
#             self.rotate_image()
#         return True

#     def on_enter(self):
#         """Called when the screen is entered"""
#         logger.debug("Entering ScanScreen")
#         if not self.is_cropping and not self.camera_initialized:
#             # Use a small delay to ensure UI is fully loaded
#             Clock.schedule_once(self.start_camera, 0.5)
    
#     def on_leave(self):
#         """Called when leaving the screen"""
#         logger.debug("Leaving ScanScreen")
#         self.stop_camera()
    
#     def start_camera(self, dt=None):
#         """Initialize and start the camera"""
#         logger.debug("Starting camera initialization")
#         if self.camera_initialized:
#             logger.debug("Camera already initialized")
#             return
            
#         # Try to get camera settings
#         resolution_width = 640
#         resolution_height = 480
        
#         try:
#             from views.screens.python.settings_screen import SettingsScreen
#             settings = next((screen for screen in self.manager.screens if isinstance(screen, SettingsScreen)), None)
            
#             if settings and settings.camera_resolution:
#                 resolution_parts = settings.camera_resolution.split('x')
#                 if len(resolution_parts) == 2:
#                     resolution_width = int(resolution_parts[0])
#                     resolution_height = int(resolution_parts[1])
#         except Exception as e:
#             logger.warning(f"Could not get camera resolution settings: {e}")
            
#         # Try with DirectShow first on Windows (best compatibility)
#         try:
#             logger.debug("Trying camera with DirectShow backend")
#             self.capture = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
#             if self.capture.isOpened():
#                 # Set camera properties
#                 self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, resolution_width)
#                 self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution_height)
#                 self.capture.set(cv2.CAP_PROP_FPS, 30)
#                 self.capture.set(cv2.CAP_PROP_AUTOFOCUS, 1)
#                 self.capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Auto exposure
                
#                 # Check if we can read a frame
#                 ret, frame = self.capture.read()
#                 if ret:
#                     logger.debug("Successfully initialized camera with DirectShow")
#                     self.camera_initialized = True
#                     # Start camera update in a separate thread
#                     self.camera_thread = threading.Thread(target=self.camera_update_thread)
#                     self.camera_thread.daemon = True
#                     self.camera_thread.start()
                    
#                     # Schedule frame display update
#                     Clock.schedule_interval(self.update_texture, 1.0/30.0)
#                     return
#                 else:
#                     logger.warning("Could not read frame from camera")
#                     self.capture.release()
#             else:
#                 logger.warning("Could not open camera with DirectShow")
#         except Exception as e:
#             logger.error(f"Error initializing camera with DirectShow: {e}")
#             if self.capture:
#                 self.capture.release()
        
#         # Fallback to trying different camera indices with different backends
#         for camera_index in range(2):  # Try indices 0, 1
#             try:
#                 logger.debug(f"Fallback: Trying camera index: {camera_index}")
#                 # Try different backends (MSMF on Windows, V4L on Linux)
#                 self.capture = cv2.VideoCapture(camera_index)
#                 if self.capture.isOpened():
#                     # Set camera properties
#                     self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#                     self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#                     self.capture.set(cv2.CAP_PROP_FPS, 30)
                    
#                     # Check if we can read a frame
#                     ret, frame = self.capture.read()
#                     if ret:
#                         logger.debug(f"Successfully initialized camera with index {camera_index}")
#                         self.camera_initialized = True
#                         # Start camera update in a separate thread
#                         self.camera_thread = threading.Thread(target=self.camera_update_thread)
#                         self.camera_thread.daemon = True
#                         self.camera_thread.start()
                        
#                         # Schedule frame display update
#                         Clock.schedule_interval(self.update_texture, 1.0/30.0)
#                         return
#                     else:
#                         logger.warning(f"Could not read frame from camera {camera_index}")
#                         self.capture.release()
#                 else:
#                     logger.warning(f"Could not open camera {camera_index}")
#             except Exception as e:
#                 logger.error(f"Error initializing camera {camera_index}: {e}")
#                 if self.capture:
#                     self.capture.release()
        
#         logger.error("Failed to initialize any camera")
#         self.show_error_dialog("Camera Error", "Failed to initialize camera. Please check your camera connection.")
    
#     def stop_camera(self):
#         """Stop the camera"""
#         logger.debug("Stopping camera")
#         if self.capture and self.camera_initialized:
#             self.camera_initialized = False
#             self.capture.release()
#             self.capture = None
#             Clock.unschedule(self.update_texture)
    
#     def camera_update_thread(self):
#         """Camera update thread to capture frames"""
#         logger.debug("Starting camera update thread")
#         # Set a flag to keep track of consecutive failures
#         consecutive_failures = 0
        
#         while self.camera_initialized and self.capture and self.capture.isOpened():
#             try:
#                 ret, frame = self.capture.read()
#                 if ret and frame is not None and frame.size > 0:
#                     # Reset failure count on success
#                     consecutive_failures = 0
#                     # Store the frame for the main thread to use
#                     self.frame = frame
#                     self.frame_available = True
#                     # Small sleep to prevent flooding the queue
#                     time.sleep(0.01)
#                 else:
#                     logger.warning(f"Failed to read frame from camera, ret={ret}")
#                     consecutive_failures += 1
                    
#                     # Only try to reinitialize after several consecutive failures
#                     if consecutive_failures > 5:
#                         logger.error(f"Multiple consecutive failures: {consecutive_failures}")
#                         # Try to reinitialize the camera
#                         if self.capture:
#                             self.capture.release()
#                             self.capture = None
                        
#                         try:
#                             self.capture = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
#                             # Reset count if we successfully reopen
#                             if self.capture and self.capture.isOpened():
#                                 consecutive_failures = 0
#                                 logger.info("Camera successfully reinitialized")
#                             else:
#                                 logger.error("Failed to reinitialize camera")
#                                 break
#                         except Exception as e:
#                             logger.error(f"Error reinitializing camera: {e}")
#                             break
                    
#                     time.sleep(0.1)  # Wait before trying again
#             except Exception as e:
#                 logger.error(f"Error in camera thread: {e}")
#                 consecutive_failures += 1
#                 if consecutive_failures > 10:
#                     logger.error("Too many errors, stopping camera thread")
#                     break
#                 time.sleep(0.1)
        
#         logger.debug("Camera update thread exiting")
#         Clock.schedule_once(lambda dt: self.handle_camera_failure(), 0)
    
#     def update_texture(self, dt):
#         """Update the texture with the latest frame (called in main thread)"""
#         if self.frame_available and self.frame is not None:
#             try:
#                 # Create a copy to avoid race conditions
#                 if self.frame.size == 0:
#                     logger.warning("Empty frame received, skipping texture update")
#                     self.frame_available = False
#                     return
                
#                 frame_copy = self.frame.copy()
                
#                 # Convert BGR to RGB for proper color display
#                 try:
#                     frame_rgb = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB)
#                 except cv2.error as e:
#                     logger.warning(f"Failed to convert frame colors: {e}")
#                     self.frame_available = False
#                     return
                
#                 # Apply rotation (180 degrees)
#                 frame_rgb = cv2.rotate(frame_rgb, cv2.ROTATE_180)
                
#                 # Apply camera settings if available
#                 try:
#                     from views.screens.python.settings_screen import SettingsScreen
#                     settings = next((screen for screen in self.manager.screens if isinstance(screen, SettingsScreen)), None)
                    
#                     if settings:
#                         # Apply horizontal flip if enabled
#                         if settings.camera_flip_horizontal:
#                             frame_rgb = cv2.flip(frame_rgb, 1)
                        
#                         # Apply vertical flip if enabled
#                         if settings.camera_flip_vertical:
#                             frame_rgb = cv2.flip(frame_rgb, 0)
#                 except Exception as e:
#                     logger.warning(f"Could not apply camera settings: {e}")
                
#                 # Create texture
#                 buf = frame_rgb.tobytes()
#                 texture = Texture.create(size=(frame_rgb.shape[1], frame_rgb.shape[0]), colorfmt='rgb')
#                 texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
                
#                 # Display image
#                 if hasattr(self, 'ids') and 'camera_image' in self.ids:
#                     self.ids.camera_image.texture = texture
#                     self.ids.camera_image.canvas.ask_update()
#                     # Log only occasionally for debugging
#                     if hasattr(self, '_log_counter'):
#                         self._log_counter += 1
#                         if self._log_counter % 30 == 0:  # Log every ~30 frames (~1 second)
#                             logger.debug("Camera texture updated successfully")
#                     else:
#                         self._log_counter = 0
#                         logger.debug("First camera texture update")
#                 else:
#                     logger.warning("Camera image widget not found in ids")
#                 self.frame_available = False
#             except Exception as e:
#                 logger.error(f"Error updating texture: {e}")
#                 import traceback
#                 logger.error(traceback.format_exc())
    
#     def take_picture(self):
#         """Capture an image from the camera"""
#         logger.debug("Taking picture")
#         if self.frame is not None:
#             # Show processing indicator
#             self.is_processing = True
            
#             # Stop camera preview
#             self.stop_camera()
            
#             # Store the captured image
#             # Deep copy to avoid race conditions
#             self.current_image = self.frame.copy()
            
#             # Apply 180 degree rotation (consistent with preview)
#             self.current_image = cv2.rotate(self.current_image, cv2.ROTATE_180)
            
#             # Apply camera settings from settings screen
#             try:
#                 from views.screens.python.settings_screen import SettingsScreen
#                 settings = next((screen for screen in self.manager.screens if isinstance(screen, SettingsScreen)), None)
                
#                 if settings:
#                     # Apply horizontal flip if enabled
#                     if settings.camera_flip_horizontal:
#                         self.current_image = cv2.flip(self.current_image, 1)
                    
#                     # Apply vertical flip if enabled
#                     if settings.camera_flip_vertical:
#                         self.current_image = cv2.flip(self.current_image, 0)
#             except Exception as e:
#                 logger.warning(f"Could not apply camera settings to captured image: {e}")
            
#             # Display the captured image
#             self.display_image(self.current_image)
            
#             # Switch to cropping mode
#             Clock.schedule_once(lambda dt: self.start_cropping(), 0.5)
    
#     def display_image(self, image):
#         """Display an image on the screen"""
#         try:
#             logger.debug("Displaying image")
#             if image is None or image.size == 0:
#                 logger.error("Cannot display empty image")
#                 return
            
#             # Make a deep copy to avoid modifying the original
#             display_img = image.copy()
            
#             # Convert BGR to RGB for proper color display
#             # This is required because OpenCV uses BGR and Kivy expects RGB
#             image_rgb = cv2.cvtColor(display_img, cv2.COLOR_BGR2RGB)
            
#             # Create texture
#             buf = image_rgb.tobytes()
#             texture = Texture.create(size=(image_rgb.shape[1], image_rgb.shape[0]), colorfmt='rgb')
#             texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            
#             # Display image
#             if hasattr(self, 'ids') and 'camera_image' in self.ids:
#                 logger.debug("Updating display image texture")
#                 self.ids.camera_image.texture = texture
#                 self.ids.camera_image.canvas.ask_update()
#             else:
#                 logger.warning("Camera image widget not found in ids")
#         except Exception as e:
#             logger.error(f"Error displaying image: {e}")
#             import traceback
#             logger.error(traceback.format_exc())
    
#     def start_cropping(self):
#         """Enter cropping mode"""
#         logger.debug("Starting cropping mode")
#         self.is_cropping = True
#         self.is_processing = False
        
#         # Show cropping instructions
#         MDSnackbar(
#             MDLabel(text="Drag the corner markers to adjust the crop area"),
#             duration=3
#         ).open()
        
#         # Show cropping controls
#         self.ids.camera_controls.clear_widgets()
        
#         # Add auto-detect, confirm and cancel buttons
#         auto_detect_btn = MDRaisedButton(
#             text="Auto Detect",
#             pos_hint={'center_x': 0.2, 'center_y': 0.5},
#             on_release=self.auto_detect_document
#         )
        
#         confirm_btn = MDRaisedButton(
#             text="Confirm",
#             pos_hint={'center_x': 0.5, 'center_y': 0.5},
#             on_release=self.confirm_crop
#         )
        
#         cancel_btn = MDRaisedButton(
#             text="Cancel",
#             pos_hint={'center_x': 0.8, 'center_y': 0.5},
#             on_release=self.cancel_crop
#         )
        
#         self.ids.camera_controls.add_widget(auto_detect_btn)
#         self.ids.camera_controls.add_widget(confirm_btn)
#         self.ids.camera_controls.add_widget(cancel_btn)
        
#         # Initial document edge detection
#         self.auto_detect_document(None)
    
#     def auto_detect_document(self, instance):
#         """Auto-detect document edges"""
#         if self.current_image is None:
#             return
        
#         # Show processing indicator
#         self.is_processing = True
        
#         # Run detection in a separate thread to avoid UI freezing
#         threading.Thread(target=self._detect_document_edges_thread).start()
    
#     def _detect_document_edges_thread(self):
#         """Thread function for document edge detection"""
#         try:
#             logger.debug("Starting document edge detection")
#             # Convert to grayscale
#             gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
#             gray = cv2.GaussianBlur(gray, (5, 5), 0)
            
#             # Edge detection
#             edged = cv2.Canny(gray, 75, 200)
            
#             # Find contours
#             contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#             contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
            
#             # Find the document contour
#             document_contour = None
#             for contour in contours:
#                 perimeter = cv2.arcLength(contour, True)
#                 approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
                
#                 if len(approx) == 4:
#                     document_contour = approx
#                     break
            
#             # If document contour found, set crop points
#             if document_contour is not None:
#                 # Reorder points: top-left, top-right, bottom-right, bottom-left
#                 pts = document_contour.reshape(4, 2)
#                 rect = np.zeros((4, 2), dtype="float32")
                
#                 # Top-left: smallest sum of coordinates
#                 # Bottom-right: largest sum of coordinates
#                 s = pts.sum(axis=1)
#                 rect[0] = pts[np.argmin(s)]
#                 rect[2] = pts[np.argmax(s)]
                
#                 # Top-right: smallest difference of coordinates
#                 # Bottom-left: largest difference of coordinates
#                 diff = np.diff(pts, axis=1)
#                 rect[1] = pts[np.argmin(diff)]
#                 rect[3] = pts[np.argmax(diff)]
                
#                 # Update crop points on the main thread
#                 Clock.schedule_once(lambda dt: self._update_crop_points([(int(x), int(y)) for x, y in rect]), 0)
#             else:
#                 # Default to image corners if no document detected
#                 h, w = self.current_image.shape[:2]
#                 Clock.schedule_once(lambda dt: self._update_crop_points([(0, 0), (w, 0), (w, h), (0, h)]), 0)
                
#                 # Show message that no document was detected
#                 Clock.schedule_once(lambda dt: MDSnackbar(
#                     MDLabel(text="No document detected. Please adjust corners manually."),
#                     duration=3
#                 ).open(), 0.5)
#         except Exception as e:
#             logger.error(f"Error in document detection: {e}")
#             self.is_processing = False
#             self.show_error_dialog("Detection Error", "Failed to detect document edges. Please try again.")
#         finally:
#             # Hide processing indicator
#             Clock.schedule_once(lambda dt: setattr(self, 'is_processing', False), 0)
    
#     def _update_crop_points(self, points):
#         """Update crop points and refresh corner markers"""
#         logger.debug(f"Updating crop points to: {points}")
#         # Make sure points are integers and within image boundaries
#         valid_points = []
#         if self.current_image is not None:
#             h, w = self.current_image.shape[:2]
#             for x, y in points:
#                 # Ensure points are within image boundaries
#                 x = max(0, min(int(x), w-1))
#                 y = max(0, min(int(y), h-1))
#                 valid_points.append((x, y))
#         else:
#             valid_points = [(int(x), int(y)) for x, y in points]
        
#         self.crop_points = valid_points
#         self.refresh_corner_markers()
    
#     def refresh_corner_markers(self):
#         """Refresh corner markers based on current crop points"""
#         # Clear any existing markers
#         for marker in self.corner_markers:
#             if marker.parent:
#                 self.ids.crop_overlay.remove_widget(marker)
#         self.corner_markers = []
        
#         # Add new markers at crop points
#         for i, point in enumerate(self.crop_points):
#             try:
#                 marker = CornerMarker(i, pos=point)
#                 marker.bind(pos=lambda instance, pos, idx=i: self.update_crop_point(idx, pos))
#                 self.corner_markers.append(marker)
#                 self.ids.crop_overlay.add_widget(marker)
#                 logger.debug(f"Added corner marker {i} at position {point}")
#             except Exception as e:
#                 logger.error(f"Error adding corner marker: {e}")
#                 import traceback
#                 logger.error(traceback.format_exc())
    
#     def update_crop_point(self, index, pos):
#         """Update crop point when marker is moved"""
#         self.crop_points[index] = pos
    
#     def confirm_crop(self, instance):
#         """Apply the crop and save the image"""
#         if self.current_image is None:
#             return
        
#         # Show processing indicator
#         self.is_processing = True
        
#         # Process in a separate thread
#         threading.Thread(target=self._process_and_save_image).start()
    
#     def _process_and_save_image(self):
#         """Process and save the cropped image in a background thread"""
#         try:
#             logger.debug("Starting image processing")
#             # Apply perspective transform
#             src_pts = np.array(self.crop_points, dtype=np.float32)
            
#             # Calculate width and height of the cropped image
#             width_a = np.sqrt(((self.crop_points[2][0] - self.crop_points[3][0]) ** 2) + 
#                              ((self.crop_points[2][1] - self.crop_points[3][1]) ** 2))
#             width_b = np.sqrt(((self.crop_points[1][0] - self.crop_points[0][0]) ** 2) + 
#                              ((self.crop_points[1][1] - self.crop_points[0][1]) ** 2))
#             max_width = max(int(width_a), int(width_b))
            
#             height_a = np.sqrt(((self.crop_points[1][0] - self.crop_points[2][0]) ** 2) + 
#                               ((self.crop_points[1][1] - self.crop_points[2][1]) ** 2))
#             height_b = np.sqrt(((self.crop_points[0][0] - self.crop_points[3][0]) ** 2) + 
#                               ((self.crop_points[0][1] - self.crop_points[3][1]) ** 2))
#             max_height = max(int(height_a), int(height_b))
            
#             # Ensure minimum dimensions
#             max_width = max(max_width, 100)
#             max_height = max(max_height, 100)
            
#             # Destination points
#             dst_pts = np.array([
#                 [0, 0],
#                 [max_width - 1, 0],
#                 [max_width - 1, max_height - 1],
#                 [0, max_height - 1]
#             ], dtype=np.float32)
            
#             # Get transformation matrix and apply it
#             matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
#             cropped_image = cv2.warpPerspective(self.current_image, matrix, (max_width, max_height))
            
#             # Enhance the image
#             enhanced_image = self.enhance_document_image(cropped_image)
            
#             # Save the cropped image
#             timestr = time.strftime("%Y%m%d_%H%M%S")
#             filename = f"prescription_{timestr}.png"
#             filepath = os.path.join(self.prescriptions_dir, filename)
#             cv2.imwrite(filepath, enhanced_image)
            
#             # Show success message on main thread
#             Clock.schedule_once(lambda dt: MDSnackbar(
#                 MDLabel(text=f"Saved to {filepath}"),
#                 duration=3
#             ).open(), 0)
            
#             # Exit cropping mode on main thread
#             Clock.schedule_once(lambda dt: self.exit_cropping_mode(), 0.5)
#         except Exception as e:
#             logger.error(f"Error processing image: {e}")
#             # Show error on main thread
#             Clock.schedule_once(lambda dt: self.show_error_dialog(
#                 "Processing Error", 
#                 f"Failed to process image: {str(e)}"
#             ), 0)
#         finally:
#             # Hide processing indicator
#             Clock.schedule_once(lambda dt: setattr(self, 'is_processing', False), 0)
    
#     def enhance_document_image(self, image):
#         """Enhance document image for better readability"""
#         try:
#             logger.debug("Starting image enhancement")
#             # Convert to grayscale
#             gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
#             # Apply adaptive thresholding
#             thresh = cv2.adaptiveThreshold(
#                 gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
#                 cv2.THRESH_BINARY, 11, 2
#             )
            
#             # Apply unsharp masking for sharpening
#             blurred = cv2.GaussianBlur(gray, (0, 0), 3)
#             sharpened = cv2.addWeighted(gray, 1.5, blurred, -0.5, 0)
            
#             # Create a colored result with the sharpened image
#             result = image.copy()
            
#             # Return the enhanced image
#             return result
#         except Exception as e:
#             logger.error(f"Error enhancing image: {e}")
#             return image  # Return original if enhancement fails
    
#     def cancel_crop(self, instance):
#         """Cancel cropping and return to camera mode"""
#         self.exit_cropping_mode()
    
#     def exit_cropping_mode(self):
#         """Exit cropping mode and return to camera mode"""
#         self.is_cropping = False
#         self.current_image = None
        
#         # Clear corner markers
#         for marker in self.corner_markers:
#             self.ids.crop_overlay.remove_widget(marker)
#         self.corner_markers = []
        
#         # Restore camera controls
#         self.ids.camera_controls.clear_widgets()
#         capture_btn = MDFloatingActionButton(
#             icon="camera",
#             pos_hint={'center_x': 0.5, 'center_y': 0.5},
#             on_release=lambda x: self.take_picture()
#         )
#         upload_btn = MDFloatingActionButton(
#             icon="upload",
#             pos_hint={'center_x': 0.8, 'center_y': 0.5},
#             on_release=lambda x: self.show_file_chooser()
#         )
#         self.ids.camera_controls.add_widget(capture_btn)
#         self.ids.camera_controls.add_widget(upload_btn)
        
#         # Restart camera
#         self.start_camera()
    
#     def show_file_chooser(self):
#         """Show file chooser for uploading images"""
#         content = BoxLayout(orientation='vertical')
#         file_chooser = FileChooserListView(
#             path=os.path.expanduser('~'),
#             filters=['*.png', '*.jpg', '*.jpeg']
#         )
#         content.add_widget(file_chooser)
        
#         buttons = BoxLayout(size_hint_y=None, height=50)
#         select_btn = Button(text='Select')
#         cancel_btn = Button(text='Cancel')
#         buttons.add_widget(select_btn)
#         buttons.add_widget(cancel_btn)
#         content.add_widget(buttons)
        
#         popup = Popup(title='Choose Image', content=content, size_hint=(0.9, 0.9))
        
#         # Bind events
#         select_btn.bind(on_release=lambda x: self.load_selected_file(file_chooser.selection, popup))
#         cancel_btn.bind(on_release=popup.dismiss)
        
#         popup.open()
    
#     def load_selected_file(self, selection, popup):
#         """Load the selected image file"""
#         if selection and os.path.isfile(selection[0]):
#             # Dismiss popup
#             popup.dismiss()
            
#             # Show processing indicator
#             self.is_processing = True
            
#             # Stop camera if running
#             self.stop_camera()
            
#             # Load the image in a separate thread
#             threading.Thread(target=self._load_image_thread, args=(selection[0],)).start()
    
#     def _load_image_thread(self, filepath):
#         """Load image in a background thread"""
#         try:
#             # Load the image
#             self.current_image = cv2.imread(filepath)
            
#             # Update UI on main thread
#             Clock.schedule_once(lambda dt: self.display_image(self.current_image), 0)
#             Clock.schedule_once(lambda dt: self.start_cropping(), 0.5)
#         except Exception as e:
#             logger.error(f"Error loading image: {e}")
#             Clock.schedule_once(lambda dt: self.show_error_dialog(
#                 "Loading Error", 
#                 f"Failed to load image: {str(e)}"
#             ), 0)
#             Clock.schedule_once(lambda dt: self.exit_cropping_mode(), 0.5)
#         finally:
#             # Hide processing indicator
#             Clock.schedule_once(lambda dt: setattr(self, 'is_processing', False), 0)
    
#     def show_error_dialog(self, title, message):
#         """Show error dialog"""
#         dialog = MDDialog(
#             title=title,
#             text=message,
#             buttons=[
#                 MDRaisedButton(
#                     text="OK",
#                     on_release=lambda x: dialog.dismiss()
#                 )
#             ]
#         )
#         dialog.open()
    
#     def handle_camera_failure(self):
#         """Handle camera thread failure"""
#         if self.camera_initialized:
#             logger.debug("Handling camera failure")
#             self.camera_initialized = False
#             # Notify user of camera issue
#             self.show_error_dialog("Camera Error", "Camera disconnected or not responding. Please try again.")

#     def toggle_crop_mode(self):
#         self.is_cropping = not self.is_cropping
#         if self.is_cropping and self.has_image:
#             # Initialize crop points to image corners
#             image = self.ids.camera_image
#             x, y = image.pos
#             w, h = image.size
#             self.crop_points = [
#                 (x + dp(20), y + dp(20)),           # Top-left
#                 (x + w - dp(20), y + dp(20)),       # Top-right
#                 (x + w - dp(20), y + h - dp(20)),   # Bottom-right
#                 (x + dp(20), y + h - dp(20))        # Bottom-left
#             ]

#     def rotate_image(self):
#         """Rotate the current image by 180 degrees"""
#         if self.current_image is not None:
#             logger.debug("Rotating image by 180 degrees")
#             # Rotate the current image
#             self.current_image = cv2.rotate(self.current_image, cv2.ROTATE_180)
            
#             # Update the display
#             self.display_image(self.current_image)
            
#             # If we have an original image, keep it in sync
#             if hasattr(self, 'original_image') and self.original_image is not None:
#                 self.original_image = cv2.rotate(self.original_image, cv2.ROTATE_180)

#     def apply_crop(self):
#         if self.has_image and self.is_cropping:
#             # Convert crop points to numpy array
#             pts = np.float32([[p[0], p[1]] for p in self.crop_points])
            
#             # Get image dimensions
#             image = self.ids.camera_image
#             w, h = image.size
            
#             # Define the output rectangle (destination points)
#             dst = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
            
#             # Calculate perspective transform matrix
#             M = cv2.getPerspectiveTransform(pts, dst)
            
#             # Apply perspective transform
#             if self.current_image is not None:
#                 warped = cv2.warpPerspective(self.current_image, M, (int(w), int(h)))
#                 self.current_image = warped
#                 # Update the display
#                 # You'll need to implement the logic to update the image display
            
#             # Exit crop mode
#             self.is_cropping = False 

import os
import cv2
import numpy as np
import time
import logging

from PySide6.QtCore import Signal, QTimer, Qt, QRect
from PySide6.QtWidgets import QMessageBox, QFileDialog
from PySide6.QtGui import QImage, QPixmap
from views.screens.pyside.scan_screen_ui import ScanScreenUI

logger = logging.getLogger(__name__)

class ScanScreen(ScanScreenUI):
    go_to_home = Signal()
    go_to_settings = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.back_btn.clicked.connect(self.handle_back_to_home)
        self.capture_btn.clicked.connect(self.handle_capture)
        self.upload_btn.clicked.connect(self.handle_upload)

        # Camera and image state
        self.camera_initialized = False
        self.capture = None
        self.frame = None
        self.camera_timer = QTimer(self)
        self.camera_timer.timeout.connect(self.update_camera_frame)
        self.current_image = None
        self.prescriptions_dir = 'prescriptions'
        os.makedirs(self.prescriptions_dir, exist_ok=True)
        
    # --- Navigation and UI state ---
    def handle_back_to_home(self):
        self.stop_camera()
        self.go_to_home.emit()

    def handle_settings(self):
        self.go_to_settings.emit()

    # --- Camera logic ---
    def start_camera(self):
        if self.camera_initialized:
            return
        self.capture = cv2.VideoCapture(0)
        if self.capture.isOpened():
            self.camera_initialized = True
            self.camera_timer.start(30)  # ~30 FPS
        else:
            QMessageBox.critical(self, "Camera Error", "Không thể khởi động camera.")

    def stop_camera(self):
        if self.camera_initialized and self.capture:
            self.camera_timer.stop()
            self.capture.release()
            self.capture = None
            self.camera_initialized = False

    def update_camera_frame(self):
        if self.capture and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret and frame is not None:
                self.frame = frame
                self.display_camera_frame(frame)
                self.capture_btn.setEnabled(True)
            else:
                self.capture_btn.setEnabled(False)
        else:
            self.capture_btn.setEnabled(False)

    def display_camera_frame(self, frame):
        # Flip the frame horizontally
        flipped = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qt_img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_img)
        self.camera_label.setPixmap(
            pixmap.scaled(
                self.camera_label.width(),
                self.camera_label.height(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
        )

    def display_image(self, image):
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qt_img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_img)
        self.camera_label.setPixmap(
            pixmap.scaled(
                self.camera_label.width(),
                self.camera_label.height(),
                Qt.KeepAspectRatioByExpanding,  # <-- This line changed
                Qt.SmoothTransformation
            )
        )

    # --- Capture and upload ---
    def handle_capture(self):
        if self.frame is not None:
            self.current_image = self.frame.copy()
            self.stop_camera()  # <--- Stop camera so preview doesn't overwrite
            self.display_image(self.current_image)
            self.enter_crop_mode()
        else:
            QMessageBox.warning(self, "Lỗi", "Không có khung hình để chụp.")
    
    def handle_recapture(self):
        self.show_capture_controls()
        self.camera_label.clear()
        self.current_image = None
        self.start_camera()

    def handle_upload(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn ảnh", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            image = cv2.imread(file_path)
            if image is not None:
                self.current_image = image
                self.stop_camera()  # <--- Stop camera so preview doesn't overwrite
                self.display_image(self.current_image)
                self.enter_crop_mode()
            else:
                QMessageBox.warning(self, "Lỗi", "Không thể mở ảnh.")

    # --- Crop mode ---
    def enter_crop_mode(self):
        self.show_crop_controls()
        # Resize overlay to match image label
        self.crop_overlay.setGeometry(self.camera_label.geometry())
        self.crop_overlay.raise_()
        self.crop_overlay.show()
        # Connect crop controls
        # self.crop_back_btn.clicked.connect(self.handle_recapture)
        self.rotate_btn.clicked.connect(self.handle_rotate)
        self.confirm_btn.clicked.connect(self.handle_confirm)

    def handle_auto_detect(self):
        if self.current_image is None:
            return
        # Auto-detect document edges and update crop rect
        rect = self.auto_detect_document(self.current_image)
        if rect is not None:
            # Map detected rect to overlay coordinates
            img_h, img_w = self.current_image.shape[:2]
            label_w, label_h = self.camera_label.width(), self.camera_label.height()
            scale_x = label_w / img_w
            scale_y = label_h / img_h
            x, y, w, h = rect
            overlay_rect = QRect(
                int(x * scale_x),
                int(y * scale_y),
                int(w * scale_x),
                int(h * scale_y)
            )
            self.crop_overlay.crop_rect = overlay_rect
            self.crop_overlay.update()
        else:
            QMessageBox.information(self, "Tự động", "Không phát hiện được tài liệu. Hãy điều chỉnh vùng cắt thủ công.")

    def auto_detect_document(self, image):
        # Simple rectangle detection (you can improve this)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 75, 200)
        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                return (x, y, w, h)
        # Fallback: full image
        h, w = image.shape[:2]
        return (0, 0, w, h)

    def handle_rotate(self):
        if self.current_image is not None:
            self.current_image = cv2.rotate(self.current_image, cv2.ROTATE_90_CLOCKWISE)
            self.display_image(self.current_image)
            # Reset crop overlay
            self.crop_overlay.crop_rect = QRect(60, 60, 200, 200)
            self.crop_overlay.update()

    def handle_confirm(self):
        if self.current_image is not None:
            rect = self.crop_overlay.get_crop_rect()
            # Map crop rect from overlay to image coordinates
            pixmap = self.camera_label.pixmap()
            if pixmap is None:
                QMessageBox.warning(self, "Lỗi", "Không có ảnh để cắt.")
                return
            label_w, label_h = self.camera_label.width(), self.camera_label.height()
            img_h, img_w = self.current_image.shape[:2]
            scale_x = img_w / label_w
            scale_y = img_h / label_h
            x = int(rect.x() * scale_x)
            y = int(rect.y() * scale_y)
            w = int(rect.width() * scale_x)
            h = int(rect.height() * scale_y)
            cropped = self.current_image[y:y+h, x:x+w]
            enhanced_image = self.enhance_document_image(cropped)
            timestr = time.strftime("%Y%m%d_%H%M%S")
            filename = f"prescription_{timestr}.png"
            filepath = os.path.join(self.prescriptions_dir, filename)
            cv2.imwrite(filepath, enhanced_image)
            QMessageBox.information(self, "Thành công", f"Đã lưu vào {filepath}")
            self.show_capture_controls()
            self.camera_label.clear()
            self.current_image = None

    def enhance_document_image(self, image):
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            thresh = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )
            blurred = cv2.GaussianBlur(gray, (0, 0), 3)
            sharpened = cv2.addWeighted(gray, 1.5, blurred, -0.5, 0)
            result = image.copy()
            return result
        except Exception as e:
            logger.error(f"Error enhancing image: {e}")
            return image

    # --- PySide6 widget events ---
    def showEvent(self, event):
        super().showEvent(event)
        self.start_camera()

    def hideEvent(self, event):
        super().hideEvent(event)
        self.stop_camera()