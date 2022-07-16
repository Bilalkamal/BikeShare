import time
import pandas as pd
import numpy as np
import math

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

cities_list = ["chicago", "new york city", "washington", "c", "w", "nyc"]
months_all = ["all", "january", "february", "march", "april", "may", "june"]
months = ['january', 'february', 'march', 'april', 'may', 'june']
days_all = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
            'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input("Please pick a city: Chicago, New York City, or Washington: ").lower()
    # TODO: Create an autocorrection

    while city not in cities_list:
        print("Please enter a valid city name\n")
        city = input("Please pick a city: Chicago(C), New York City(NYC), or Washington(W): ").lower()

    if city == "w":
        city = "washington"
    elif city == "c":
        city = "chicago"
    elif city == "nyc":
        city = "new york city"

    print(f'It seems you want to see data about {city.title()}.')

    # get user input for month (all, january, february, ... , june)

    month = input("Please pick a month: January --> June, or type All to get data about all months: ").lower().strip()

    while month not in months_all:
        print("Please enter a valid month \n")
        month = input("Please pick a month: January --> June, or type All to get data about all months: ").lower().strip()
    print(f'It seems you want to see data about {month.title()}.')

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day = input("Please pick a day: Friday --> Thursday, or type All to get data about all days: ").lower().strip()
    while day not in days_all:
        print("Please enter a valid day\n")
        day = input("Please pick a day: Friday --> Thursday, or type All to get data about all days: ").lower().strip()
    print(f'It seems you want to see data about {day.title()}.')

    print('-' * 60)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        month = months.index(month) + 1

        df = df[df['Month'] == month]

    if day != 'all':
        df = df[df['Day of Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month = df['Month'].mode()[0]
    print(f'The most common month is: {months[month-1]}')
    # display the most common day of week
    day = df['Day of Week'].mode()[0]
    print(f'The most common day of week is: {day}')
    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    pop_hour = df['Hour'].mode()[0]
    print(f'The most common start hour is: {pop_hour}')

    end_time = time.time()
    print(f"\nThis took {round(end_time - start_time,3)} seconds.\n")
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start_st = df['Start Station'].mode()[0]
    print(f'The most popular start station is: {pop_start_st}')
    # display most commonly used end station
    pop_end_st = df['End Station'].mode()[0]
    print(f'The most popular end station is: {pop_end_st}')
    # display most frequent combination of start station and end station trip
    pop_trip = df['Start Station'] + ' to ' + df['End Station']
    print(f'The most popular trip is: from {pop_trip.mode()[0]} ')

    end_time = time.time()
    print(f"\nThis took {round(end_time - start_time,3)} seconds.\n")
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time is", df['Trip Duration'].sum(), "\n")
    # display mean travel time
    print("The total mean time is", df['Trip Duration'].mean(), "\n")

    end_time = time.time()
    print(f"\nThis took {round(end_time - start_time,3)} seconds.\n")
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()

    print(f"The types of users by number are:\n{user_type}")

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print(f"\nThe types of users by gender are:\n{gender}")
    except:
        print("Gender data is missing!")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        com_year = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest year of birth: {earliest}\nThe most recent year of birth: {recent}\nThe most common year of birth: {com_year}")
    except:
        print("Birth year data is missing!")

    end_time = time.time()
    print(f"\nThis took {round(end_time - start_time,3)} seconds.\n")
    print('-' * 40)


def display_data(df):
    raw = input('\nWould you like to display raw data? (Yes / No)\n')
    if raw.lower() == 'yes':
        count = 0
        while True:
            print(df.iloc[count: count + 5])
            count += 5
            ask = input('Next 5 raws?')
            if ask.lower() != 'yes':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart?(Yes / No)\n')
        if (restart.lower() != 'yes') or (restart.lower() != 'y'):
            break


if __name__ == "__main__":
    main()
