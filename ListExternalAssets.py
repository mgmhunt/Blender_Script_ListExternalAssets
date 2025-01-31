import bpy
import os

def list_external_assets():
    external_files = {}
    
    # Function to resolve absolute paths correctly
    def get_absolute_path(path):
        abs_path = bpy.path.abspath(path)
        return os.path.normpath(abs_path)  # Normalize the path to remove '..' and redundant separators
    
    # Check all images
    for img in bpy.data.images:
        if img.source == 'FILE' and img.filepath:
            abs_path = get_absolute_path(img.filepath)
            if abs_path not in external_files:
                external_files[abs_path] = []
            external_files[abs_path].append(f"Image: {img.name}")
    
    # Check linked libraries
    for lib in bpy.data.libraries:
        if lib.filepath:
            abs_path = get_absolute_path(lib.filepath)
            if abs_path not in external_files:
                external_files[abs_path] = []
            external_files[abs_path].append(f"Linked Library: {lib.name}")
    
    # Check external sounds
    for snd in bpy.data.sounds:
        if snd.filepath:
            abs_path = get_absolute_path(snd.filepath)
            if abs_path not in external_files:
                external_files[abs_path] = []
            external_files[abs_path].append(f"Sound: {snd.name}")
    
    # Check external fonts
    for font in bpy.data.fonts:
        if font.filepath:
            abs_path = get_absolute_path(font.filepath)
            if abs_path not in external_files:
                external_files[abs_path] = []
            external_files[abs_path].append(f"Font: {font.name}")
    
    # Check world textures (including HDRI)
    for world in bpy.data.worlds:
        if world.node_tree:
            for node in world.node_tree.nodes:
                if hasattr(node, 'image') and node.image:
                    abs_path = get_absolute_path(node.image.filepath)
                    if abs_path not in external_files:
                        external_files[abs_path] = []
                    external_files[abs_path].append(f"World: {world.name} uses Image: {node.image.name}")
    
    # Check material textures (including video textures)
    for mat in bpy.data.materials:
        if mat.node_tree:
            for node in mat.node_tree.nodes:
                if hasattr(node, 'image') and node.image:
                    abs_path = get_absolute_path(node.image.filepath)
                    if abs_path not in external_files:
                        external_files[abs_path] = []
                    external_files[abs_path].append(f"Material: {mat.name} uses Image: {node.image.name}")
    
    # Check external video textures
    for movie in bpy.data.movieclips:
        if movie.filepath:
            abs_path = get_absolute_path(movie.filepath)
            if abs_path not in external_files:
                external_files[abs_path] = []
            external_files[abs_path].append(f"Video Texture: {movie.name}")
    
    # Check external cache files (Alembic, USD, etc.)
    for cache in bpy.data.cache_files:
        if cache.filepath:
            abs_path = get_absolute_path(cache.filepath)
            if abs_path not in external_files:
                external_files[abs_path] = []
            external_files[abs_path].append(f"Cache File: {cache.name}")
    
    # Check linked objects
    for obj in bpy.data.objects:
        if obj.library:
            abs_path = get_absolute_path(obj.library.filepath)
            if abs_path not in external_files:
                external_files[abs_path] = []
            external_files[abs_path].append(f"Linked Object: {obj.name}")
    
    # Check external Python scripts
    for text in bpy.data.texts:
        if text.filepath:
            abs_path = get_absolute_path(text.filepath)
            if abs_path not in external_files:
                external_files[abs_path] = []
            external_files[abs_path].append(f"Python Script: {text.name}")
    
    # Check external physics caches (Smoke, Fluid, Cloth, etc.)
    if bpy.context.scene.rigidbody_world and bpy.context.scene.rigidbody_world.point_cache.filepath:
        abs_path = get_absolute_path(bpy.context.scene.rigidbody_world.point_cache.filepath)
        if abs_path not in external_files:
            external_files[abs_path] = []
        external_files[abs_path].append("Physics Cache")
    
    # Check external reference images
    for obj in bpy.data.objects:
        if obj.type == 'EMPTY' and obj.empty_display_type == 'IMAGE' and obj.data:
            abs_path = get_absolute_path(obj.data.filepath)
            if abs_path not in external_files:
                external_files[abs_path] = []
            external_files[abs_path].append(f"Reference Image: {obj.name}")
    
    # Create a new text file in Blender and write the results
    text_name = "External_Assets_List"
    if text_name in bpy.data.texts:
        text_block = bpy.data.texts[text_name]
    else:
        text_block = bpy.data.texts.new(name=text_name)
    
    text_block.clear()
    text_block.write("External Assets Summary:\n\n")
    
    # Summary list of paths
    for path in external_files.keys():
        text_block.write(f"{path}\n")
    
    text_block.write("\nDetailed Usage:\n\n")
    
    if external_files:
        for path, usages in external_files.items():
            text_block.write(f"{path}\n")
            for usage in usages:
                text_block.write(f"    - {usage}\n")
            text_block.write("\n")
    else:
        text_block.write("No external assets found.\n")

# Run the function
list_external_assets()
