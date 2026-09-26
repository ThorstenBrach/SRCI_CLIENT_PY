import re

# Read the file
with open('src/robot_library_py/enumerations/Events/ErrorIdEnum.py', 'r') as f:
    content = f.read()

# Replace /// comments with """
content = re.sub(r'^\s*/// (.*)$', r'    """\1"""', content, flags=re.MULTILINE)

# Replace := with =
content = re.sub(r'\s*:=\s*', ' = ', content)

# Replace 16#hex with 0xhex
content = re.sub(r'16#([0-9A-Fa-f]+)', r'0x\1', content)

# Remove trailing commas
content = re.sub(r',\s*$', '', content, flags=re.MULTILINE)

# Write back
with open('src/robot_library_py/enumerations/Events/ErrorIdEnum.py', 'w') as f:
    f.write(content)

print('Conversion done')