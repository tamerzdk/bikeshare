import time

import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! \n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid
    # inputs
    while True:
        city = input('Please choose a city from the list below:- \n [chicago, new york city, washington] \n')
        if city in CITY_DATA.keys():
            break
        else:
            print('Invalid input! Please try again! \n')

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('Please input a month \n (all, january, february, ... , june) \n').lower()
        if month in MONTHS:
            break
        else:
            print('Invalid input! Please try again! \n')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Please input a day \n (all, monday, tuesday, ... sunday) \n').lower()
        if day in DAYS:
            break
        else:
            print('Invalid input! Please try again! \n')

    print('-' * 40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month)

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe

        df = df.loc[df['day_of_week'].str.lower() == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month_index = df['month'].mode()[0]
    print('Most popular month:', MONTHS[common_month_index])

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most popular day:', common_day)

    # TO DO: display the most common start hour
    common_start_hour = df['Start Time'].dt.hour.mode()[0]
    print('Most popular hour:', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Commonly used start station:', common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Commonly used end station:', common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    common_trip = \
        df.groupby(['Start Station', 'End Station']).size().reset_index().sort_values(by=0, ascending=False).iloc[0]
    print('Commonly used trip from {} to {}'.format(common_trip['Start Station'], common_trip['End Station']))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_trip_duration = (pd.to_datetime(df['End Time']) - df['Start Time']).sum()
    print("Total trip duration is", total_trip_duration)

    # TO DO: display mean travel time
    average_trip_duration = (pd.to_datetime(df['End Time']) - df['Start Time']).mean()
    print("Average trip duration is", average_trip_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df.groupby(['User Type']).size().reset_index(name='count')
    print('Counts of user types \n', user_type)
    print()
    try:
        # TO DO: Display counts of gender
        user_gender = df.groupby(['Gender']).size().reset_index(name='count')
        print('Counts of user types \n', user_gender)
        print()
        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]
        print('earliest, most recent, and most common year of birth:\n {} , {} , {}'.format(earliest_year, most_recent,
                                                                                            common_year))
    except:
        print()
    finally:
        print("This took %s seconds." % (time.time() - start_time))
        print('-' * 40)


def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    if view_data.lower() == 'yes':
        start_loc = 0
        while start_loc < len(df):
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            view_data = input("Do you wish to continue?: ").lower()
            if view_data.lower() != 'yes':
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
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ != "__main__":
    pass
else:
    main()
