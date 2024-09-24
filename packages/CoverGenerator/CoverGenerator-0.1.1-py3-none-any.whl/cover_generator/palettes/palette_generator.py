import os
import json
import cover_generator.color as cc
import cover_generator.cover_generator as cg
from os.path import abspath, join

def user_generate_palettes():
    """
    Generates palette and example images for each color pair in the palette.
    """
    hue_offset = None
    primary_saturation = None
    primary_value = None
    secondary_saturation = None
    secondary_value = None
    # Get values from the user
    palette_category = input("Palette Category: ")
    palette_name = input("Palette Name: ")
    while hue_offset is None:
        try:
            hue_offset = float(1 / int(input("Hue Offset (1/X): ")))
        except ValueError: hue_offset = None
    while primary_saturation is None:
        try:
            primary_saturation = float(input("Primary Saturation (0.0 - 1.0): "))
        except ValueError: primary_saturation = None
    while primary_value is None:
        try:
            primary_value = float(input("Primary Value (0.0 - 1.0): "))
        except ValueError: primary_value = None
    while secondary_saturation is None:
        try:
            secondary_saturation = float(input("Secondary Saturation (0.0 - 1.0): "))
        except ValueError: secondary_saturation = None
    while secondary_value is None:
        try:
            secondary_value = float(input("Secondary Value (0.0 - 1.0): "))
        except ValueError: secondary_value = None
    # Generate the user offset Palette
    palette = cc.generate_offset_palette(palette_name, palette_category, hue_offset,
            primary_saturation=primary_saturation, primary_value=primary_value,
            secondary_saturation=secondary_saturation, secondary_value=secondary_value)
    # Save palette as a json file
    palette_file = abspath(join(os.getcwd(), f"{palette_name}.json"))
    with open(palette_file, "w", encoding="UTF-8") as out_file:
        out_file.write(json.dumps(palette, indent="   ", separators=(", ", ": ")))
    # Run through all pairs in the palette
    for pair in palette["color_pairs"]:
        cover_image = abspath(join(os.getcwd(), f"[{pair['id']}] {palette_name}.png"))
        svg = cg.generate_bubble_layout("PALETTE TESTING", "PERSON", pair["primary_color"], pair["secondary_color"])
        # Save Cover Image
        print(f"{palette_name} ({pair['id']})")
        cg.write_layout_to_image(svg, cover_image)

if __name__ == "__main__":
    user_generate_palettes()