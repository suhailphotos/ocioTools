import PyOpenColorIO as ocio
import shutil
import os

def append_ocio(source_ocio_path, target_ocio_path):
    # Backup the existing target config
    backup_path = f"{target_ocio_path}.bak"
    shutil.copyfile(target_ocio_path, backup_path)
    print(f"Backup of the target config saved at {backup_path}")

    # Load source and target configs
    source_config = ocio.Config.CreateFromFile(source_ocio_path)
    target_config = ocio.Config.CreateFromFile(target_ocio_path)

    # Append colorspaces from source to target
    for cs in source_config.getColorSpaces():
        target_config.addColorSpace(cs)

    # Collect existing active displays and views
    active_displays = set(target_config.getActiveDisplays().split(","))
    active_views = set(target_config.getActiveViews().split(","))

    # Append displays and views
    for display in source_config.getDisplays():
        for view in source_config.getViews(display):
            colorspace = source_config.getDisplayViewColorSpaceName(display, view)
            target_config.addDisplayView(display, view, colorspace)

            # Add display and view to active lists
            active_displays.add(display.strip())
            active_views.add(view.strip())

    # Update active displays and views
    target_config.setActiveDisplays(", ".join(sorted(active_displays)))
    target_config.setActiveViews(", ".join(sorted(active_views)))

    # Append view transforms
    for view_transform in source_config.getViewTransforms():
        target_config.addViewTransform(view_transform)

    # Save the updated config
    with open(target_ocio_path, 'w') as f:
        f.write(target_config.serialize())
    print(f"Appended {source_ocio_path} to {target_ocio_path} and saved the updated config.")

# Example usage
source_ocio_path = "../asus/asus_pa32ucxr.ocio"
target_ocio_path = os.path.expandvars("$DROPBOX/appSettings/houdini/win/20.5/ocio/houdini-config-v2.1.0_aces-v1.3_ocio-v2.3.ocio")
append_ocio(source_ocio_path, target_ocio_path)
