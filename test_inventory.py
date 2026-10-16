
"""Basic manual checks for the component inventory."""

from firmware_assistant.database import (
    list_components,
    search_components,
    get_component_by_id,
)


print("=== All components ===")
print(list_components())

print("\n=== Search for sensors ===")
print(search_components("sensor"))

print("\n=== Search for ESP32 ===")
print(search_components("ESP32"))

print("\n=== Find component ID 1 ===")
print(get_component_by_id(1))

print("\n=== Find a missing component ===")
print(get_component_by_id(9999))