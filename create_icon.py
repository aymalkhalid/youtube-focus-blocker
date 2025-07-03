#!/usr/bin/env python3
"""
Create an icon for the YouTube Stopper executable
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create a professional-looking icon for the app"""
    
    # Create multiple sizes for the ICO file
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    
    for size in sizes:
        # Create a new image with transparent background
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Colors
        bg_color = (220, 53, 69, 255)  # YouTube red
        circle_color = (255, 255, 255, 255)  # White
        
        # Draw background circle
        margin = max(1, size // 16)
        draw.ellipse([margin, margin, size-margin, size-margin], 
                    fill=bg_color, outline=None)
        
        # Draw the "stop" symbol (square in circle)
        inner_margin = max(3, size // 8)
        square_size = size - (inner_margin * 2)
        square_x1 = inner_margin
        square_y1 = inner_margin
        square_x2 = square_x1 + square_size
        square_y2 = square_y1 + square_size
        
        draw.rectangle([square_x1, square_y1, square_x2, square_y2], 
                      fill=circle_color, outline=None)
        
        # Add a small "Y" if the icon is large enough
        if size >= 32:
            font_size = max(8, size // 6)
            try:
                # Try to use a system font
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                # Fallback to default font
                font = ImageFont.load_default()
            
            # Calculate text position to center it
            text = "Y"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            text_x = (size - text_width) // 2
            text_y = (size - text_height) // 2 - 1
            
            draw.text((text_x, text_y), text, fill=bg_color, font=font)
        
        images.append(img)
    
    # Save as ICO file
    images[0].save(
        'icon.ico',
        format='ICO',
        sizes=[(img.width, img.height) for img in images],
        append_images=images[1:],
    )
    
    print("✅ Icon created: icon.ico")
    
    # Also create a PNG version for reference
    images[-1].save('icon.png', format='PNG')
    print("✅ PNG version created: icon.png")

if __name__ == "__main__":
    create_icon()
