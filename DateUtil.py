from datetime import datetime, timedelta

def to_string(date):
    return date.strftime('%Y-%m-%d')

def nearest_friday_of(datetime):
    selected_date = datetime.date()
    
    # Moving back to Friday if the date falls on a weekend
    if selected_date.weekday() == 5: # Saturday
        selected_date = selected_date - timedelta(days=1)
    elif selected_date.weekday() == 6: # Sunday
        selected_date = selected_date - timedelta(days=2)
    
    return datetime.combine(selected_date, datetime.time())

def next_day_of(datetime):
    return datetime + timedelta(days=1)