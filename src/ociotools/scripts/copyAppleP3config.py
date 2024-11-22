# CODE UNVERIFIED 
# Check before you use this code

import PyOpenColorIO as ocio

# Paths to the provided files
target_config_path = '../blender/config.ocio'
apple_display_config_path = 'apple_display_p3_config.ocio'
merged_config_path = '../blender/merged_config.ocio'

# Load the configurations
target_config = ocio.Config.CreateFromFile(target_config_path)
apple_display_config = ocio.Config.CreateFromFile(apple_display_config_path)

# Function to merge displays and views
def merge_displays_and_views(source_config, target_config):
    displays = source_config.getDisplays()
    for display in displays:
        views = source_config.getViews(display)
        for view in views:
            color_space = source_config.getDisplayViewColorSpaceName(display, view)
            looks = source_config.getDisplayViewLooks(display, view)
            target_config.addDisplayView(display, view, color_space, looks)
            print(f"Merged view '{view}' for display '{display}' with color space '{color_space}' and looks '{looks}'")
    return target_config

# Function to merge color spaces
def merge_color_spaces(source_config, target_config):
    color_spaces = source_config.getColorSpaces()
    for cs in color_spaces:
        target_config.addColorSpace(cs)
    return target_config

# Function to merge view transforms
def merge_view_transforms(source_config, target_config):
    view_transforms = source_config.getViewTransforms()
    for vt in view_transforms:
        target_config.addViewTransform(vt)
    return target_config

# Function to update active displays and views
def update_active_displays_and_views(source_config, target_config):
    source_displays = source_config.getActiveDisplays().split(', ')
    target_displays = target_config.getActiveDisplays().split(', ')
    for display in source_displays:
        if display not in target_displays:
            target_displays.append(display)
    target_config.setActiveDisplays(', '.join(target_displays))
    
    source_views = source_config.getActiveViews().split(', ')
    target_views = target_config.getActiveViews().split(', ')
    for view in source_views:
        if view not in target_views:
            target_views.append(view)
    target_config.setActiveViews(', '.join(target_views))

# Merge the relevant information
target_config = merge_displays_and_views(apple_display_config, target_config)
target_config = merge_color_spaces(apple_display_config, target_config)
target_config = merge_view_transforms(apple_display_config, target_config)
update_active_displays_and_views(apple_display_config, target_config)

# Save the merged configuration to a new file
with open(merged_config_path, 'w') as f:
    f.write(target_config.serialize())

print(f"Merged OCIO configuration saved to: {merged_config_path}")

