import PyOpenColorIO as ocio

# Load the Houdini OCIO configuration file
houdini_config_path = '../houdini/houdini-config-v1.0.0_aces-v1.3_ocio-v2.1.ocio'
houdini_config = ocio.Config.CreateFromFile(houdini_config_path)

# Load the Blender OCIO configuration file
blender_config_path = '../blender/config.ocio'
blender_config = ocio.Config.CreateFromFile(blender_config_path)

# Function to print the displays and views
def print_displays_and_views(config, config_name):
    displays = config.getDisplays()
    print(f"{config_name} Displays:")
    for display in displays:
        print(f"  Display: {display}")
        views = config.getViews(display)
        for view in views:
            color_space = config.getDisplayViewColorSpaceName(display, view)
            looks = config.getDisplayViewLooks(display, view)
            print(f"    View: {view}")
            print(f"      Color Space: {color_space}")
            print(f"      Looks: {looks}")

# Function to copy displays from Houdini to Blender config
def copy_displays(houdini_config: ocio.Config, blender_config: ocio.Config):
    displays = houdini_config.getDisplays()
    for display in displays:
        if display == 'Apple Display P3 - Display':
            views = houdini_config.getViews(display)
            for view in views:
                color_space = houdini_config.getDisplayViewColorSpaceName(display, view)
                looks = houdini_config.getDisplayViewLooks(display, view)
                blender_config.addDisplayView(display, view, color_space, looks)
                print(f"Copied view '{view}' for display '{display}' with color space '{color_space}' and looks '{looks}'")

# Print displays and views for both configs before copying
print_displays_and_views(houdini_config, "Houdini Config")
print_displays_and_views(blender_config, "Blender Config")

# Copy the displays and views from Houdini to Blender
copy_displays(houdini_config, blender_config)

# Print displays and views for Blender config after copying
print_displays_and_views(blender_config, "Blender Config After Copying")
