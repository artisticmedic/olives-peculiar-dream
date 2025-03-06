
import pygame
import os

def load_olive_cat_image():
    """Load the Olive cat image for the celebration sprites"""
    # Get the directory of this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct path to the image file
    image_path = os.path.join(current_dir, "olive_cat.png")
    
    try:
        # Load the image
        image = pygame.image.load(image_path)
        # Scale it to a reasonable size for sprites
        image = pygame.transform.scale(image, (40, 40))
        # Make sure the image has an alpha channel
        return image.convert_alpha()
    except pygame.error:
        print(f"Could not load image from {image_path}")
        return None
