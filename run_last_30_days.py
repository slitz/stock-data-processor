import datetime
import subprocess
import time

def get_last_30_business_days():
    today = datetime.date.today()
    dates = []
    current = today
    count = 0
    while count < 30:
        current -= datetime.timedelta(days=1)
        if current.weekday() < 5:  # Monday to Friday (0-4)
            dates.append(current)
            count += 1
    return dates

def main():
    dates = get_last_30_business_days()
    for date in dates:
        date_str = date.isoformat()
        cmd = f"python main.py --date {date_str}"
        print(f"Running: {cmd}")
        subprocess.run(cmd, shell=True)
        time.sleep(10) # request delay to avoid hitting API rate limits

if __name__ == "__main__":
    main()