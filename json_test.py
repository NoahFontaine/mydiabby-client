from rich import print
import json

with open("insulinflow_device.json") as f:
    data = json.load(f)

print(data["2025-08-24"].keys())

print(data["2025-08-24"]["list"]['53977'])

# print(data["2025-08-24"]["hour"])