import numpy as np
from pyvox.models import Vox
from pyvox.writer import VoxWriter

default_voxel_color_map = {
    -4: [180, 187, 216],  # (lightgray) 'Building',
    -3: [78, 99, 63],   # (forestgreen) 'Tree',
    -2: [188, 143, 143],  # (saddle brown) 'Underground',
    0: [239, 228, 176],   # 'Bareland (ground surface)',
    1: [123, 130, 59],   # (greenyellow) 'Rangeland (ground surface)',
    2: [108, 119, 129],   # (darkgray) 'Developed space (ground surface)',
    3: [59, 62, 87],      # (dimgray) 'Road (ground surface)',
    4: [116, 150, 66],   # (greenyellow) 'Tree (ground surface)',
    5: [24, 61, 107],    # (blue) 'Water (ground surface)',
    6: [112, 120, 56],   # (lightgreen) 'Agriculture land (ground surface)',
    7: [150, 166, 190],    # (lightgray) 'Building (ground surface)'
    8: [150, 166, 190],    # (lightgray) 'Building (ground surface)'
}

# Define the color map
# default_voxel_color_map = {
#     -4: [180, 187, 216],  # (lightgray) 'Building',
#     -3: [48, 176, 158],   # (forestgreen) 'Tree',
#     -2: [188, 143, 143],  # (saddle brown) 'Underground',
#     0: [239, 228, 176],   # 'Bareland (ground surface)',
#     1: [145, 168, 86],   # (greenyellow) 'Rangeland (ground surface)',
#     2: [108, 119, 129],   # (darkgray) 'Developed space (ground surface)',
#     3: [101, 101, 108],      # (dimgray) 'Road (ground surface)',
#     4: [145, 168, 86],   # (greenyellow) 'Tree (ground surface)',
#     5: [23, 55, 87],    # (blue) 'Water (ground surface)',
#     6: [150, 226, 180],   # (lightgreen) 'Agriculture land (ground surface)',
#     7: [150, 166, 190],    # (lightgray) 'Building (ground surface)'
#     8: [150, 166, 190],    # (lightgray) 'Building (ground surface)'
# }

def create_custom_palette(color_map):
    palette = np.zeros((256, 4), dtype=np.uint8)
    palette[:, 3] = 255  # Set alpha to 255 for all colors
    
    # Set the first color (index 0) to black with alpha 0 (fully transparent)
    palette[0] = [0, 0, 0, 0]
    
    for i, color in enumerate(color_map.values(), start=1):
        palette[i, :3] = color
    
    return palette

def create_mapping(color_map):
    return {value: i+1 for i, value in enumerate(color_map.keys())}

def numpy_to_vox(array, color_map, output_file):
    palette = create_custom_palette(color_map)
    value_mapping = create_mapping(color_map)
    
    # Ensure 0 maps to 0 (void)
    value_mapping[0] = 0
    
    # Flip the array along the z-axis
    array_flipped = np.flip(array, axis=2)
    
    # Transpose the array to match MagicaVoxel's axis order
    # MagicaVoxel expects (y, z, x), so we transpose from (x, y, z) to (y, z, x)
    array_transposed = np.transpose(array_flipped, (1, 2, 0))
    
    # Map the array values to palette indices
    mapped_array = np.vectorize(value_mapping.get)(array_transposed, 0)
    
    # Create a Vox model
    vox = Vox.from_dense(mapped_array.astype(np.uint8))
    
    # Set the custom palette
    vox.palette = palette
    
    # Write the Vox file
    VoxWriter(output_file, vox).write()

    return value_mapping, palette, array_transposed.shape


def export_magicavoxel_vox(array, output_path):

    # Convert and save
    value_mapping, palette, new_shape = numpy_to_vox(array, default_voxel_color_map, output_path)
    print(f"\t{output_path} was successfully exported")
    # print(f"Original shape: {array.shape}")
    # print(f"Shape in VOX file: {new_shape}")

    # # Print the value mapping for reference
    # for original, new in value_mapping.items():
    #     print(f"Original value {original} mapped to palette index {new}")
    #     if new == 0:
    #         print("  Color: Void (transparent)")
    #     else:
    #         print(f"  Color: {palette[new, :3]}")
    #     print()