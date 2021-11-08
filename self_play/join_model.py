import sys


data = ''
for elem in sys.argv[2:]:
    with open('learned_data/' + elem, 'r') as f:
        data += f.read()

with open('eval/' + sys.argv[1], 'w') as f:
    f.write(data)