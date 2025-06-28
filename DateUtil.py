from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

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

def past_month_dates(date = datetime.now(), num_of_months = 12):
    dates_list = []
    current_date = date
    
    for _ in range(num_of_months):
        calc_date = nearest_friday_of(current_date)
        dates_list.append(calc_date)
        current_date -= relativedelta(months=1)
        
    return sorted(dates_list)

def date_from(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d")