#!/usr/bin/env python3
import hashlib


def attempt_mine(data):
    hashed_data = hashlib.sha256()
    hashed_data.update(data.encode('utf-8'))
    return hashed_data.hexdigest()


current_hash = "4a"

data = "8+University of New South Wales+01121c281c1ed269ee79ab66bbe3dfd28eee48d4d80b797a80227632c998698b"
# data = "7+Optus+072e9ff438cc9c46b29cc53453dc5ddde76a8eb46d1124f756ccae38191994d5"

index = 0
while not current_hash.startswith("0") or not current_hash[1].isnumeric():
    current_hash = attempt_mine(f"{data}+{index}\n")
    print(current_hash)
    index += 1

print(index - 1)
print(current_hash)
