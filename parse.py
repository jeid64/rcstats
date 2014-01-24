#!/usr/bin/python
import csv
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import datetime
import argparse

def main():
    parser = argparse.ArgumentParser(description='Make graphs from a CSV file to figure out who used the most cpu-minutes on RC machines.')
    parser.add_argument('inputcsv', help="The CSV you want to put in.")
    #parser.add_argument('')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--topSum', help='Print the top N users, as well as the sum of everyone in the CVS per day.', type=int)
    group.add_argument('--userReport', help='Make a png of every users graph.', action="store_true")
    group.add_argument('--allUsers', help="Make a graph of allUsers on one graph.", action="store_true")
    group.add_argument('--demo', help="Make a simple graph with the second and third users in the CSV.", action="store_true")
    args = vars(parser.parse_args())
    print (args)
    with open(args["inputcsv"], 'rb') as csvfile:
        reader = csv.reader(csvfile)
        dates = []
        users = []
        for row in reader:
            if len(dates) is 0:
                # Add dates for period.
                dates = row[1:]
            else:
                # Check if it is a uid number instead of a cn.
                if not row[0].isdigit():
                    users.append(row)
        print ("Dates are ", dates)
        print ("User values are ", users)
        dateobjects = [datetime.datetime.strptime(d,'%Y%m%d').date() for d in dates]
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        if (args["topSum"]):
            topSumUsers(dateobjects, users, args["topSum"])
        elif (args["userReport"]):
            userReport(dateobjects, users)
        elif (args["allUsers"]):
            allUsers(dateobjects, users)
        else:
            demo(dateobjects, users)

def userReport(dateobjects, users):
    # Makes a png per user with their graph.
    for user in users:
        plt.figure()
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        plt.gca().yaxis.set_major_locator(MultipleLocator(1440))
        plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%i minutes.'))
        plt.gca().yaxis.grid(True)
        plt.plot(dateobjects, user[1:], label=user[0])
        plt.legend()
        plt.gcf().autofmt_xdate()
        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(18.5,10.5)
        plt.savefig(user[0] + ".png", dpi=100)
        matplotlib.pyplot.close("all")

def topSumUsers(dateobjects, users, numUsers):
    # Shows the top four sum users, comparing it to everyone else as well.
    # Inserts the sum at the head of the list. Inefficient with built in list.
    for user in users:
        floatMinutes = list(map(float, user[1:]))
        sumMinutes = sum(floatMinutes)
        user.insert(0, sumMinutes)
    users.sort(key=lambda x:x[0], reverse=True)
    for i in xrange(0, numUsers):
        plt.plot(dateobjects, users[i][2:], label=users[i][1])
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.gca().yaxis.set_major_locator(MultipleLocator(1440))
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%i minutes.'))
    plt.gca().yaxis.grid(True)
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(18.5,10.5)
    plt.savefig("topSumUsers.png",dpi=100)

def allUsers(dateobjects, users):
    for user in users:
        plt.plot(dateobjects, user[1:], label=user[0])
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.gca().yaxis.set_major_locator(MultipleLocator(1440))
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%i minutes.'))
    plt.gca().yaxis.grid(True)
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(18.5,10.5)
    plt.savefig("allUsers.png",dpi=100)

def demo(dateobjects, users):
    plt.gca().yaxis.set_major_locator(MultipleLocator(1440))
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%i minutes.'))
    plt.gca().yaxis.grid(True)
    plt.plot(dateobjects, users[3][1:], label=users[3][0])
    plt.plot(dateobjects, users[4][1:], label=users[4][0])
    plt.legend()
    plt.gcf().autofmt_xdate()
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(18.5,10.5)
    plt.savefig("demo.png",dpi=100)

if __name__ == "__main__":
    main()
