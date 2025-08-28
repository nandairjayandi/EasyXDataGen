import csv
import random
from datetime import datetime, timedelta

def round_to_15(dt):
    minute = (dt.minute // 15) * 15
    return dt.replace(minute=minute, second=0, microsecond=0)

def random_monday(max_weeks_back=52):
    today = datetime.today()
    last_monday = today - timedelta(days=today.weekday())
    weeks_back = random.randint(0, max_weeks_back)
    past_monday = last_monday - timedelta(weeks=weeks_back)
    return past_monday

def generate_week_timesheet(empid, start_date=None):
    """
    Generate a timesheet for one week for a given employee ID.
    - start_date: optional Monday; if None, pick a random past Monday
    Returns list of rows: [empid, date, startMorning, endMorning, startAfternoon, endAfternoon, extraHour]
    """
    if start_date is None:
        start_date = random_monday()

    timesheet = []

    # Total weekly hours target: 50 ±5
    total_hours = 50 + random.randint(-5, 5)
    daily_hours = [8 for _ in range(5)]  # 5 weekdays
    scale = total_hours / sum(daily_hours)
    daily_hours = [round(h * scale, 2) for h in daily_hours]

    for i in range(5):
        date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        work_hours = daily_hours[i]

        extra_hour = 2 if random.random() < 0.01 else 0
        total_daily_hours = work_hours + extra_hour

        # Split into morning and afternoon (~half-half)
        morning_hours = round(total_daily_hours / 2 + random.uniform(-0.25, 0.25), 2)
        afternoon_hours = round(total_daily_hours - morning_hours, 2)

        # Random start times around standard
        start_morning = datetime.strptime("09:00", "%H:%M") + timedelta(minutes=random.randint(-15,15))
        end_morning = start_morning + timedelta(hours=morning_hours)

        start_afternoon = datetime.strptime("13:00", "%H:%M") + timedelta(minutes=random.randint(-15,15))
        end_afternoon = start_afternoon + timedelta(hours=afternoon_hours)

        start_morning = round_to_15(start_morning)
        end_morning = round_to_15(end_morning)
        start_afternoon = round_to_15(start_afternoon)
        end_afternoon = round_to_15(end_afternoon)

        timesheet.append([
            empid,
            date,
            start_morning.strftime("%H:%M"),
            end_morning.strftime("%H:%M"),
            start_afternoon.strftime("%H:%M"),
            end_afternoon.strftime("%H:%M"),
            extra_hour
        ])

    return timesheet

def save_week_timesheet_csv(timesheet, filename='timesheet.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['empid', 'date', 'startMorning', 'endMorning', 'startAfternoon', 'endAfternoon', 'extraHour'])
        writer.writerows(timesheet)

if __name__ == "__main__":
    empid = "123456"
    week_timesheet = generate_week_timesheet(empid)
    save_week_timesheet_csv(week_timesheet, 'week_timesheet.csv')
    print("Weekly timesheet CSV generated for empid:", empid)
