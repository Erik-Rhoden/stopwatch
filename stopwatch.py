import argparse
import time
import json
import os

class Stopwatch:
    def __init__(self):
        self.start_timer = 0
        self.stop_timer = 0
        self.elapsed_time = 0

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
group = parser.add_mutually_exclusive_group()
group.add_argument("-s", "--start", help="initializes the timer", action="store_true")
group.add_argument("-x", "--reset", help="resets timer", action="store_true")
group.add_argument("-p", "--pause", help="adds the current time to start_time", action="store_true")
group.add_argument("-r", "--resume", help="resumes timer from elapsed time", action="store_true")
args = parser.parse_args()
stopwatch = Stopwatch()
if args.start:
    if not os.path.exists("pause.json"):
        stopwatch.start_timer = time.time()
        print("Timer started")
        with open("start.json", "w") as file:
            json.dump(stopwatch.start_timer, file)
    else:
        print("Timer in progress")

if args.pause:
    if os.path.exists("start.json"):
        with open("start.json", "r") as file:
            stopwatch.start_timer = json.load(file)
        if stopwatch.start_timer != 0:
            stopwatch.stop_timer = time.time()
            if not os.path.exists("pause.json"):
                stopwatch.elapsed_time = 0
            else:
                with open('pause.json', "r") as file:
                    stopwatch.elapsed_time = json.load(file)
            stopwatch.elapsed_time += stopwatch.stop_timer - stopwatch.start_timer
            with open("pause.json", "w") as file:
                json.dump(stopwatch.elapsed_time, file)
            stopwatch.start_timer = 0
            with open("start.json", "w") as file:
                json.dump(stopwatch.start_timer, file)
            print("Timer Stopped")
            print(stopwatch.formatting(stopwatch.elapsed_time))
        else:
            if os.path.exists('pause.json'):
                with open('pause.json', "r") as file:
                    stopwatch.elapsed_time = json.load(file)
                print(stopwatch.formatting(stopwatch.elapsed_time))
            else:
                print("Timer has not been started")
    else:
        print("Timer does not exist or has not been started")

if args.resume:
    if os.path.exists("pause.json") and os.path.exists("start.json"):
        stopwatch.start_timer = time.time()
        with open("pause.json", "r") as file:
            stopwatch.elapsed_time = json.load(file)
        print("Timer running")
        with open("start.json", "w") as file:
            json.dump(stopwatch.start_timer, file)
    else:
        print("Timer is not paused or Timer does not exist")

if args.reset:
    if os.path.exists("start.json"):
        os.remove("start.json")
    if os.path.exists("pause.json"):
        os.remove("pause.json")
    print("Timer reset")