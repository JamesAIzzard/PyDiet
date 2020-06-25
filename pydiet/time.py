from datetime import datetime

class TimeIntervalParseError(Exception):
    def __init__(self, *args):
        if len(args) and args[0]:
            super().__init__(args[0])

class TimeIntervalValueError(Exception):
    def __init__(self, *args):
        if len(args) and args[0]:
            super().__init__(args[0])   

class TimeValueError(Exception):
    def __init__(self, *args):
        if len(args) and args[0]:
            super().__init__(args[0])   

def parse_time_interval(time_interval: str) -> str:
    # Split the string into two parts about the hyphen;
    start_and_end_time = time_interval.split('-')
    # Check there are two parts;
    if not len(start_and_end_time) == 2:
        raise TimeIntervalParseError
    # Format the time into double digit 24hr format;
    for n, t in enumerate(start_and_end_time):
        start_and_end_time[n] = parse_time(t)
    # Check the intervals are not the same;
    if start_and_end_time[0] == start_and_end_time[1]:
        raise TimeIntervalValueError
    # Return the interval;
    return '-'.join(start_and_end_time)

def parse_time(time_interval:str) -> str:
    # Try format the time into double digit 24hr format;
    try:
        d = datetime.strptime(time_interval, "%H:%M")
        return d.strftime("%H:%M")
    except ValueError:
        raise TimeValueError