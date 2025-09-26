#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install opencv-python pillow webcolors


# In[7]:


import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import webcolors
import threading
import colorsys

class ColorDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Python Color Detection Tool")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.cap = None
        self.is_camera_running = False
        self.current_image = None
        self.color_history = []
        self.current_color = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="🎨 Color Detection Tool", 
                              font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='#333')
        title_label.pack(pady=10)
        
        # Control Frame
        control_frame = tk.Frame(self.root, bg='#f0f0f0')
        control_frame.pack(pady=10)
        
        # Buttons
        self.start_camera_btn = tk.Button(control_frame, text="📹 Start Camera", 
                                         command=self.start_camera, font=('Arial', 12),
                                         bg='#4CAF50', fg='white', padx=20, pady=5)
        self.start_camera_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_camera_btn = tk.Button(control_frame, text="⏹️ Stop Camera", 
                                        command=self.stop_camera, font=('Arial', 12),
                                        bg='#f44336', fg='white', padx=20, pady=5,
                                        state=tk.DISABLED)
        self.stop_camera_btn.pack(side=tk.LEFT, padx=5)
        
        self.upload_btn = tk.Button(control_frame, text="📁 Upload Image", 
                                   command=self.upload_image, font=('Arial', 12),
                                   bg='#2196F3', fg='white', padx=20, pady=5)
        self.upload_btn.pack(side=tk.LEFT, padx=5)
        
        self.capture_color_btn = tk.Button(control_frame, text="🎯 Capture Color", 
                                          command=self.capture_current_color, font=('Arial', 12),
                                          bg='#FF9800', fg='white', padx=20, pady=5,
                                          state=tk.DISABLED)
        self.capture_color_btn.pack(side=tk.LEFT, padx=5)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left side - Image/Video display
        left_frame = tk.LabelFrame(main_frame, text="Image/Camera Feed", 
                                  font=('Arial', 12, 'bold'), bg='#f0f0f0')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Create a frame for the image with fixed size
        self.image_frame = tk.Frame(left_frame, bg='white', width=650, height=500)
        self.image_frame.pack(padx=10, pady=10)
        self.image_frame.pack_propagate(False)  # Maintain fixed size
        
        self.image_label = tk.Label(self.image_frame, text="No image loaded\nClick 'Start Camera' or 'Upload Image'",
                                   font=('Arial', 14), bg='white', fg='gray')
        self.image_label.place(relx=0.5, rely=0.5, anchor='center')  # Center the label
        self.image_label.bind("<Button-1>", self.on_image_click)
        
        # Instructions
        instruction_label = tk.Label(left_frame, 
                                   text="Camera Mode: Color detection at center crosshair\nImage Mode: Click anywhere to detect color",
                                   font=('Arial', 10), bg='#f0f0f0', fg='#666')
        instruction_label.pack(pady=(5, 10))
        
        # Right side - Color information
        right_frame = tk.LabelFrame(main_frame, text="Color Information", 
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0')
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Current color display
        color_display_frame = tk.Frame(right_frame, bg='#f0f0f0')
        color_display_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(color_display_frame, text="Current Color:", font=('Arial', 12, 'bold'),
                bg='#f0f0f0').pack()
        
        self.color_preview = tk.Label(color_display_frame, text="", width=20, height=3,
                                     relief=tk.RAISED, bg='white')
        self.color_preview.pack(pady=5)
        
        # Color values
        values_frame = tk.Frame(right_frame, bg='#f0f0f0')
        values_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.color_name_var = tk.StringVar(value="Color Name: -")
        self.rgb_var = tk.StringVar(value="RGB: -")
        self.hex_var = tk.StringVar(value="HEX: -")
        self.hsl_var = tk.StringVar(value="HSL: -")
        
        tk.Label(values_frame, textvariable=self.color_name_var, font=('Arial', 10, 'bold'),
                bg='#f0f0f0', anchor='w').pack(fill=tk.X, pady=2)
        tk.Label(values_frame, textvariable=self.rgb_var, font=('Arial', 10),
                bg='#f0f0f0', anchor='w').pack(fill=tk.X, pady=2)
        tk.Label(values_frame, textvariable=self.hex_var, font=('Arial', 10),
                bg='#f0f0f0', anchor='w').pack(fill=tk.X, pady=2)
        tk.Label(values_frame, textvariable=self.hsl_var, font=('Arial', 10),
                bg='#f0f0f0', anchor='w').pack(fill=tk.X, pady=2)
        
        # Color history
        history_frame = tk.LabelFrame(right_frame, text="Color History", 
                                     font=('Arial', 12, 'bold'), bg='#f0f0f0')
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Simple scrollable text widget for history
        history_container = tk.Frame(history_frame)
        history_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Text widget with scrollbar for history
        self.history_text = tk.Text(history_container, height=10, width=25, wrap=tk.WORD,
                                   font=('Arial', 9), bg='white', relief=tk.SUNKEN, bd=1)
        history_scrollbar = ttk.Scrollbar(history_container, orient="vertical", 
                                         command=self.history_text.yview)
        self.history_text.configure(yscrollcommand=history_scrollbar.set)
        
        self.history_text.pack(side="left", fill="both", expand=True)
        history_scrollbar.pack(side="right", fill="y")
        
        # Add initial message
        self.history_text.insert(tk.END, "Captured colors will appear here...\n\n")
        self.history_text.config(state=tk.DISABLED)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready - Choose camera or upload image")
        status_bar = tk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN,
                             anchor=tk.W, font=('Arial', 10), bg='#e0e0e0')
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def start_camera(self):
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Cannot access camera!")
                return
            
            self.is_camera_running = True
            self.start_camera_btn.config(state=tk.DISABLED)
            self.stop_camera_btn.config(state=tk.NORMAL)
            self.capture_color_btn.config(state=tk.NORMAL)
            self.status_var.set("Camera started - Color detection at center crosshair")
            
            # Start camera thread
            self.camera_thread = threading.Thread(target=self.update_camera, daemon=True)
            self.camera_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start camera: {str(e)}")
    
    def stop_camera(self):
        self.is_camera_running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        
        self.start_camera_btn.config(state=tk.NORMAL)
        self.stop_camera_btn.config(state=tk.DISABLED)
        self.capture_color_btn.config(state=tk.DISABLED)
        self.status_var.set("Camera stopped")
        self.image_label.config(image='', text="No image loaded\nClick 'Start Camera' or 'Upload Image'")
        self.image_label.place(relx=0.5, rely=0.5, anchor='center')
    
    def resize_image_maintain_aspect(self, pil_image, max_width, max_height):
        """Resize image while maintaining aspect ratio"""
        original_width, original_height = pil_image.size
        
        # Calculate aspect ratio
        aspect_ratio = original_width / original_height
        
        # Calculate new dimensions
        if aspect_ratio > max_width / max_height:
            # Image is wider, scale by width
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            # Image is taller, scale by height
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
        
        return pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    def update_camera(self):
        while self.is_camera_running:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Draw crosshair at center
            h, w = frame.shape[:2]
            center_x, center_y = w // 2, h // 2
            
            # Draw crosshair
            cv2.line(frame, (center_x - 15, center_y), (center_x + 15, center_y), (0, 255, 0), 2)
            cv2.line(frame, (center_x, center_y - 15), (center_x, center_y + 15), (0, 255, 0), 2)
            cv2.circle(frame, (center_x, center_y), 20, (0, 255, 0), 2)
            
            # Get color at center
            bgr_color = frame[center_y, center_x]
            rgb_color = tuple(reversed(bgr_color))  # Convert BGR to RGB
            
            # Update color information
            self.update_color_info(rgb_color)
            
            # Convert to display format
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            
            # Resize to fit the display area while maintaining aspect ratio
            display_width, display_height = 630, 480
            pil_image = self.resize_image_maintain_aspect(pil_image, display_width, display_height)
            photo = ImageTk.PhotoImage(pil_image)
            
            # Update display
            self.image_label.config(image=photo, text="")
            self.image_label.place(relx=0.5, rely=0.5, anchor='center')
            self.image_label.image = photo  # Keep reference
    
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")]
        )
        
        if file_path:
            try:
                # Stop camera if running
                if self.is_camera_running:
                    self.stop_camera()
                
                # Load and display image
                self.current_image = cv2.imread(file_path)
                if self.current_image is None:
                    messagebox.showerror("Error", "Failed to load image!")
                    return
                
                # Store original image dimensions for click coordinate conversion
                self.original_height, self.original_width = self.current_image.shape[:2]
                
                # Convert to RGB for display
                rgb_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(rgb_image)
                
                # Resize for display while maintaining aspect ratio
                display_width, display_height = 630, 480
                self.display_image = self.resize_image_maintain_aspect(pil_image, display_width, display_height)
                self.display_width, self.display_height = self.display_image.size
                
                photo = ImageTk.PhotoImage(self.display_image)
                
                self.image_label.config(image=photo, text="")
                self.image_label.place(relx=0.5, rely=0.5, anchor='center')
                self.image_label.image = photo
                
                self.capture_color_btn.config(state=tk.NORMAL)
                self.status_var.set("Image loaded - Click anywhere on image to detect color")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def on_image_click(self, event):
        if self.current_image is None or self.is_camera_running:
            return
        
        try:
            # Calculate scaling factors between displayed image and original image
            scale_x = self.original_width / self.display_width
            scale_y = self.original_height / self.display_height
            
            # Get click coordinates relative to the image label
            label_width = self.image_label.winfo_width()
            label_height = self.image_label.winfo_height()
            
            # Calculate offset from center (since image is centered)
            x_offset = (label_width - self.display_width) / 2
            y_offset = (label_height - self.display_height) / 2
            
            # Adjust click coordinates
            click_x = event.x - x_offset
            click_y = event.y - y_offset
            
            # Check if click is within the actual image bounds
            if 0 <= click_x <= self.display_width and 0 <= click_y <= self.display_height:
                # Convert to original image coordinates
                orig_x = int(click_x * scale_x)
                orig_y = int(click_y * scale_y)
                
                # Ensure coordinates are within bounds
                orig_x = max(0, min(orig_x, self.original_width - 1))
                orig_y = max(0, min(orig_y, self.original_height - 1))
                
                # Get BGR color and convert to RGB
                bgr_color = self.current_image[orig_y, orig_x]
                rgb_color = tuple(reversed(bgr_color))
                
                # Update color information
                self.update_color_info(rgb_color)
                self.status_var.set(f"Color detected at ({orig_x}, {orig_y})")
            
        except Exception as e:
            print(f"Error in click detection: {e}")
            self.status_var.set("Error detecting color at clicked position")
    
    def update_color_info(self, rgb_color):
        self.current_color = rgb_color
        r, g, b = rgb_color
        
        print(f"Updating color info: RGB({r}, {g}, {b})")  # Debug
        
        # Update color preview
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        self.color_preview.config(bg=hex_color)
        
        # Get color name
        color_name = self.get_color_name(rgb_color)
        print(f"Color name: {color_name}")  # Debug
        
        # Convert to HSL
        hsl = colorsys.rgb_to_hls(r/255, g/255, b/255)
        h, s, l = int(hsl[0]*360), int(hsl[1]*100), int(hsl[2]*100)
        
        # Update labels
        self.color_name_var.set(f"Color Name: {color_name}")
        self.rgb_var.set(f"RGB: ({r}, {g}, {b})")
        self.hex_var.set(f"HEX: {hex_color.upper()}")
        self.hsl_var.set(f"HSL: ({h}°, {s}%, {l}%)")
    
    def get_color_name(self, rgb_color):
        """Get color name using a simple color mapping approach"""
        try:
            # Try webcolors first
            color_name = webcolors.rgb_to_name(rgb_color)
            return color_name.title()
        except ValueError:
            # If webcolors fails, use our own color mapping
            return self.get_closest_color_name(rgb_color)
    
    def get_closest_color_name(self, rgb_color):
        """Find closest color name using basic color definitions"""
        r, g, b = rgb_color
        
        # Define basic colors
        color_map = {
            'Red': (255, 0, 0),
            'Green': (0, 255, 0),
            'Blue': (0, 0, 255),
            'Yellow': (255, 255, 0),
            'Orange': (255, 165, 0),
            'Purple': (128, 0, 128),
            'Pink': (255, 192, 203),
            'Brown': (165, 42, 42),
            'Gray': (128, 128, 128),
            'Black': (0, 0, 0),
            'White': (255, 255, 255),
            'Cyan': (0, 255, 255),
            'Magenta': (255, 0, 255),
            'Navy': (0, 0, 128),
            'Maroon': (128, 0, 0),
            'Olive': (128, 128, 0),
            'Lime': (0, 255, 0),
            'Aqua': (0, 255, 255),
            'Silver': (192, 192, 192),
            'Teal': (0, 128, 128),
            'Fuchsia': (255, 0, 255),
            'Gold': (255, 215, 0),
            'Indigo': (75, 0, 130),
            'Violet': (238, 130, 238),
            'Turquoise': (64, 224, 208),
            'Coral': (255, 127, 80),
            'Salmon': (250, 128, 114),
            'Khaki': (240, 230, 140),
            'Crimson': (220, 20, 60)
        }
        
        min_distance = float('inf')
        closest_color = 'Unknown'
        
        for color_name, (cr, cg, cb) in color_map.items():
            # Calculate Euclidean distance
            distance = ((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_color = color_name
        
        return closest_color
    
    def capture_current_color(self):
        if self.current_color is None:
            messagebox.showwarning("Warning", "No color detected!")
            return
        
        r, g, b = self.current_color
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        color_name = self.get_color_name(self.current_color)
        
        print(f"Capturing color: {color_name} - RGB{self.current_color} - {hex_color}")  # Debug
        
        # Add to history
        color_info = {
            'rgb': self.current_color,
            'hex': hex_color,
            'name': color_name
        }
        
        self.color_history.append(color_info)
        self.update_color_history()
        
        self.status_var.set(f"Captured: {color_name} ({hex_color}) - Total: {len(self.color_history)}")
    
    def update_color_history(self):
        """Update the color history display"""
        self.history_text.config(state=tk.NORMAL)
        
        # Clear and add header if this is the first color
        if len(self.color_history) == 1:
            self.history_text.delete(1.0, tk.END)
            self.history_text.insert(tk.END, "🎨 Captured Colors:\n" + "="*25 + "\n\n")
        
        # Add the latest color
        if self.color_history:
            latest_color = self.color_history[-1]
            color_text = f"#{len(self.color_history):02d} {latest_color['name']}\n"
            color_text += f"HEX: {latest_color['hex']}\n"
            r, g, b = latest_color['rgb']
            color_text += f"RGB: ({r}, {g}, {b})\n"
            color_text += "-" * 20 + "\n\n"
            
            self.history_text.insert(tk.END, color_text)
            
            # Scroll to bottom
            self.history_text.see(tk.END)
        
        self.history_text.config(state=tk.DISABLED)
        print(f"Color history updated. Total colors: {len(self.color_history)}")  # Debug
    
    def __del__(self):
        if self.cap:
            self.cap.release()

def main():
    # Check if required packages are installed
    required_packages = {
        'cv2': 'opencv-python',
        'PIL': 'pillow',
        'webcolors': 'webcolors'
    }
    
    missing_packages = []
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(pip_name)
    
    if missing_packages:
        print("❌ Missing required packages!")
        print("Please install the following packages:")
        for package in missing_packages:
            print(f"  pip install {package}")
        print("\nThen run the script again.")
        return
    
    print("✅ All required packages are installed!")
    print("🚀 Starting Color Detection App...")
    
    root = tk.Tk()
    app = ColorDetectionApp(root)
    
    # Handle window closing
    def on_closing():
        print("Closing application...")
        app.is_camera_running = False
        if app.cap:
            app.cap.release()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted by user")
        on_closing()

if __name__ == "__main__":
    main()

