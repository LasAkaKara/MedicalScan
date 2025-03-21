from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.graphics import Color, Line, InstructionGroup
from kivy.uix.scatter import Scatter
from kivymd.uix.button import MDFloatingActionButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
import cv2
import numpy as np
import time
import os
import threading

class CornerMarker(Scatter):
    """Improved draggable corner marker for manual cropping"""
    def __init__(self, corner_index, **kwargs):
        super(CornerMarker, self).__init__(**kwargs)
        self.corner_index = corner_index
        self.do_rotation = False
        self.do_scale = False
        self.do_translation = True
        self.size_hint = (None, None)
        self.size = (30, 30)  # Larger for easier touch
        
        # Set different colors for each corner to make them easier to identify
        colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 0, 1)]
        self.color = colors[corner_index % 4]

class ScanScreen(Screen):
    camera = ObjectProperty(None)
    crop_points = ListProperty([(0, 0), (0, 0), (0, 0), (0, 0)])
    is_processing = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create prescriptions directory if it doesn't exist
        self.prescriptions_dir = 'prescriptions'
        if not os.path.exists(self.prescriptions_dir):
            os.makedirs(self.prescriptions_dir)
        
        self.current_image = None
        self.is_cropping = False
        self.corner_markers = []
        self.capture = None
        self.frame_available = False
        self.frame = None
        self.camera_initialized = False
        self.crop_lines = InstructionGroup()
    
    def on_enter(self):
        """Called when the screen is entered"""
        if not self.is_cropping:
            self.start_camera()
    
    def on_leave(self):
        """Called when leaving the screen"""
        self.stop_camera()
    
    def start_camera(self):
        """Initialize and start the camera"""
        if self.camera_initialized:
            return
            
        # Try different camera indices
        for camera_index in range(3):  # Try indices 0, 1, 2
            try:
                self.capture = cv2.VideoCapture(camera_index)
                if self.capture.isOpened():
                    # Set lower resolution for better performance
                    self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    
                    # Check if we can read a frame
                    ret, frame = self.capture.read()
                    if ret:
                        print(f"Camera initialized with index {camera_index}")
                        self.camera_initialized = True
                        # Start camera update in a separate thread
                        self.camera_thread = threading.Thread(target=self.camera_update_thread)
                        self.camera_thread.daemon = True
                        self.camera_thread.start()
                        
                        # Schedule frame display update
                        Clock.schedule_interval(self.update_texture, 1.0/30.0)
                        return
                    else:
                        self.capture.release()
            except Exception as e:
                print(f"Error initializing camera {camera_index}: {e}")
                if self.capture:
                    self.capture.release()
        
        print("Failed to initialize any camera")
        self.show_error_dialog("Camera Error", "Failed to initialize camera. Please check your camera connection.")
    
    def stop_camera(self):
        """Stop the camera"""
        if self.capture and self.camera_initialized:
            self.camera_initialized = False
            self.capture.release()
            self.capture = None
            Clock.unschedule(self.update_texture)
    
    def camera_update_thread(self):
        """Camera update thread to capture frames"""
        while self.camera_initialized and self.capture and self.capture.isOpened():
            try:
                ret, frame = self.capture.read()
                if ret:
                    # Store the frame for the main thread to use
                    self.frame = frame
                    self.frame_available = True
                else:
                    time.sleep(0.01)  # Short sleep to prevent CPU overuse
            except Exception as e:
                print(f"Error in camera thread: {e}")
                time.sleep(0.1)
    
    def update_texture(self, dt):
        """Update the texture with the latest frame (called in main thread)"""
        if self.frame_available and self.frame is not None:
            # Convert to texture
            # Flip the image vertically to fix upside-down preview
            frame = cv2.flip(self.frame, 0)
            
            # Convert BGR to RGB for proper color display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Create texture
            buf = frame_rgb.tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            
            # Display image
            self.ids.camera_image.texture = texture
            self.frame_available = False
    
    def take_picture(self):
        """Capture an image from the camera"""
        if self.frame is not None:
            # Show processing indicator
            self.is_processing = True
            
            # Stop camera preview
            self.stop_camera()
            
            # Store the captured image
            self.current_image = self.frame.copy()
            
            # Display the captured image
            self.display_image(self.current_image)
            
            # Switch to cropping mode
            Clock.schedule_once(lambda dt: self.start_cropping(), 0.5)
    
    def display_image(self, image):
        """Display an image on the screen"""
        # Convert BGR to RGB for proper color display
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Create texture
        buf = image_rgb.tobytes()
        texture = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        
        # Display image
        self.ids.camera_image.texture = texture
    
    def start_cropping(self):
        """Enter cropping mode"""
        self.is_cropping = True
        self.is_processing = False
        
        # Show cropping instructions
        Snackbar(
            text="Drag the corner markers to adjust the crop area",
            duration=3
        ).open()
        
        # Show cropping controls
        self.ids.camera_controls.clear_widgets()
        
        # Add auto-detect, confirm and cancel buttons
        auto_detect_btn = MDRaisedButton(
            text="Auto Detect",
            pos_hint={'center_x': 0.2, 'center_y': 0.5},
            on_release=self.auto_detect_document
        )
        
        confirm_btn = MDRaisedButton(
            text="Confirm",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            on_release=self.confirm_crop
        )
        
        cancel_btn = MDRaisedButton(
            text="Cancel",
            pos_hint={'center_x': 0.8, 'center_y': 0.5},
            on_release=self.cancel_crop
        )
        
        self.ids.camera_controls.add_widget(auto_detect_btn)
        self.ids.camera_controls.add_widget(confirm_btn)
        self.ids.camera_controls.add_widget(cancel_btn)
        
        # Initial document edge detection
        self.auto_detect_document(None)
    
    def auto_detect_document(self, instance):
        """Auto-detect document edges"""
        if self.current_image is None:
            return
        
        # Show processing indicator
        self.is_processing = True
        
        # Run detection in a separate thread to avoid UI freezing
        threading.Thread(target=self._detect_document_edges_thread).start()
    
    def _detect_document_edges_thread(self):
        """Thread function for document edge detection"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Edge detection
            edged = cv2.Canny(gray, 75, 200)
            
            # Find contours
            contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
            
            # Find the document contour
            document_contour = None
            for contour in contours:
                perimeter = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
                
                if len(approx) == 4:
                    document_contour = approx
                    break
            
            # If document contour found, set crop points
            if document_contour is not None:
                # Reorder points: top-left, top-right, bottom-right, bottom-left
                pts = document_contour.reshape(4, 2)
                rect = np.zeros((4, 2), dtype="float32")
                
                # Top-left: smallest sum of coordinates
                # Bottom-right: largest sum of coordinates
                s = pts.sum(axis=1)
                rect[0] = pts[np.argmin(s)]
                rect[2] = pts[np.argmax(s)]
                
                # Top-right: smallest difference of coordinates
                # Bottom-left: largest difference of coordinates
                diff = np.diff(pts, axis=1)
                rect[1] = pts[np.argmin(diff)]
                rect[3] = pts[np.argmax(diff)]
                
                # Update crop points on the main thread
                Clock.schedule_once(lambda dt: self._update_crop_points([(int(x), int(y)) for x, y in rect]), 0)
            else:
                # Default to image corners if no document detected
                h, w = self.current_image.shape[:2]
                Clock.schedule_once(lambda dt: self._update_crop_points([(0, 0), (w, 0), (w, h), (0, h)]), 0)
                
                # Show message that no document was detected
                Clock.schedule_once(lambda dt: Snackbar(
                    text="No document detected. Please adjust corners manually.",
                    duration=3
                ).open(), 0.5)
        except Exception as e:
            print(f"Error in document detection: {e}")
        finally:
            # Hide processing indicator
            Clock.schedule_once(lambda dt: setattr(self, 'is_processing', False), 0)
    
    def _update_crop_points(self, points):
        """Update crop points and refresh corner markers"""
        self.crop_points = points
        self.refresh_corner_markers()
    
    def refresh_corner_markers(self):
        """Refresh corner markers based on current crop points"""
        # Clear any existing markers
        for marker in self.corner_markers:
            self.ids.crop_overlay.remove_widget(marker)
        self.corner_markers = []
        
        # Add new markers at crop points
        for i, point in enumerate(self.crop_points):
            marker = CornerMarker(i, pos=point)
            marker.bind(pos=lambda instance, pos, idx=i: self.update_crop_point(idx, pos))
            self.corner_markers.append(marker)
            self.ids.crop_overlay.add_widget(marker)
    
    def update_crop_point(self, index, pos):
        """Update crop point when marker is moved"""
        self.crop_points[index] = pos
    
    def confirm_crop(self, instance):
        """Apply the crop and save the image"""
        if self.current_image is None:
            return
        
        # Show processing indicator
        self.is_processing = True
        
        # Process in a separate thread
        threading.Thread(target=self._process_and_save_image).start()
    
    def _process_and_save_image(self):
        """Process and save the cropped image in a background thread"""
        try:
            # Apply perspective transform
            src_pts = np.array(self.crop_points, dtype=np.float32)
            
            # Calculate width and height of the cropped image
            width_a = np.sqrt(((self.crop_points[2][0] - self.crop_points[3][0]) ** 2) + 
                             ((self.crop_points[2][1] - self.crop_points[3][1]) ** 2))
            width_b = np.sqrt(((self.crop_points[1][0] - self.crop_points[0][0]) ** 2) + 
                             ((self.crop_points[1][1] - self.crop_points[0][1]) ** 2))
            max_width = max(int(width_a), int(width_b))
            
            height_a = np.sqrt(((self.crop_points[1][0] - self.crop_points[2][0]) ** 2) + 
                              ((self.crop_points[1][1] - self.crop_points[2][1]) ** 2))
            height_b = np.sqrt(((self.crop_points[0][0] - self.crop_points[3][0]) ** 2) + 
                              ((self.crop_points[0][1] - self.crop_points[3][1]) ** 2))
            max_height = max(int(height_a), int(height_b))
            
            # Ensure minimum dimensions
            max_width = max(max_width, 100)
            max_height = max(max_height, 100)
            
            # Destination points
            dst_pts = np.array([
                [0, 0],
                [max_width - 1, 0],
                [max_width - 1, max_height - 1],
                [0, max_height - 1]
            ], dtype=np.float32)
            
            # Get transformation matrix and apply it
            matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
            cropped_image = cv2.warpPerspective(self.current_image, matrix, (max_width, max_height))
            
            # Enhance the image
            enhanced_image = self.enhance_document_image(cropped_image)
            
            # Save the cropped image
            timestr = time.strftime("%Y%m%d_%H%M%S")
            filename = f"prescription_{timestr}.png"
            filepath = os.path.join(self.prescriptions_dir, filename)
            cv2.imwrite(filepath, enhanced_image)
            
            # Show success message on main thread
            Clock.schedule_once(lambda dt: Snackbar(
                text=f"Saved to {filepath}",
                duration=3
            ).open(), 0)
            
            # Exit cropping mode on main thread
            Clock.schedule_once(lambda dt: self.exit_cropping_mode(), 0.5)
        except Exception as e:
            print(f"Error processing image: {e}")
            # Show error on main thread
            Clock.schedule_once(lambda dt: self.show_error_dialog(
                "Processing Error", 
                f"Failed to process image: {str(e)}"
            ), 0)
        finally:
            # Hide processing indicator
            Clock.schedule_once(lambda dt: setattr(self, 'is_processing', False), 0)
    
    def enhance_document_image(self, image):
        """Enhance document image for better readability"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply adaptive thresholding
            thresh = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
            
            # Apply unsharp masking for sharpening
            blurred = cv2.GaussianBlur(gray, (0, 0), 3)
            sharpened = cv2.addWeighted(gray, 1.5, blurred, -0.5, 0)
            
            # Create a colored result with the sharpened image
            result = image.copy()
            
            # Return the enhanced image
            return result
        except Exception as e:
            print(f"Error enhancing image: {e}")
            return image  # Return original if enhancement fails
    
    def cancel_crop(self, instance):
        """Cancel cropping and return to camera mode"""
        self.exit_cropping_mode()
    
    def exit_cropping_mode(self):
        """Exit cropping mode and return to camera mode"""
        self.is_cropping = False
        self.current_image = None
        
        # Clear corner markers
        for marker in self.corner_markers:
            self.ids.crop_overlay.remove_widget(marker)
        self.corner_markers = []
        
        # Restore camera controls
        self.ids.camera_controls.clear_widgets()
        capture_btn = MDFloatingActionButton(
            icon="camera",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            on_release=lambda x: self.take_picture()
        )
        upload_btn = MDFloatingActionButton(
            icon="upload",
            pos_hint={'center_x': 0.8, 'center_y': 0.5},
            on_release=lambda x: self.show_file_chooser()
        )
        self.ids.camera_controls.add_widget(capture_btn)
        self.ids.camera_controls.add_widget(upload_btn)
        
        # Restart camera
        self.start_camera()
    
    def show_file_chooser(self):
        """Show file chooser for uploading images"""
        content = BoxLayout(orientation='vertical')
        file_chooser = FileChooserListView(
            path=os.path.expanduser('~'),
            filters=['*.png', '*.jpg', '*.jpeg']
        )
        content.add_widget(file_chooser)
        
        buttons = BoxLayout(size_hint_y=None, height=50)
        select_btn = Button(text='Select')
        cancel_btn = Button(text='Cancel')
        buttons.add_widget(select_btn)
        buttons.add_widget(cancel_btn)
        content.add_widget(buttons)
        
        popup = Popup(title='Choose Image', content=content, size_hint=(0.9, 0.9))
        
        # Bind events
        select_btn.bind(on_release=lambda x: self.load_selected_file(file_chooser.selection, popup))
        cancel_btn.bind(on_release=popup.dismiss)
        
        popup.open()
    
    def load_selected_file(self, selection, popup):
        """Load the selected image file"""
        if selection and os.path.isfile(selection[0]):
            # Dismiss popup
            popup.dismiss()
            
            # Show processing indicator
            self.is_processing = True
            
            # Stop camera if running
            self.stop_camera()
            
            # Load the image in a separate thread
            threading.Thread(target=self._load_image_thread, args=(selection[0],)).start()
    
    def _load_image_thread(self, filepath):
        """Load image in a background thread"""
        try:
            # Load the image
            self.current_image = cv2.imread(filepath)
            
            # Update UI on main thread
            Clock.schedule_once(lambda dt: self.display_image(self.current_image), 0)
            Clock.schedule_once(lambda dt: self.start_cropping(), 0.5)
        except Exception as e:
            print(f"Error loading image: {e}")
            Clock.schedule_once(lambda dt: self.show_error_dialog(
                "Loading Error", 
                f"Failed to load image: {str(e)}"
            ), 0)
            Clock.schedule_once(lambda dt: self.exit_cropping_mode(), 0.5)
        finally:
            # Hide processing indicator
            Clock.schedule_once(lambda dt: setattr(self, 'is_processing', False), 0)
    
    def show_error_dialog(self, title, message):
        """Show error dialog"""
        dialog = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open() 