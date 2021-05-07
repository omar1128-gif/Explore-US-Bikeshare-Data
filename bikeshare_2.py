import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def check_month(m):
    """
    Checks if the input string is in the array of specified months

    Returns:
        bool - if true then the month is in the array, otherwise it is not valid (False).
    """
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    if m in months:
        return True
    else:
        return False


def convert_day(day_index):
    """
    Checks if the input string is a day of the week

    Returns:
        (str) - day name corresponding to the entered integer
    """
    days = ['sunday', 'monday',
            'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    return days[day_index - 1]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_city = False
    while not valid_city:
        city_input = input(
            'Would you like to see data for Chicago, New York, or Washington? \n').lower()
        if city_input == 'new york':
            city_input += ' city'

        if city_input in CITY_DATA.keys():
            valid_city = True
            print('Looks like you want to hear about {}! If this is not true, restart the program now! \n'.format(
                city_input.title()))
        else:
            valid_city = False
            print('Please enter a valid city name "Choose from the 3 cities" \n')
    city = city_input

    # get user filter (month, day, both, or none)
    print()
    filter_input = input(
        'Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter. \n')

    month, day = '', ''
    if filter_input == 'both':
        valid_month = False
        while not valid_month:
            month = input(
                'Which month? January, February, March, April, May, or June?\n').lower()
            if check_month(month):
                valid_month = True

        valid_day = False
        while not valid_day:
            try:
                day_input = int(
                    input('Which day? Please type your response an an integer(e.g., 1=Sunday).\n'))
                if 1 <= day_input <= 7:
                    valid_day = True

            except ValueError:
                print(
                    'Please enter a valid number representing the day (e.g., 1=Sunday).\n')
        day = convert_day(day_input)

    elif filter_input == 'month':
        valid_month = False
        while not valid_month:
            month = input(
                'Which month? January, February, March, April, May, or June?\n').lower()
            if check_month(month):
                valid_month = True
        day = 'all'

    elif filter_input == 'day':
        valid_day = False
        while not valid_day:
            try:
                day_input = int(
                    input('Which day? Please type your response an an integer(e.g., 1=Sunday).\n'))
                if 1 <= day_input <= 7:
                    valid_day = True
                else:
                    print(
                        'Invalid number, Please enter a number between 1 and 7 "Inclusive"')

            except ValueError:
                print(
                    'Please enter a valid number representing the day (e.g., 1=Sunday).\n')
        day = convert_day(day_input)
        month = 'all'

    elif filter_input == 'none':
        month, day = 'all', 'all'
    else:
        print('Invalid filter was entered, filter will be set to none by default.')
        month, day = 'all', 'all'

    print('-'*40)
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
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month == 'all' and day == 'all':
        return df
    elif month != 'all' and day != 'all':
        return df[(df['month'] == month) & (df['day_of_week'] == day.title())]
    elif month == 'all' and day != 'all':
        return df[(df['day_of_week'] == day.title())]
    elif month != 'all' and day == 'all':
        return df[(df['month'] == month)]


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month: {}\n'.format(df['month'].mode()[0]))

    # display the most common day of week
    print('Most common day: {}\n'.format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print('Most common start hour: {}\n'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station: {}\n'.format(
        df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('Most commonly used end station: {}\n'.format(
        df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print('Most frequent combination of start station and end station trip:\n {}'.format(
        df.groupby(["Start Station", "End Station"]).size().sort_values(ascending=False).head(1)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time: {}\n'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('Mean travel time: {}\n'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User types: \n {}\n'.format(df['User Type'].value_counts()))

    # Display counts of gender
    try:
        print('Gender types: \n{}'.format(df['Gender'].value_counts()))
    except KeyError:
        print("Gender types:\nNo data available.")

    # Display earliest, most recent, and most common year of birth
    try:
        print('Earliest year of birth: {}'.format(df['Birth Year'].min()))
    except KeyError:
        print('Earliest year of birth:\nNo data available')

    try:
        print('Most recent year of birth: {}'.format(df['Birth Year'].max()))
    except KeyError:
        print('Most recent year of birth:\nNo data available')

    try:
        print('Most common year of birth: {}'.format(
            df['Birth Year'].mode()[0]))
    except KeyError:
        print('Most common year of birth:\nNo data available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_row_data(df, n):
    df = df.to_dict(orient='records')
    for i in range(5):
        print(df[n+i], '\n')


def main():
    try:
        while True:
            city, month, day = get_filters()
            df = load_data(city, month, day)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            raw, n = True, 0
            while raw:
                user_answer = input(
                    "Would you like to see 5 lines of raw data? Enter yes or no. \n")
                if user_answer == 'yes':
                    display_row_data(df, n)
                    n += 5
                elif user_answer == 'no':
                    raw = False
                else:
                    print("Invalid entry, please enter yes or no to see raw data.\n")

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
    except KeyboardInterrupt:
        print('\nClosing...')


if __name__ == "__main__":
    main()
