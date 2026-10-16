
"""Initialize the local component database with demonstration records."""

from .database import get_connection, initialize_database


DEMO_COMPONENTS = [
    (
        "ESP32 DevKit",
        "Microcontroller board",
        "Espressif",
        "ESP32 DevKit",
        2,
        None,
        "Wi-Fi, Bluetooth, GPIO",
        "Demonstration record; verify exact board revision.",
    ),
    (
        "DHT11",
        "Sensor",
        None,
        "DHT11",
        1,
        None,
        "Digital interface",
        "Demonstration record; verify the module and pinout.",
    ),
    (
        "IR Receiver",
        "Sensor",
        None,
        None,
        2,
        None,
        None,
        "Demonstration record; exact model not specified.",
    ),
    (
        "16x2 LCD",
        "Display",
        None,
        None,
        1,
        None,
        None,
        "Demonstration record; interface and controller unknown.",
    ),
]


def main():
    """Create the inventory table and insert demo records once."""
    initialize_database()

    with get_connection() as connection:
        connection.executemany("""
            INSERT INTO components (
                name, category, manufacturer, model, quantity,
                voltage_info, interfaces, notes
            )
            SELECT ?, ?, ?, ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1
                FROM components
                WHERE name = ? AND model IS ?
            )
        """, [
            (*component, component[0], component[3])
            for component in DEMO_COMPONENTS
        ])

    print("Component database initialized.")
    print("Demo records are ready for testing.")


if __name__ == "__main__":
    main()