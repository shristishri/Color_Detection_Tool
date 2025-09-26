# 🎨 Python Color Detection Tool

A comprehensive color detection application built with Python that can analyze colors from both live camera feed and uploaded images. Perfect for designers, developers, and anyone who needs to identify and capture color information accurately.

## ✨ Features

### 🎥 Dual Input Modes
- **Real-time Camera Detection**: Live color detection with crosshair targeting
- **Image Upload Analysis**: Click-to-detect colors from uploaded images

### 🎯 Accurate Color Analysis
- **RGB Values**: Red, Green, Blue color components (0-255)
- **HEX Codes**: Web-ready hexadecimal color codes
- **HSL Values**: Hue, Saturation, Lightness percentages
- **Color Names**: Intelligent color naming with 30+ predefined colors

### 📊 Advanced Features
- **Color History**: Track and save up to 15 recently captured colors
- **Smart Color Matching**: Uses Euclidean distance for closest color name detection
- **Aspect Ratio Preservation**: Images display without distortion
- **Real-time Updates**: Instant color information as you move the camera



## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Webcam (for camera mode)
- Compatible image files (JPG, PNG, BMP, GIF, TIFF)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/python-color-detection.git
cd python-color-detection
```

2. **Install required dependencies**
```bash
pip install opencv-python pillow webcolors
```

3. **Run the application**
```bash
python color_detection.py
```

### Alternative Installation (using requirements.txt)
```bash
pip install -r requirements.txt
python color_detection.py
```

## 📋 Requirements

Create a `requirements.txt` file with:
```txt
opencv-python>=4.5.0
Pillow>=8.0.0
webcolors>=1.11.1
```

## 🎯 Usage Guide

### Camera Mode
1. Click **"📹 Start Camera"** to begin live detection
2. Point the green crosshair at any color
3. Color information updates in real-time
4. Click **"🎯 Capture Color"** to save interesting colors
5. Click **"⏹️ Stop Camera"** when finished

### Image Mode
1. Click **"📁 Upload Image"** to select an image file
2. Click anywhere on the uploaded image
3. Color at that pixel will be detected and displayed
4. Click **"🎯 Capture Color"** to save the color

### Color History
- View up to 15 recently captured colors
- Each entry shows color name, HEX code, and RGB values
- Automatically scrolls to show newest colors
- Perfect for building color palettes

## 🛠️ Technical Details

### Dependencies
- **OpenCV (cv2)**: Camera access and image processing
- **Pillow (PIL)**: Image handling and display
- **tkinter**: GUI framework (included with Python)
- **webcolors**: Color name mapping and conversion
- **colorsys**: HSL color space conversions

### Color Detection Algorithm
1. **Pixel Sampling**: Extract RGB values from specific coordinates
2. **Color Space Conversion**: Convert between RGB, HEX, and HSL
3. **Name Matching**: Use Euclidean distance to find closest named color
4. **Fallback System**: 30+ predefined colors if webcolors fails

### Supported Formats
- **Images**: JPG, JPEG, PNG, BMP, GIF, TIFF
- **Color Spaces**: RGB, HEX, HSL
- **Output**: Real-time display and exportable color data

## 🎨 Color Palette

The application recognizes 30+ colors including:
- **Primary**: Red, Green, Blue
- **Secondary**: Yellow, Orange, Purple
- **Tertiary**: Pink, Brown, Gray
- **Extended**: Coral, Turquoise, Indigo, Crimson, etc.

## 🔧 Customization

### Adding New Colors
Edit the `color_map` dictionary in `get_closest_color_name()`:
```python
color_map = {
    'Your Color Name': (R, G, B),  # Add your color here
    'Custom Blue': (30, 144, 255),
    # ... existing colors
}
```

### Adjusting History Size
Change the history limit in `update_color_history()`:
```python
recent_colors = self.color_history[-20:]  # Show last 20 colors
```

## 🐛 Troubleshooting

### Camera Issues
- **Camera not detected**: Ensure no other applications are using the camera
- **Permission denied**: Grant camera permissions to Python/terminal
- **Poor quality**: Clean camera lens and ensure good lighting

### Image Issues
- **Click detection fails**: Ensure image is fully loaded before clicking
- **Image too large**: App automatically resizes while maintaining aspect ratio
- **Unsupported format**: Convert to JPG or PNG

### Common Solutions
```bash
# If OpenCV installation fails
pip install --upgrade pip
pip install opencv-python-headless

# If GUI doesn't appear on Linux
sudo apt-get install python3-tk

# If webcolors is missing
pip install webcolors
```

## 📁 Project Structure
```
python-color-detection/
├── color_detection.py      # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── examples/              # Sample images for testing
```

## 🚀 Future Enhancements

### Planned Features
- [ ] **Color Palette Export** - Save palettes to JSON/CSV
- [ ] **Batch Image Processing** - Analyze multiple images
- [ ] **Dominant Color Extraction** - Find main colors in images
- [ ] **Color Blindness Simulation** - Preview colors for accessibility
- [ ] **Machine Learning Integration** - Advanced color classification
- [ ] **API Integration** - Connect to online color databases

### Performance Improvements
- [ ] **Faster Image Loading** - Optimize large image handling
- [ ] **Memory Management** - Better resource cleanup
- [ ] **Multi-threading** - Separate UI and processing threads

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit: `git commit -am 'Add feature-name'`
5. Push: `git push origin feature-name`
6. Submit a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Add docstrings to functions
- Include error handling
- Test with both camera and image modes

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@shristishri](https://github.com/shristishri)

## 🙏 Acknowledgments

- **OpenCV Team** - Computer vision library
- **Pillow Contributors** - Image processing capabilities  
- **Python Community** - Amazing ecosystem and support
- **Color Theory Resources** - Inspiration for color matching algorithms

## 📊 Statistics

- **Languages**: Python 100%
- **Dependencies**: 4 main packages
- **Features**: 15+ color detection features
- **Supported Formats**: 6 image formats
- **Color Database**: 30+ named colors

---

⭐ **Star this repository** if you found it helpful!

🐛 **Report bugs** by creating an issue

💡 **Suggest features** through discussions

📧 **Contact** for collaboration opportunities
