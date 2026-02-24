import sys
import teslapy
import time
from datetime import datetime
from pathlib import Path

try:
    controlFilePath = Path('~/PythonCode/Tesla/control.txt').expanduser()
    controlFile = open(controlFilePath)
except FileNotFoundError:
    sys.exit(1)

targetAmps = controlFile.readline().rstrip('\n')
accountName = controlFile.readline().rstrip('\n')
controlFile.close()

with teslapy.Tesla(accountName) as tesla:
    # Authorise and load vehicles
    tesla.fetch_token()
    myVehicle = tesla.vehicle_list()[0]  # Get the first vehicle in your account. If you have more than one Tesla, lucky you! Make another installation of this in a different folder, and change the index number from 0 to 1,2,3..99 etc.
    summary = myVehicle.get_vehicle_summary()

    # If you don't want to force the change when the car is offline or asleep, then uncomment the next two lines.
    #if summary['state'] == "offline" or summary['state'] == "asleep":
        #sys.exit(1)

    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    myVehicle.sync_wake_up()
    myVehicleData = myVehicle.get_vehicle_data()

    # Information about the car's state
    vehicleState = myVehicleData.get('vehicle_state', {})

    # Information about the car's drive state and location
    driveState = myVehicleData.get('drive_state', {})
    latitude = driveState.get('latitude')
    longitude = driveState.get('longitude')

    # Information about the the state of the charging, such as battery state of charge and amps
    chargeState = myVehicleData.get('charge_state', {})
    chargingState = chargeState.get('charging_state', {})
    batteryLevel = chargeState.get('battery_level', {})
    batteryRange = chargeState.get('battery_range', {})
    chargerVoltage = chargeState.get('charger_voltage')
    chargeRate = chargeState.get('charge_rate')
    estBatteryRange = chargeState.get('est_battery_range')

    if chargingState != 'Disconnected':
        chargingAmps = chargeState.get('charge_amps', {})
        chargingAmps = str(chargingAmps)
        print(f"{now},{targetAmps},{chargingAmps},{latitude},{longitude},{chargerVoltage},{chargeRate},{batteryLevel},{batteryRange},{estBatteryRange},{chargingState}")
        myVehicle.command('CHARGING_AMPS', charging_amps=targetAmps)

    if chargingState == 'Complete' or (chargingState == 'Stopped' and batteryLevel == 100):
        #Delete the control file to stop the car waking up every minute after a charge has been completed
        Path(controlFilePath).unlink()

