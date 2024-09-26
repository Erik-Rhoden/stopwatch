import argparse
import time
import json

class Stopwatch:
    def __init__(self):
        self.start_timer = 0
        self.stop_timer = 0

    def formatting(self, elapsed_time):
        remaining_time = elapsed_time
        weeks = int(remaining_time // (60 * 60 * 24 * 7))
        days = int((remaining_time % (60 * 60 * 24 * 7)) // (60 * 60 * 24))
        hours = int((remaining_time % (60 * 60* 24)) // (60 * 60))
        minutes = int((remaining_time % (60 * 60)) // 60)
        seconds = int(remaining_time % 60)
        tenths = int((remaining_time - int(remaining_time)) * 10)

        if seconds < 0:
            return 0
        if seconds == 0:
            return f".{tenths} seconds"
        if minutes == 0:
            return f"00:{seconds}.{tenths} seconds"
        if hours == 0:
            return f"00:{minutes}:{seconds}.{tenths}"
        if days == 0:
            return f"{hours}:{minutes}:{seconds}.{tenths}"
        if weeks == 0:
            return f"{days}d {hours}:{minutes}:{seconds}.{tenths}"
        else:
            return f"{weeks}w {days}d {hours}:{minutes}:{seconds}.{tenths}"

parser = argparse.ArgumentParser(prog="Stopwatch",
                                 description="Provides elapsed time")
parser.add_argument("-s", "--start", help="initializes the timer", action="store_true")
parser.add_argument("-x", "--stop", help="stops timer", action="store_true")
args = parser.parse_args()
stopwatch = Stopwatch()
if args.start:
    stopwatch.start_timer = time.time()
    print("Timer started")
    with open("stopwatch.json", "w") as file:
        json.dump(stopwatch.start_timer, file)
elif args.stop:
    stopwatch.stop_timer = time.time()
    with open("stopwatch.json", "r") as file:
        stopwatch.start_timer = json.load(file)
    elapsed_time = stopwatch.stop_timer - stopwatch.start_timer
    print(stopwatch.formatting(elapsed_time))