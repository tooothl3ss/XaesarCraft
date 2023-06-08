#!/usr/bin/env python3

import re
import sys
import fileinput
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process and format byte arrays')
    parser.add_argument('-n', '--number', type=parse_hex_number, default=None,
                        help='The number to use for XOR or decreasing operation')
    parser.add_argument('-m', '--mode', type=str, choices=['xor', 'rot'], default='xor',
                        help='Mode of operation: xor or rot')
    parser.add_argument('-i','--input', type=str, default=None,
                        help='Input string to process. If not provided, input is read from stdin')
    return parser.parse_args()

def parse_hex_number(hex_string):
    try:
        return int(hex_string, 0)
    except ValueError:
        return None

def decrease_bytes(bytes_list, number=13):
    result = []
    for i, byte in enumerate(bytes_list):
        value = int(byte, 16)
        value = (value - number) % 255   
        hex_value = hex(value).replace('0x', '0x')
        result.append(hex_value if len(hex_value) > 3 else hex_value[:2] + hex_value[2:].zfill(2))
    return result

def extract_bytes(input_string):
    return re.findall(r'0x[0-9a-fA-F]{2}', input_string)

def xor_bytes(bytes_list, number=0xfa):
    result = []
    for i, byte in enumerate(bytes_list):
        value = int(byte, 16)
        value = value ^ number   
        hex_value = hex(value).replace('0x', '0x')
        result.append(hex_value if len(hex_value) > 3 else hex_value[:2] + hex_value[2:].zfill(2))
    return result

def format_output(input_string, processed_bytes):
    if "Byte" in input_string:
        return "[Byte[]] $buf = " + ','.join(processed_bytes)
    elif "byte" in input_string:
        return "byte[] buf = new byte[{}] {{{}}}".format(len(processed_bytes), ','.join(processed_bytes))
    else:
        return "Unknown format"

def main():
    args = parse_arguments()

    raw_input_string = ""
    if args.input:
        raw_input_string = args.input
    else:
        for line in sys.stdin:
            raw_input_string += line

    input_string = raw_input_string.replace('\n', '').replace('\\n', '')
    bytes_list = extract_bytes(input_string)
    if args.mode == 'xor':
        if args.number is None: 
            processed_bytes = xor_bytes(bytes_list)
        else:
            number = args.number 
            processed_bytes = xor_bytes(bytes_list, number)
    elif args.mode == 'rot':
        if args.number is None: 
            processed_bytes = decrease_bytes(bytes_list)
        else:
            number = args.number 
            processed_bytes = decrease_bytes(bytes_list, number)
    
    formatted_output = format_output(raw_input_string, processed_bytes)
    print(f"Processed string: {formatted_output}")


if __name__ == "__main__":
    main()