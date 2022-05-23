import time
import pandas as pd
import numpy as np

#Creating a dictionary containing the data sources for the three cities
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

#Function to filter the inputs of the user
def get_filters():
    """
    Asks user to choose a city, month, and day to analyze.

    Returns:
        str (city): name of the city to analyze
        str (month): name of the month to filter by, or "all" to apply no month filter
        str (day): name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #Running this loop to ensure the correct user input gets selected else repeat
    while True:
        cities= ['chicago','new york city','washington']
        print("\nWelcome to this program. Which city would you like to analyse?")
        print("\n1. Chicago 2. New York City 3. Washington")
        #Taking user input and convert them into lower to make the imput CASE INSENSITIVE.
        # We 'll do this lower functions again with month filter and day_of_week filter for same purpose.
        city = input().lower()

        if city in cities:
            break
        else:
                print("\nPlease check your input and enter a valid city name.")

    print("\nYou have chosen {} to analyse.".format(city.title()))

    #Creating a list to store all the months including the 'all' option
    while True:
        months= ['january','february','march','april','june','may','all']
        month = input("\n Which month would you like to consider? \n 1.January 2.February 3.March 4.April 5.May 6.June?\n Type 'All' for no month filter. \n").lower()
        if month in months:
            break
        else:
            print("\n Please enter a valid month")


    print("\nYour chosen month to analyze is: {}.".format(month.title()))

    #Creating a list to store all the days including the 'all' option
    while True:
        DAY_LIST = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
        day = input("\nPlease enter a day in the week of your choice for which you're seeking the data:\n 1.Monday 2. Tuesday 3.Wednesday 4.Thursday 5.Friday 6.Saturday 7.Sunday\n Type 'All'for no day in the week filter. \n").lower()
        if day in DAY_LIST:
            break
        else:
            print("\n Please enter a valid day")


    print("\nYou have chosen {} as your day of week to seek data.".format(day.title()))
    print("\nYou have chosen to view data for city: {}, month: {} and day: {}.".format(city.upper(), month.title(), day.title()))
    print('-'*100)
    #Returning the city, month and day selections for the function get_filters
    return city, month, day

#Function to load data from 3 .csv files
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        param1 (str): name of the city to analyze
        param2 (str): name of the month to filter by, or "all" to apply no month filter
        param3 (str): name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df: Pandas DataFrame containing city data filtered by month and day
    """
    #Load data file into dataframe
    print("\nLoading. Please wait a moment...")
    df = pd.read_csv(CITY_DATA[city])

    #Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    #Filter by month if applicable
    if month != 'all':
        #Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #Filter by month to create the new dataframe
        df = df[df['month'] == month]

    #Filter by day of week if applicable
    if day != 'all':
        #Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    #Returns the selected file as a dataframe (df) with relevant columns
    return df

#Function to calculate all the time-related statistics for the chosen data
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]

    print("\nMost Popular Month: {}".format(popular_month))

    #display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    print("\nMost Popular Day: {}".format(popular_day))

    #Extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    #Uses mode method to find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print("\nMost Popular Start Hour: {}".format(popular_hour))

    #Prints the time taken to perform the calculation
    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*100)

#Function to calculate station related statistics
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Uses mode method to find the most common start station
    common_start_station = df['Start Station'].mode()[0]

    print("The most commonly used start station: {}".format(common_start_station))

    #Uses mode method to find the most common end station
    common_end_station = df['End Station'].mode()[0]

    print("\nThe most commonly used end station: {}".format(common_end_station))

    #display most frequent combination of start station and end station trip
    most_popular_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()

    print("\nThe most frequent combination of trips are from {}.".format(popular_combine_trip))

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*100)

#Function for trip duration related statistics
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Uses sum method to calculate the total trip duration
    total_duration = df['Trip Duration'].sum()
    #Finds out the duration in minutes and seconds format
    minute, second = divmod(total_duration, 60)
    #Finds out the duration in hour and minutes format
    hour, minute = divmod(minute, 60)
    print("The total trip duration is {} hours, {} minutes and {} seconds.".format(hour, minute, second))

    #display mean travel time using mean method
    average_duration = round(df['Trip Duration'].mean())
    mins, sec = divmod(average_duration, 60)
    #This filter prints the time in hours, mins, sec format if the mins exceed 60
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print("\nThe average trip duration is {} hours, {} minutes and {} seconds.".format(hrs,mins,sec))
    else:
        print("\nThe average trip duration is {} minutes and {} seconds.".format(mins,sec))

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*100)

#Function to calculate user statistics
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_type = df['User Type'].value_counts()

    print("The types of users by number are given below:\n\n{}".format(user_type))

    #This try clause is implemented to display the numebr of users by Gender
    #However, not every df may have the Gender column (if user choose imput city is Washington)
    try:
        gender = df['Gender'].value_counts()
        print("\nThe types of users by gender are given below:\n\n{}".format(gender))
    except:
        print("\nThere is no 'Gender' information in this city data file.")
    # Birth_year data seeking
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        pop_year = int(df['Birth Year'].mode()[0])
        print("\nThe earliest year of birth: {}\n\nThe most recent year of birth: {}\n\nThe most common year of birth: {}".format(earliest, recent, pop_year))
    except:
        print("There are no birth year details in this city data file.")

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*100)

#Function to display the data frame itself as per user request
def display_data(df):
    """Displays 5 rows of data from the csv file for the selected city.
    """
    pd.set_option('display.max_columns',200)
    while True:
        response=['yes','no']
        choice= input("Would you like to view individual trip data (5 entries)? Type 'yes' or 'no'\n").lower()
        if choice in response:
            if choice=='yes':
                start=0
                end=5
                data = df.iloc[start:end,:9]
                print(data)
            break
        else:
            print("Please enter a valid response")
    if  choice=='yes':
            while True:
                choice_2= input("Would you like to view more trip data? Type 'yes' or 'no'\n").lower()
                if choice_2 in response:
                    if choice_2=='yes':
                        start+=5
                        end+=5
                        data = df.iloc[start:end,:9]
                        print(data)
                    else:
                        break
                else:
                    print("Please enter a valid response")


    print('-'*100)

#Main function to call all the previous functions
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to try another analysis? Enter Yes or No.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
