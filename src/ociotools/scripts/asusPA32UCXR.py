import PyOpenColorIO as ocio

def create_ocio_config():
    # Create a new OCIO config
    config = ocio.Config.CreateRaw()
    
    # Set the OCIO version (major, minor)
    config.setVersion(2, 0)

    # Set default luma coefficients
    config.setDefaultLumaCoefs([0.2126, 0.7152, 0.0722])

    # Add a new color space for your ASUS PA32UCXR monitor
    red = (0.6908, 0.3074)
    green = (0.1781, 0.7520)
    blue = (0.1494, 0.0592)
    white_point = (0.3135, 0.3287)  # Close to D65

    # Create an OCIO matrix transform from RGB to XYZ based on the monitor's chromaticity values
    matrix_transform = ocio.MatrixTransform()
    matrix = [1.7167, -0.3557, -0.2539, 0, -0.6667, 1.6165, -0.0832, 0, 0.0177, -0.0422, 0.9421, 0, 0, 0, 0, 1]
    matrix_transform.setMatrix(matrix)

    # Add PQ exponent (for HDR)
    pq_transform = ocio.ExponentTransform(value=[2.4, 2.4, 2.4, 1.0])

    # Create a new color space for the calibrated monitor
    colorspace_bt2020_pq = ocio.ColorSpace(name="Rec.2100-PQ-BT2020-Custom")
    colorspace_bt2020_pq.setDescription("BT.2020 primaries with PQ (HDR) encoding from calibration")
    colorspace_bt2020_pq.setBitDepth(ocio.BIT_DEPTH_F32)

    # Combine the matrix and PQ transform
    group_transform = ocio.GroupTransform()
    group_transform.appendTransform(matrix_transform)  # Use appendTransform
    group_transform.appendTransform(pq_transform)      # Use appendTransform

    colorspace_bt2020_pq.setTransform(group_transform, ocio.COLORSPACE_DIR_FROM_REFERENCE)

    # Add the color space to the config
    config.addColorSpace(colorspace_bt2020_pq)

    # Add the display for this monitor using the new color space
    display_name = "ASUS PA32UCXR - Dolby Vision (PQ)"
    view_name = "HDR PQ 1000 nits"
    config.addDisplayView(display_name, view_name, "Rec.2100-PQ-BT2020-Custom")

    # Save the OCIO config to a file
    output_path = "../asus/asus_pa32ucxr.ocio"
    config.serialize(output_path)
    print(f"Updated OCIO config with calibration saved to {output_path}")

# Run the function
create_ocio_config()
