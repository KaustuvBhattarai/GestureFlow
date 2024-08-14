import h5py

def print_and_save_h5_contents(filename):
    # Open the .h5 file
    with h5py.File(filename, 'r') as f:
        # Function to recursively print the contents
        def print_attrs(name, obj):
            print(f"Name: {name}")
            if isinstance(obj, h5py.Dataset):
                print(f"  Dataset shape: {obj.shape}")
                print(f"  Dataset dtype: {obj.dtype}")
            elif isinstance(obj, h5py.Group):
                print(f"  Group: {name}")
            for key, value in obj.attrs.items():
                print(f"    Attribute {key}: {value}")

        # Print the contents of the file
        f.visititems(print_attrs)

        # Prepare the output filename
        output_filename = filename.replace('.h5', '_unpacked.txt')

        # Save the contents to a text file
        with open(output_filename, 'w') as txt_file:
            def write_attrs(name, obj):
                txt_file.write(f"Name: {name}\n")
                if isinstance(obj, h5py.Dataset):
                    txt_file.write(f"  Dataset shape: {obj.shape}\n")
                    txt_file.write(f"  Dataset dtype: {obj.dtype}\n")
                elif isinstance(obj, h5py.Group):
                    txt_file.write(f"  Group: {name}\n")
                for key, value in obj.attrs.items():
                    txt_file.write(f"    Attribute {key}: {value}\n")
            
            # Save the contents to the file
            f.visititems(write_attrs)
    
    print(f"Contents saved to {output_filename}")

# Example usage
filename = 'hand_detection_model.h5'  # Replace with your .h5 file
print_and_save_h5_contents(filename)
