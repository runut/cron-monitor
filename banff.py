import requests
from datetime import datetime, timedelta
from email_sender import send_email 


def filter_dates_with_consecutive_days(dates_list):
    # Convert the list to tuples of (label, date)
    dates = [(item.split(": ")[0], datetime.strptime(item.split(": ")[1], "%Y-%m-%d")) for item in dates_list]

    # Sort dates by the date
    dates.sort(key=lambda x: x[1])

    # Function to check if there's at least one pair of consecutive days
    def has_consecutive_dates(dates, date):
        for i in range(0, len(dates)):
            if date == dates[i][1]:
                if i > 0:
                    if dates[i - 1][1] == date - timedelta(days=1):
                        return True
                if i < len(dates) - 1:
                    if dates[i + 1][1] == date + timedelta(days=1):
                        return True
        return False

    # Filter the list to keep only items with at least one consecutive pair of dates
    new_datas_list = []
    for item in dates_list:
       date = datetime.strptime(item.split(": ")[1], "%Y-%m-%d")
       if has_consecutive_dates(dates, date):
           new_datas_list.append(item)
    return new_datas_list

def avai_checker():
  # Set the end date
  end_date = datetime.strptime("2025-09-15", "%Y-%m-%d")
  # Get the current date + 1 day
  current_date = datetime.now() + timedelta(days=1)
  start_date = datetime.strptime("2025-05-17", "%Y-%m-%d")
  if current_date > start_date:
    start_date = current_date

  if start_date < end_date:
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    # Define the URL with the current start date
    name_id_map = {
       "Two Jack Lakeside": -2147483606,
       "Tunnel Mountain - Village 2": -2147483611,
      #  "Two Jack Lakeside Tent": -2147483604,
    }
    date_avai = []
    headers = {
        "Host": "reservation.pc.gc.ca",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    for name, id in name_id_map.items():
      url = f'https://reservation.pc.gc.ca/api/availability/map?mapId={id}&bookingCategoryId=1&startDate={start_date_str}&endDate={end_date_str}&getDailyAvailability=true&isReserving=true'
      r = requests.get(url, headers=headers)
      if r.status_code == 200:
        data = r.json()
        map_availabilities = data["mapAvailabilities"]
        current_date = start_date
        for availability in map_availabilities:
          avi_date = current_date.strftime("%Y-%m-%d")
          if availability == 0 and avi_date in ['2025-05-17', '2025-05-18', '2025-06-28', '2025-06-29', '2025-06-30', '2025-08-02', '2025-08-03']:
              date_avai.append(name + ": " + current_date.strftime("%Y-%m-%d"))
          elif availability == 0 and current_date.weekday() in [4, 5, 6]:  # 4 is Firday, 5 is Saturday
              date_avai.append(name + ": " + current_date.strftime("%Y-%m-%d"))
          current_date += timedelta(days=1)
    # url = 'https://reservation.pc.gc.ca/api/availability/map?mapId=-2147483606&startDate=2024-08-24&endDate=2024-08-25&getDailyAvailability=false&isReserving=true'
    # r = requests.get(url)
    # if r.status_code == 200:
    #   data = r.json()
    #   map_availabilities = data["mapAvailabilities"]
    #   for availability in map_availabilities:
    #     if availability == 0:
    #       date_avai.append("Tent: 2024-08-24")
  # date_avai.append("Tent: 2024-08-24")
  # date_avai.append("Tent: 2024-08-22")
  if len(date_avai) > 0:
    date_avai = filter_dates_with_consecutive_days(date_avai)
  return {
    "avai": False if len(date_avai) == 0 else True,
    "date": str(date_avai)
  }

def main():
    result = avai_checker()
    if result["avai"]:
        subject = "Banff Campsite Available!"
        body = f"Banff Campsite is available on the following days: {result['date']}"
        print(body)
        send_email(subject, body)
    else:
        print("Banff Campsite is not available.")

if __name__ == "__main__":
    main()
    # send_email("test", "test")
    

