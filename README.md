# SetTeslaAmps
Control the maximum amps that the car draws from your charge.
# Why use TeslaAmps?
If your charger sometimes trips, it may be worth adjusting down very slightly the maximum number of amps your Tesla can draw. 

This can be done through the car's interface and is based on your current location. In most cases 32A is fine, but certain setups (such as mine) trip even a 40A fuse.

Reducing down to 29A seemed to solve the problem, but occasionally it would still trip. I noticed that the car was reporting it was going to draw a maximum of 32A again, so something was preventing the 29A being permanent. I decided to write this script to force it back to 29A every 60 seconds whilst awake and plugged in. There's still a potential for the car to decide it wants 32A - probably when it starts or stops charging, but within 60 seconds it will either trip, or get set back to 29A and remain charging.
# How to use SetTeslaAmps
Install TeslaPy. This contains all the code necessary to integrate your Tesla with Python.

Copy the contents of the "Tesla" folder in this repo to ~/Tesla. Another folder is ok, but the examples below assume you have dropped the folder contents as "Tesla" into your home folder.

In your ~/Tesla folder, edit the "control.txt" file so that the first line reads the number of amps and the second line contains your Tesla account's email address.

Run the command "python AmpTimer.py" manually to initialise the cache.json file in your ~/Tesla folder. This needs to be done with a screen as it will run a browser. If you have to do it headless, run it on another machine and copy the cache.json file into this folder.

Configure your crontab with to execute the following commands:

*/1 21-23 * * * youruser cd ~/Tesla && python ~/Tesla/AmpTimer.py >> ~/Tesla/AmpResults.txt
*/1 00-08 * * * youruser cd ~/Tesla && python ~/Tesla/AmpTimer.py >> ~/Tesla/AmpResults.txt

The two lines above will execute the python code every minute between 9pm and midnight, and then from midnight until 8:59am. Adjust accordingly, but these suit my own energy tariff.

00 13 * * * yourusername ~/Tesla/SetMasterAmps.sh 29 ~/Tesla/ your@teslaemailaddress.something > ~/Tesla/LogSetAmps.txt

The line above recreates the control.txt file that was deleted at the end of the previous charging session.
# Process
Each execution of the python code carries out the following steps:

Look for file control.txt

If not found, just quit and do nothing else.

If found, read the target amps from the first line and Tesla account from the second line. This is generally your email address.

Get the first vehicle. This script only works with one vehicle, but you can amend it to look for other vehicles.

Get all the information it needs.

Force the amps to the target value.

If charging has been completed, delete the control.txt file to avoid it keeping the vehicle awake and using battery. It'll be recreated whenever your crontab tells it to.
# Requirements
Python

Cron

TeslaPy
# Enhancements planned
1: Check for 'stopped' charging status and '100' rather than just 'completed' to stop the code from executing. Sometimes a smart charger will see the vehicle has reached 100% and decide to stop, when in fact there may be a few fractions of a percent still available to charge.

2: Write results to SQL table instead of text file. This will allow for integration with energy tariff monitoring in my Octopus Energy smart meter data logger.

3: Create an empty results file with headers if it doesn't exist

4: Create an initialisation script that checks login and creates the cache.json file
