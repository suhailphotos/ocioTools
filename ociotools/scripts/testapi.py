import PyOpenColorIO as ocio

blender_config_path = '../blender/config.ocio'
blender_config = ocio.Config.CreateFromFile(blender_config_path)

active_displays = blender_config.getActiveDisplays().split(', ')
print(active_displays)
