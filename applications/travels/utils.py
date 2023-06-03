from datetime import datetime


def check_date_order(start_date, end_date):
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    if start_dt <= end_dt:
        return True
    else:
        return False
