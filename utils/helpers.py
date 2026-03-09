from datetime import datetime
def format_date(date):
    if not date:
        return ""
    return date.strftime("%d %b %Y")