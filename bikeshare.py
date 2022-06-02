import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import plotly.express as px

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

# Permanently changes the pandas settings
# This setting will change the display of output data on the commandline
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def get_filters():
    """
    Asks user to provide information: city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input("Please enter either 'chicago', 'new york city', or 'washington' - case insencitive. Type 'q' to quit: ")
            if (city.lower() == 'chicago' or city.lower() == 'new york city' or city.lower() == 'washington'):
                print('you enter the city: {}\n'.format(city.lower()))
                break
            elif city.lower() != 'q':
                print("you entered wrong city: {}".format(city.lower()))
            else:
                exit(0)
        except Exception as e:
            print("Someting strange happening {}".format(e))

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("Please enter month 'Jan', 'Feb', 'Mar', 'Apr', "
                          "'May', 'Jun', or 'All'. Type 'q' to quit: ")
            if (month.lower() == 'jan' or month.lower() == 'feb' or month.lower() == 'mar'
            or month.lower() == 'apr' or month.lower() == 'may' or month.lower() == 'jun'
            or month.lower() == 'all'):
                print('you entered the month: {}'.format(month.lower()))
                break
            elif month.lower() != 'q':
                print("you entered wrong month: {}".format(month.lower()))
            else:
                exit(0)
        except Exception as e:
            print("Something strnage happening {}".format(e))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nPlease enter either Sun, Mon, Tue, Wed, Thu, Fri, Sat, or All - Type 'q' to quit: ")
        if (day.lower() == 'sun' or day.lower() == 'mon' or day.lower() == 'tue' or
            day.lower() == 'wed' or day.lower() == 'thu' or day.lower() == 'fri' or
            day.lower() == 'sat' or day.lower() == 'all'):
            print('you entered the day: {}'.format(day.lower()))
            break
        elif  day.lower() != 'q':
            print("You entered wrong day: {}".format(day.lower()))
        else:
            exit(0)

    print('You entered city <{}>, month <{}>, day of week <{}>.'.format(city.lower(), month.lower(), day.lower()))
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

    "add two new columns (month, day of week) to the data frame "
    "so that the program can filter based on month and day of week"
    print(city, month, day)
    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour_of_day'] = df['Start Time'].dt.hour

    "The following converts the short input to long input for month"
    if month != 'all':
        if month == 'jan':
            month_long = 'january'
        elif month == 'feb':
            month_long = 'february'
        elif month == 'mar':
            month_long = 'march'
        elif month == 'apr':
            month_long = 'april'
        elif month == 'may':
            month_long = 'may'
        else:
            month_long = 'june'

        # get the correct month to be filtered
        months_long = ['january', 'february', 'march', 'april', 'may', 'june']
        month_long = months_long.index(month_long) + 1
        df = df[df['month'] == month_long]

    if day != 'all':
        if day == 'mon':
            day_long = 'monday'
        elif day == 'tue':
            day_long = 'tuesday'
        elif day == 'wed':
            day_long = 'wednesday'
        elif day == 'thu':
            day_long = 'thursday'
        elif day == 'fri':
            day_long = 'friday'
        elif day == 'sat':
            day_long = 'saturday'
        else:
            day_long = 'sunday'

        'filter the date frame by week of day'
        df = df[df['day_of_week'] == day_long.title()]

    'This print 5 rows at a time, change all 5s to 10s if you want to print 10 rows at a time'
    'This also can be changed to a function which take df and n as parameter'
    number_of_loops = int(len(df)/5) + 1
    i = 0
    j = 5
    loop_counter = 1
    while True:
        question = input("Do you want to see the data 5 at a time? 'y' to continue, 'n' to proceed: ")
        if (question.lower() == 'y' and loop_counter < number_of_loops):
            print(df.iloc[i:j, ])
            loop_counter += 1
            i += 5
            j += 5
        elif question.lower() != 'n':
            print("Please answer 'y' or 'n'")
        elif (question.lower() == 'y' and loop_counter == number_of_loops):
            print(df.iloc[i: len(df)+1, ])
            break
        else:
            break

    print('-' * 40)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print("most common month is: <{}>".format(popular_month))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("most common day of week is: <{}>".format(popular_day))

    # display the most common start hour
    popular_hour = df['hour_of_day'].mode()[0]
    print("most common start hour is: <{}>".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    df['Start_End_Station'] = df['Start Station'] + "|" + df['End Station']
    # display most commonly used start station
    most_commonly_used_start_station = df['Start Station'].mode()[0]
    print("Most common used start station is: <{}>\n".format(most_commonly_used_start_station))

    # display most commonly used end station
    most_commonly_used_end_station = df['End Station'].mode()[0]
    print("most commonly used end station is: <{}>\n".format(most_commonly_used_end_station))

    # display most frequent combination of start station and end station trip
    most_frequent_combination_of_start_and_end_station = df['Start_End_Station'].mode()[0]
    print("most frequent combination of start and end station is: <{}>".format(most_frequent_combination_of_start_and_end_station))

    top_most_popular_start_station = df['Start Station'].mode()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['timediff'] = df['End Time'] - df['Start Time']
    #print('*' * 50)
    #print(df.head(10))
    #print('*' * 50)

    # display total travel time
    total_travel_time = df['timediff'].sum()
    print("total travel time is: <{}>".format(total_travel_time))

    # display mean travel time
    average_travel_time = df['timediff'].mean()
    print("Average travel time is: <{}>".format(average_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_of_user_types = Counter(df['User Type'])
    print("counts of user types are:")
    print(*counts_of_user_types.items(), sep='\n')

    # Display counts of gender
    #if 'Gender' in df.columns:
    try:
        counts_of_gender = Counter(df['Gender'])
        print("\ncounts of genders are:")
        print(*counts_of_gender.items(), sep='\n')
    except Exception as e:
        print("exception caught: {}".format(e))

    #else:
        #print("There is no Gender information in this city.")

    # Display earliest, most recent, and most common year of birth
    try:
        print("\nDisplay earliest, most recent, and most common year of birth")
        earliest_birthyear = int(df['Birth Year'].dropna().min())
        print("earliest birthyear is: <{}>".format(earliest_birthyear))

        most_recent_birthyear = int(df['Birth Year'].dropna().max())
        print("most recent birthyear is: <{}>".format(most_recent_birthyear))

        most_common_birthyear = int(df['Birth Year'].dropna().mode())
        print("most common birthyear is: <{}>".format(most_common_birthyear))
    except Exception as e:
        print("exception caught: {}".format(e))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def more_stats(df):
    """
        display graphic statistics: boxplot, bor graph etc
        display top 10 and botton 10 of certain data

        Args:
            (dataframe) df - city data
        Returns:
            nothing.
        """

    "The following print out the boxplot of age distribution of a particular city"
    try:
        print("This is the age distribution")
        box_plot = px.box(df['Birth Year'].dropna(), x="Birth Year", title="boxplot of Birth Year")
        box_plot.show()
    except Exception as e:
        print("Caught expection: {}".format(e))

    "The following displays the top 10 start station"
    try:
        print("This is the top 10 start stations: ")
        all_start_stations = Counter(df['Start Station'])
        top_10_start_station = all_start_stations.most_common(10)
        print("top 10 start stations are: {}".format(top_10_start_station))
        plt.plot(*zip(*top_10_start_station))
        plt.xticks(rotation = 90)
        plt.title("Top 10 start stations")
        plt.show()
    except Exception as e:
        print("Something wrong: {}".format(e))


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)


        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        more_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
