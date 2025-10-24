#with open (...) as ...:
#w for write: overwrite the entire file
#r for read: read the entire file
#a for append: add to the end of the file

# with open("file.txt", "w") as file:
#     file.write("Hello \n")

# with open("file.txt", "r") as file:
#     content=file.read()

# print(content)

# with open("file.txt", "a") as file:
#     file.write("Hello \n")

# tasks=[{"task":"Buy milk","done":False},{},{}]

#json -> javascript object notation

#json.dump(data, file) : dump data to a file
#json.load(file) : load data from a file

import json

# Sample data for demonstration: three identical dictionaries
my_data=[{"name":"Siddhant","age":20},{"name":"Bob","age":30},{"name":"Alice","age":25}]
# Save the my_data list to a JSON file for persistent storage
with open("my_data.json", "w") as f:
    json.dump(my_data, f,indent=4)
    
print("data saved")

# Load the data from the JSON file
with open("my_data.json", "r") as f:
    loaded_data = json.load(f)

print(loaded_data[0]['name'])
print(loaded_data[0]['age'])
