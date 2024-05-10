def rgb_to_binary(rgb):
    r, g, b = rgb
    return (format(r, '08b'), format(g, '08b'), format(b, '08b'))


def binary_to_rgb(binary_values):
    r, g, b = binary_values
    return (int(r, 2), int(g, 2), int(b, 2))


# Example usage
rgb_values = (252, 186, 3)
binary_values = ('11111100', '10111010', '00000011')

# Display binary representation of each example RGB value
binary_representation = rgb_to_binary(rgb_values)
print(f"RGB {rgb_values} in binary is {binary_representation}")
RGB_representation = binary_to_rgb(binary_values)
print(f"Binary {binary_values} in binary is {RGB_representation}")

print("\n\n\n")

new_binary_values = ('11111101', '10111011', '00000010')
RGB_representation = binary_to_rgb(new_binary_values)
print(f"Binary {new_binary_values} in binary is {RGB_representation}")
