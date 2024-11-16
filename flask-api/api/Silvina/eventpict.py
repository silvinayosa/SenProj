import os
import re

# Define the folder path
folder_path = "../Database/Event-Pictures"  # Replace with the actual path to your folder

############################################################
##Rename all the .webp files in the folder to .jpg format###
############################################################
# Dictionary to keep track of the count of each filename
# file_counts = {}

# # Loop through each file in the folder
# for filename in os.listdir(folder_path):
#     # Check if the file is a .webp file
#     if filename.endswith(".webp"):
#         # Extract the event name within single quotes using regex
#         match = re.search(r"'([^']*)'", filename)
#         if match:
#             event_name = match.group(1)
#             # Initialize the count if the event name is encountered for the first time
#             if event_name not in file_counts:
#                 file_counts[event_name] = 1
#             else:
#                 file_counts[event_name] += 1

#             # Construct the new filename with .jpg extension
#             new_filename = f"{event_name}.jpg"
#             if file_counts[event_name] > 1:
#                 new_filename = f"{event_name}{file_counts[event_name]}.jpg"
            
#             # Rename the file
#             os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
#             print(f"Renamed '{filename}' to '{new_filename}'")


#########################################################################
##Collect all the filenames in the folder and write them to a text file##
#########################################################################
output_file = "event_picture.txt"  # Output text file name

# Open the output file in write mode
with open(output_file, "w") as file:
    # Loop through each file in the folder
    for filename in os.listdir(folder_path):
        # Write the filename to the text file
        file.write(filename + "\n")

print(f"File list has been written to {output_file}")
