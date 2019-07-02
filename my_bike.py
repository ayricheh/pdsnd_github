import pandas as pd
import time


cities = {1: 'chicago', 2: 'new york city', 3: 'washington'}
months = {0: 'All', 1 : 'January', 2 : 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12:'December'}
days = {0: 'All', 1 : 'Monday', 2 : 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    print("Welcome to Bikeshare analysis")
    print(cities)

    while True:
        try:
            choice_c = int(input(" please select the city you wish to explore [choose: 1, 2 or 3]: \n>"))
            if choice_c not in range(1,4):
                print(" that is not a valid option")
            elif choice_c in range(1, 4):
                city = cities[(choice_c)]
                break
        except ValueError:
            print(" your choice should be in numbers")
            continue

    print(city)
    print('\n' + '.-' * 20 + '\n' )


    print (" PLEASE SELECT ONE OF THE FOLLOWING OPTIONS: \n"+
        "        1: January           7: July\n"+
        "        2: February          8: August\n"+
        "        3: March             9: September\n"+
        "        4: April            10: October\n"+
        "        5: May              11: November\n"+
        "        6: June             12:December\n"+
        "               0: All months \n")

    while True:
        try:
            choice_m = int(input(" Please select the number that corrospond to the month you wish to filter by: \n>"))

            if int(choice_m) not in range(0,13):
                print(" that is not a valid option")
            elif int(choice_m) in range(0, 13):
                month = months[(choice_m)]
                mm = choice_m
                break
        except ValueError:
            print(" your choice should be in numbers")
            continue

    if mm == 0:
        print('you have selected all months')
    else:
        print ('you have selected the month of {}'.format(month))



    print (" PLEASE SELECT ONE OF THE FOLLOWING OPTIONS: \n"+
        "        1: Monday            5: Friday\n"+
        "        2: Tuesday           6: Saturday\n"+
        "        3: Wednesday         7: Sunday\n"+
        "        4: Thursday          0: All days")


    while True:
        try:
            choice_d = int(input(" Please select the number that corrospond to the day of the week you wish to filter by: \n>"))

            if int(choice_d) not in range(0,8):
                print(" that is not a valid option")
            elif int(choice_d) in range(0, 8):
                day = days[(choice_d)]
                dd = choice_d
                break
        except ValueError:
            print(" your choice should be in numbers")
            continue

    if dd == 0:
        print('you have selected all days of the week')
    else:
        print ("you have selected to filter by {}'s".format(day))


    choices = "* You have chosen to explore the data of:{} for days: {} in the month of:{} *".format(city,day,month)
    print('*'*len(choices)+'\n'+choices+'\n'+'*'*len(choices))
    return city, month, day, mm




def load_data(city, month, day,mm):

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'All':

        df = df[df['month'] == mm]


    if day != 'All':
       df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if month == 'All':
        popular_month = df['month'].mode()[0]
        mo_count = (df.month == popular_month).sum()
        print("the most popular month is:   {}          total counts: {}".format((months[int(popular_month)]),(mo_count)))

    if day == 'All':
        popular_day = df['day_of_week'].mode()[0]
        da_count = (df.day_of_week == popular_day).sum()
        print("the most popular weekday is: {}          total counts: {}".format(popular_day, (da_count)))

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    ha_count = (df.hour == popular_hour).sum()
    print("Most Frequent Start Hour is:     {}          total counts: {}".format(popular_hour, (ha_count)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    st_station = df['Start Station'].mode()[0]
    sst_count = (df['Start Station'] == st_station).sum()


    # display most commonly used end station
    en_station = df['End Station'].mode()[0]
    est_count = (df['End Station'] == en_station).sum()


    # display most frequent combination of start station and end station trip
    df['rout'] = df['Start Station'].str.cat(df['End Station'], sep=" to: ")
    popular_rout = df['rout'].mode()[0]
    rout_count = (df['rout'] == popular_rout).sum()

    print("Most commonly used start station is: {}     with total of: {}".format(st_station, (sst_count)))
    print("Most commonly used End station is: {}     with total of: {}".format(en_station, (est_count)))
    print(" Most popular travel route was from: {}     with total of: {}".format(popular_rout, (rout_count)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    t_dur = df['Trip Duration'].sum()
    m_dur = df['Trip Duration'].mean()

    def time_con(tt):
        ttd = int(tt/86400)
        tth = int((tt%86400)/3600)
        ttm = int(((tt%86400)%3600)/60)
        tts = int(((tt%86400)%3600)%60)
        return ('{}: days    {}: hours    {}: minutes  {}: seconds'.format(ttd, tth, ttm, tts))

    print("Total travel time for the selected period was {}\n with an average trip duration of {}".format(time_con(t_dur), time_con(m_dur)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day, mm = get_filters()
        df = load_data(city, month, day,mm)



        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        #user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
