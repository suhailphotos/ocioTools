import PyOpenColorIO as ocio

# load the Houdini OCIO configuration FileExistsError
houdini_config_path = '../houdini/houdini-config-v1.0.0_aces-v1.3_ocio-v2.1.ocio'
houdini_config = ocio.Config.CreateFromFile(houdini_config_path)

#load teh Blender OCIO configuration file
blender_config_path = '../blender/config.ocio'
blender_config = ocio.Config.CreateFromFile(blender_config_path)

# Funtion to copy displays from Houdini to Blender config 
def copy_displays_and_views(houdini_config: ocio.Config, blender_config: ocio.Config):
        displays = houdini_config.getDisplays()
        for display in displays:
            if display == 'Apple Display P3 - Display':
                views = houdini_config.getViews(display)
                for view in views:
                    color_space = houdini_config.getDisplayViewColorSpaceName(display, view)
                    looks = houdini_config.getDisplayViewLooks(display, view)
                    blender_config.addDisplayView(display, view, color_space, looks)
                    print(f"Copied view '{view}' for display '{display}' with color space '{color_space}' and looks '{looks}'")
                    return blender_config

# Funtion to cpy color spaces from Houdini to Blender Config 
def copy_color_spaces(houdini_config: ocio.Config, blender_config: ocio.Config):
    color_spaces = houdini_config.getColorSpaces()
    for cs in color_spaces:
        if cs.getName() == 'Apple Display P3 - Display':
            blender_config.addColorSpace(cs)
    return blender_config

# Funtion to copy view transforms from Houdini to Blender config 
def copy_view_transforms(houdini_config: ocio.Config, blender_config: ocio.Config):
    view_transforms = houdini_config.getViewTransforms()
    for vt in view_transforms:
        blender_config.addViewTransform(vt)
    return blender_config

# copy the relevent information
blender_config = copy_displays_and_views(houdini_config, blender_config)
blender_config = copy_color_spaces(houdini_config, blender_config)
blender_config = copy_view_transforms(houdini_config, blender_config)

# Save the modified Blender OCIO configuration to a new file
modified_blender_config_path = '../blender/modified_blender_config.ocio'
blender_config.serialize(modified_blender_config_path)

print(f"Modified Blender OCIO configuration saved to: {modified_blender_config_path}")
