import csv, random
from datetime import *

def split_weekly_hours(days=5, expected_hours=40, offset=5):
    daily_hours = []
    ave_hour = expected_hours / days
    offset = offset / days

    for _ in range(days):
        random_offset = random.uniform(-offset, offset)
        daily_hours.append(round(ave_hour + random_offset, 2))

    return daily_hours

def split_daily_hours(daily_hours=8, two_shift=True, shift_bias=0.5):
    if daily_hours <= 0:
        raise ValueError('daily_hours must be a positive')
    if two_shift:
        base = 0.5 + (0.5 - shift_bias) * 0.4
        morning_fraction = random.uniform(base - 0.1, base + 0.1)
        morning_fraction = max(0.2, min(0.8, morning_fraction))

        morning_hours = round_quarter(daily_hours * morning_fraction)
        afternoon_hours = round_quarter(daily_hours - morning_hours)
        return morning_hours, afternoon_hours
    else:
        if random.random() < shift_bias:
            return daily_hours, 0
        else:
            return 0, daily_hours

def random_start_time(morning=True):
    if morning:
        return random.randint(5, 9)
    else:
        return random.randint(12, 14)

def random_date(weeks_range=52, day=0):
    today = datetime.today()
    offset = (today.weekday() - day) % 7

    rand_week = random.randint(1, weeks_range)
    return today - timedelta(days=offset) - timedelta(weeks=rand_week)

def random_week(empid, working_days=5, expected_hours=40): # populate a week
    timesheet_week = []
    daily_hours = split_weekly_hours(days=working_days, expected_hours=expected_hours)
    start_date = random_date()

    for offset, work_hours in enumerate(daily_hours):
        work_date = start_date + timedelta(days=offset)
        timesheet_week.append(TimeSheet(empid, work_date, work_hours))

    return timesheet_week

def round_fifteen(dt):
    minute = (dt.minute // 15) * 15
    return dt.replace(minute=minute, second=0, microsecond=0)

def round_quarter(hour_float):
    return round(hour_float * 4) / 4

def float_to_hour(hour_float : float) -> time:
    hour_int = int(hour_float)
    min_int = int((hour_float - hour_int) * 60)

    return time(hour_int, min_int)

def generate_shift_time(self, morning=True):
    if morning and self.morning_hours <= 0:
        return None, None
    if not morning and self.afternoon_hours <= 0:
        return None, None

    _hours = self.morning_hours if morning else self.afternoon_hours

    if morning:
        start_hour = random_start_time(morning=True)
    else:
        min_start = 13 # generally the afternoon shift should start at 13
        if self.end_morning:
            min_start = max(13, self.end_morning + 0.5)
        start_hour = random.randint(min_start, 14)

    start_minute = random.choice([0, 15, 30, 45])
    start_time = datetime.combine(self.working_date, time(start_hour, start_minute))

    end_time = start_time + timedelta(hours=_hours)

    if morning:
        max_end_time = datetime.combine(self.working_date, time(13, 0))
        if end_time > max_end_time:
            if random.random() > 0.05:  # make sure that 95% shift end time around 13
                max_hours = (max_end_time - start_time).total_seconds() / 3600
                self.morning_hours = round_quarter(max_hours)
                self.afternoon_hours = round_quarter(self.working_hours - self.morning_hours)
                end_time = start_time + timedelta(hours=self.morning_hours)

    return start_time.time(), end_time.time()



class TimeSheet: # represent an object per working day
    def __init__(self,emp_id,working_date,working_hours=8):
        self.emp_id = emp_id
        self.working_date = working_date
        self.working_hours = working_hours

        if working_hours > 6:
            morning_hours, afternoon_hours = split_daily_hours(working_hours, two_shift=True)
        else:
            morning_hours, afternoon_hours = split_daily_hours(working_hours, two_shift=False)

        self.morning_hours = round_quarter(morning_hours)
        self.afternoon_hours = round_quarter(afternoon_hours)

    def __repr__(self):
        return (f"{self.emp_id} | {self.working_date.date()} | "
                f"Morning: {self.morning_hours}h | Afternoon: {self.afternoon_hours}h")

class WorkingHour:
    def __init__(self, start=None, end=None, morning=True, extra=False):
        self.morning = morning
        self.extra = extra

        if (start is None) != (end is None):
            raise ValueError("Start and end time pair must exist")
        if start is not None and end is not None:
            try:
                start_dt = datetime.strptime(start, "%H:%M")
                end_dt = datetime.strptime(end, "%H:%M")
            except ValueError:
                raise ValueError("Start and end time pair must be in format HH:MM")

            duration = (end_dt - start_dt).total_seconds() / 3600
            if duration < 0 or duration > 12:
                raise ValueError("duration must be between 0 and 12 hours")

            if morning and start_dt.hour > 12:
                raise ValueError("start hour must be before morning hour")

            self.start = start_dt
            self.end = end_dt
        else:
            self.start = None
            self.end = None


if __name__ == '__main__':
    now = datetime.now()
    print("Rounded to 15:", round_fifteen(now))
    print("Random date:", random_date())

    hours = split_weekly_hours()
    print("Raw split:", hours, sum(hours))

    hours = [round_quarter(h) for h in hours]
    print("Quarter split:", hours, sum(hours))

    hours_as_time = [float_to_hour(h) for h in hours]
    print("As times:", hours_as_time)

    print("\nRandom week:")
    week = random_week(empid=101, expected_hours=42)
    for ts in week:
        print(ts)
