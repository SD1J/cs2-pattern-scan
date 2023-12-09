import pymem
import pymem.process
import pymem.pattern

# dwLocalPlayerController pattern "48 8B 05 ? ? ? ? 48 85 C0 74 4F"
m_iPawnHealth = 0x7F8

def pattern_to_bytes(hex_string):
    hex_values = hex_string.split()
    byte_literal = ""

    for hex_value in hex_values:
        if hex_value == "?" or hex_value == "??":
            byte_literal += "."
        else:
            byte_literal += rf"\x{hex_value}"
    return bytes(byte_literal, "utf-8")

class Memory:
    def __init__(self):
        self.handle = pymem.Pymem("cs2.exe")
        self.module = None

    def find_pattern(self, modname: str, pattern: str) -> int:
        self.module = pymem.process.module_from_name(self.handle.process_handle, modname)
        pattern_bytes = pattern_to_bytes(pattern)
        match = pymem.pattern.pattern_scan_module(self.handle.process_handle, self.module, pattern_bytes)
        
        return match
    
    def resolve_rip(self, address: int) -> int:
        displacement = self.handle.read_int(address + 0x3)
        return (address + 0x7) + displacement

mem = Memory()

match = mem.find_pattern("client.dll", "48 8B 05 ? ? ? ? 48 85 C0 74 4F")
print(f"found match: {match}")

address = mem.resolve_rip(match) - mem.module.lpBaseOfDll
print(f"address: {address}")

local = mem.handle.read_ulonglong(address + mem.module.lpBaseOfDll)
import time
while True:    
    hp = mem.handle.read_int(local + m_iPawnHealth)
    print(f"hp: {hp}")
    time.sleep(5)