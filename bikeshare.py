import time
import pandas as pd
import numpy as np

# Data file paths
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" for no month filter
        (str) day - name of the day of the week to filter by, or "all" for no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city
    while True:
        city = input("Which city would you like to explore: Chicago, New York City, or Washington? ").strip().lower()
        if city in CITY_DATA:
            break
        print("Invalid input. Please enter Chicago, New York City, or Washington.")

    # Get user input for month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Which month? January, February, March, April, May, June, or 'all' for no filter: ").strip().lower()
        if month in months:
            break
        print("Invalid input. Please enter a valid month or 'all'.")

    # Get user input for day of the week
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or 'all' for no filter: ").strip().lower()
        if day in days:
            break
        print("Invalid input. Please enter a valid day or 'all'.")

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and applies filters by month and day if applicable.

    Args:
        city (str): The city name to load data for.
        month (str): The month to filter by, or "all" for no filter.
        day (str): The day of the week to filter by, or "all" for no filter.

    Returns:
        pd.DataFrame: Filtered data for the specified city, month, and day.
    """
    # Load data
    df = pd.read_csv(CITY_DATA[city])

    # Convert Start Time column to datetime and extract time-related features
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df = df.assign(
        month=df['Start Time'].dt.month_name().str.lower(),
        day_of_week=df['Start Time'].dt.day_name().str.lower(),
        hour=df['Start Time'].dt.hour
    )

    # Apply filters
    filters = []
    if month != 'all':
        filters.append(df['month'] == month)
    if day != 'all':
        filters.append(df['day_of_week'] == day)
    
    if filters:
        df = df.loc[np.logical_and.reduce(filters)]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Most common month
    print(f"Most common month: {df['month'].mode()[0].capitalize()}")

    # Most common day of the week
    print(f"Most common day of the week: {df['day_of_week'].mode()[0].capitalize()}")

    # Most common start hour
    print(f"Most common start hour: {df['hour'].mode()[0]}")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Most common start station
    print(f"Most common start station: {df['Start Station'].mode()[0]}")

    # Most common end station
    print(f"Most common end station: {df['End Station'].mode()[0]}")

    # Most common trip
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    print(f"Most common trip: {df['trip'].mode()[0]}")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        df (pd.DataFrame): The DataFrame containing trip data.
    """
    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # Calculate total and average travel time
    total_hours = df['Trip Duration'].sum() / 3600
    average_minutes = df['Trip Duration'].mean() / 60

    # Display results
    print(f"Total travel time: {total_hours:.2f} hours")
    print(f"Average travel time: {average_minutes:.2f} minutes")

    print(f"\nExecution time: {time.time() - start_time:.2f} seconds.")
    print("-" * 40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # User types
    print("User Types:")
    print(df['User Type'].value_counts())

    if city != 'washington':
        # Gender counts
        print("\nGender Counts:")
        print(df['Gender'].value_counts())

        # Birth year statistics
        print("\nBirth Year Stats:")
        print(f"Earliest birth year: {int(df['Birth Year'].min())}")
        print(f"Most recent birth year: {int(df['Birth Year'].max())}")
        print(f"Most common birth year: {int(df['Birth Year'].mode()[0])}")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def display_raw_data(df):
    start = 0
    while True:
        raw_data = input("Would you like to see 5 rows of raw data? Enter yes or no: ").strip().lower()
        if raw_data == 'yes':
            print(df.iloc[start:start + 5])
            start += 5
        elif raw_data == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input("\nWould you like to restart? Enter yes or no: ").strip().lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()
