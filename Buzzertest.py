import asyncio
from buttplug.client import ButtplugClient
from buttplug import DeviceOutputCommand
from buttplug import OutputType
async def main():
    client = ButtplugClient("Vibe Test")
    try:
        print("Attempting connection to interface")
        await client.connect("ws://localhost:12345")
        print("connection successful")
    except Exception as e:
        print(f"Error occurred: {e}")
        return

    while True:
        try:
            print("Starting scan for devices")
            await client.start_scanning()
            await asyncio.sleep(5)  # Wait for devices to be found (up the time for more than one device)
            #Stop device scan after 5 seconds
            await client.stop_scanning()
            print("Scan stopped")
            print(f"Devices found: {len(client.devices)}")

            if len(client.devices) == 0:
                print("No devices found. Make sure Interface Central is connected and visible in Buttplug Central.")
                retry = input("Scan again? (y/n): ").strip().lower()
                if retry != 'y' and retry != 'yes':
                    print("Exiting...")
                    await client.disconnect()
                    return
                else:
                    continue
        except Exception as e:
            print(f"Connection lost during scan: {e}")
            print("Attempting to reconnect...")
            await client.connect("ws://localhost:12345")
            continue
        else:
            print("Devices found:")
            for device in client.devices.values():
                print(f"- {device.name}")
            break
    # Select the first device found
    selected_device = next(iter(client.devices.values()))
    print(f"Selected device: {selected_device.name}")
    # Connect to the selected device
    print("Device connected")

#user input loop for vibration control
    while True:
        user_input = input("Enter vibration intensity (0-100) or 'quit' to exit: ").strip().lower()
        if user_input == "quit":
            print("All done :)")
            break
        try:
            intensity = int(user_input)
            if 0 <= intensity <= 100:
                await selected_device.run_output(DeviceOutputCommand(OutputType.VIBRATE, intensity / 100))
                print(f"Set vibration intensity to {intensity}%")
            else:
                print("Please enter a value between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 100 or 'quit' to exit.")
    await client.disconnect()
    print("Disconnected from server and device - goodbye!")
if __name__ == "__main__":    asyncio.run(main())



