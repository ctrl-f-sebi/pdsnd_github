# -*- coding: utf-8 -*-
"""bikeshare.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BOHEXEXK-seYUgmKhnBdiGDSguzzdi7t
"""

#original file is Google colab, below 2 lines of code required to load files from within Google drive
#this enables me to run python without installing software on local device
#from google.colab import drive 
#drive.mount('/content/gdrive')

import time
import pandas as pd
import numpy as np

#commented out the original location of the csv files, for colab I can just host them in drive

#CITY_DATA = { 'chicago': 'gdrive/My Drive/chicago.csv',
#              'new york': 'gdrive/My Drive/new_york_city.csv',
#              'new york city': 'gdrive/My Drive/new_york_city.csv',
#              'washington': 'gdrive/My Drive/washington.csv'}

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

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
    
    # showing the input field to users and converting the city variable to lower case
    city = input('You can choose between Chicago, New York City and Washington, type in the city you would like to look at: ')
    city = city.lower()

    # adding a while loop to handle wrong input, again converting input to lowercase 
    while city not in CITY_DATA:
        city = input('Uuups, something is wrong with your input. Try Chicago, New York City and Washington: ')
        city = city.lower()
    
    #print selection (mostly for me to validate)
    print('you selected {}'.format(city).title())
       
    #get user input for month (all, january, february, ... , june)
    m = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = input('Fill in the field with a month (e.g. May) from January to June or type all: ')
    month = month.lower()
    while month not in m:
        month = input('Invalid input, please only use months between January and June or type all, watch spelling: ')
        month = month.lower()
    
    #print selection (mostly for me to validate)
    print('you selected {}'.format(month).title())
    
    #get user input for day of week (all, monday, tuesday, ... sunday)
    d = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    day = input('Type any day between Monday and Sunday or simply type all: ')
    day = day.lower()
    while day not in d:
        day = input('Something was wrong with the input, please only use names of weekdays (e.g. Sunday) or type all: ')
        day = day.lower()

    #print selection (mostly for me to validate)
    print('you selected {}'.format(day).title())

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

    #creating/loading data frame from above CSVs. getting a single table
    df = pd.read_csv(CITY_DATA[city])

    #converting starttime to datetime / timestamp format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #creating a month column, should include integers between 1 and 6
    df['month'] = df['Start Time'].dt.month

    #creating a weekday columnm should include integers between 0 and 6
    df['weekday'] = df['Start Time'].dt.dayofweek

    #creating column for hour of day (will need for stats later)
    df['hour'] = df['Start Time'].dt.hour

    #printing to see if df looks correct
    print(df.head())

    #applying converting month inputs to indices, so the filter works
    if month != 'all':
        m = ['january', 'february', 'march', 'april', 'may', 'june']
        month = m.index(month) + 1
        df = df[df['month'] == month]

    #same for days, Monday is 0 so I don't need to add 1 to the index
    if day != 'all':
        d = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = d.index(day)
        df = df[df['weekday'] == day]
    
    #printing another test table to see if filters worked
    print(df.head())

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    #display the most common month

    #get mode and store in variable
    mode_month = df['month'].mode()[0]
    #add list of months to reference in print later
    m = ['january', 'february', 'march', 'april', 'may', 'june']
    #print the most common month and format into title
    print('{} is the month with most people cycling.'.format(m[mode_month-1].title()))

    
    
    #display the most common day of week => same as for month
    mode_day = df['weekday'].mode()[0]
    d = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    print('People seem to use bikesharing the most on {}s.'.format(d[mode_day].title()))

    
    
    #display the most common start hour => same as for month
    mode_hour = df['hour'].mode()[0]
    print('The busiest time of the day is {} hours'.format(mode_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    mode_s_station = df['Start Station'].mode()[0]
    
    #display most commonly used end station
    mode_e_station = df['End Station'].mode()[0]
    
    # print both stations in the same sentence, with conditional statement
    if mode_s_station == mode_e_station:
      print('{} is both, the most popular start and end station'.format(mode_s_station))
    else:
      print('{} is the most popular start station and {} is the most popular end station.'.format(mode_s_station, mode_e_station))


    #display most frequent combination of start station and end station trip
    df['start_finish'] = df['Start Station'] + ' AND ' + df['End Station']
    mode_station_combi = df['start_finish'].mode()[0]
    print('The most popular route is between {}'.format(mode_station_combi))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    # storing sum of duration to variable
    tot_travel_time = df['Trip Duration'].sum()
    #printing result in text and rounding to 2 decimals
    print('{} is the total travel time.'.format(round(tot_travel_time,2)))

    
    
    #display mean travel time
    #storing mean of duration to variable
    mean_travel_time = df['Trip Duration'].mean()
    #printing result in text and rounding to 2 decimals
    print('{} is the average travel time.'.format(round(mean_travel_time,2)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    #assign a variable to the unique users within 
    u_type = df['User Type'].value_counts()
    u_type_rel = round(df['User Type'].value_counts(normalize = True),2)
    print('Distribution of different user types:')
    print(u_type,'\n')
    print('In relative terms that is:')
    print(u_type_rel,'\n')
    
    
    
    #Display counts of gender
    # if statement since this information is not available for Washington
    if 'Gender' in df.columns:
        #create a variable and store the count of values assigned to it
        gender = df['Gender'].value_counts()
        gender_rel = round(df['Gender'].value_counts(normalize = True),2)
        #print header for data as well as the results, results should be printed across 2 lines
        print("Let's look into the distribution of different genders:")
        print(gender,'\n')
        print('In relative terms that is:')
        print(gender_rel, '\n')
    else:
      print("Unfortunately, we don't have and data on gender. You can try a different city")

 
    #Display earliest, most recent, and most common year of birth 
    if 'Birth Year' in df.columns:
        min_year = int(df['Birth Year'].min())
        max_year = int(df['Birth Year'].max())
        mode_year = int(df['Birth Year'].mode()[0])
        print("Here is some info on the users' age:")
        print('The oldest user was born in {}'.format(min_year))
        print('The youngest user was born in {}'.format(max_year))
        print('{} is the most common birth year among users'.format(mode_year))
    else:
        print("Unfortunately, we don't have and data on birth years. You can try a different city")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#function to display 5 rows of raw data 
def display_data(df):

    #get input from user and set to lower case
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    view_data = view_data.lower()

    #index for first row of data
    start_loc = 0

    #while loop to iterate through responses until they are not yes
    while view_data in ('yes', 'y'):

      #print 5 rows of data using start_loc variable as starting point and adding 5 to the index in case users want to see more
      print(df.iloc[start_loc:start_loc+5])
      start_loc += 5
      view_data = input("Do you wish to continue?: ").lower()

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
        if restart.lower() not in ('yes', 'y'):
            break


if __name__ == "__main__":
	main()