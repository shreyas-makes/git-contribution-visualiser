import os
import requests
import numpy as np
import matplotlib.pyplot as plt
import datetime

def fetch_contributions(username):
    token = os.getenv('ACCESS_GITHUB_TOKEN')  
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=180)
    
    contributions_count = {}
    # Loop through each month in the last six months
    for month_offset in range(6):
        month = (start_date.month + month_offset - 1) % 12 + 1
        year = start_date.year + (start_date.month + month_offset - 1) // 12
        url = f"https://api.github.com/users/{username}/events?per_page=100&page=1"
        headers = {'Authorization': f'token {token}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            events = response.json()
            for event in events:
                if event['type'] == 'PushEvent':
                    date_str = event['created_at'][:10]
                    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                    if date >= start_date.date() and date <= end_date.date():
                        contributions_count[date] = contributions_count.get(date, 0) + 1
        else:
            print("Failed to fetch data:", response.status_code)
            return {}

    return contributions_count

def plot_contributions(contributions):
    # Sort the dates
    sorted_dates = sorted(contributions.keys())
    
    # Create a list of counts corresponding to sorted dates
    counts = [contributions[date] for date in sorted_dates]
    
    # Set up the plotting grid
    num_days = (sorted_dates[-1] - sorted_dates[0]).days + 1
    num_weeks = (num_days // 7) + 1
    data = np.zeros((7, num_weeks))
    
    # Fill the data array
    for i, date in enumerate(sorted_dates):
        week = (date - sorted_dates[0]).days // 7
        day = date.weekday()
        data[day, week] = contributions[date]

    # Create the heatmap
    plt.figure(figsize=(10, 2))
    plt.imshow(data, cmap='Greens', aspect='auto')
    plt.axis('off')
    plt.show()

# Example usage
username = 'shreyas-makes'
contributions = fetch_contributions(username)
plot_contributions(contributions)


