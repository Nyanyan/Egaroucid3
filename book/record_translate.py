

all_chars = [
    '!', '#', '$', '&', "'", '(', ')', '*', 
    '+', ',', '-', '.', '/', '0', '1', '2', 
    '3', '4', '5', '6', '7', '8', '9', ':', 
    ';', '<', '=', '>', '?', '@', 'A', 'B', 
    'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 
    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
    '[', ']', '^', '_', '`', 'a', 'b', 'c', 
    'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']

xs = 'ABCDEFGH'
ys = '12345678'

char_translate = {}
for i in range(64):
    char_translate[all_chars[i]] = xs[i % 8] + ys[i // 8]

def translate(raw_record):
    raw_record_split, _ = raw_record.split()
    record = ''
    for i in range(0, len(raw_record_split), 2):
        record += char_translate[raw_record_split[i + 1]]
    print(record)

with open('self_play/0000003.txt', 'r') as f:
    for _ in range(10):
        raw_record = f.readline()
        translate(raw_record)