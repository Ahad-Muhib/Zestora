import codecs

# Read the file
with open('tips/tip_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace special characters with ASCII equivalents
content = content.replace('\u2014', '--')  # em dash
content = content.replace('\u2019', "'")   # right single quotation mark
content = content.replace('\u00b0', 'deg') # degree symbol

# Write back
with open('tips/tip_data.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed encoding issues!")
