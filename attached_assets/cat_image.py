
import pygame
import os

def load_cat_image():
    cat_path = os.path.join("attached_assets", "IMG_6816.png")
    if os.path.exists(cat_path):
        try:
            # Load and scale the image
            original_img = pygame.image.load(cat_path)
            return pygame.transform.scale(original_img, (800, 600))
        except pygame.error:
            print(f"Error loading cat image from {cat_path}")
            return None
    else:
        print(f"Cat image not found at {cat_path}")
        return None
