#!/usr/bin/env python3
import sys
from typing import List
import re

FLAG_REGEX = re.compile(r'\d{14}UTC[A-Z0-9]{15}')

def parse_string(input: str) -> List[str]:
    return list(set(re.findall(FLAG_REGEX, input)))

if __name__ == "__main__":
    input = sys.stdin.read()
    #print(input)
    flags = parse_string(input)
    print("\n".join(flags))
    #print(f"Found {len(flags)} flags!")
