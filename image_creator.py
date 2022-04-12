import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import os
import tweepy
from functions import del_whitespace


async def api_request():

  api_key = os.environ['api_key']
  api_key_secret = os.environ['api_key_secret']
  access_token_secret = os.environ['access_token_secret']
  access_token = os.environ['access_token']


  auth = tweepy.OAuthHandler(api_key, api_key_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth)

  time = []
  tweets = []
  for i in tweepy.Cursor(api.user_timeline, screen_name="@MZ_GOV_PL", tweet_mode="extended").items(30):
      tweets.append(i.full_text)
      day = str(i.created_at)
      time.append(day[:10])
  

  df = pd.DataFrame({'tweets': tweets, 'time': time})
  df = df[df.tweets.str.contains("Mamy")]
  df = df[~df.tweets.str.contains("Sprostowanie")]
  df = df[~df.tweets.str.contains("@a_niedzielski")]
  df = df[~df.tweets.str.contains("szczep")]
  df = df[~df.tweets.str.contains("dialog")]
  df = df[~df.tweets.str.contains("dziewczynka")]
  df = df[~df.tweets.str.contains("mutacji")]
  df = df[~df.tweets.str.contains("Wiceminister")]

  df = df.reset_index(drop=True)
  
  
  df2 = pd.DataFrame({'tweets': tweets, 'time': time})

  df2 = df2[df2.tweets.str.contains("W ciągu doby wykonano ponad")]
  df2 = df2[~df2.tweets.str.contains("Sprostowanie")]
  df2 = df2[~df2.tweets.str.contains("Minister")]
  df2 = df2[~df2.tweets.str.contains("Korekta")]

  df2 = df2.reset_index(drop=True)


  cases = []
  for i in df.tweets:
      if i.find("nowych") != -1:
          x = i.index("nowych")
      elif i.find("nowy") != -1:
          x = i.index("nowy")
      elif i.find("nowe") != -1:
          x = i.index("nowe")
      elif i.find("(w tym") != -1:
          x = i.index("(w tym")
      case_ = 0
      if i[x-3].isnumeric():
          case_ = i[x - 3:x - 1]
          if i[x-4].isnumeric():
              case_ = i[x - 4:x - 1]
              if i[x - 5].isnumeric() or i[x-5] == " ":
                  case_ = i[x - 5:x - 1]
                  if i[x - 6].isnumeric():
                      case_ = i[x-6:x-1]
                      if i[x - 7].isnumeric():
                          case_ = i[x - 7:x - 1]
                          if i[x - 8].isnumeric():
                              case_ = i[x - 8:x - 1]
      case_ = del_whitespace(case_)
      cases.append(case_)

  dates = []
  for i in df.time:
    dates.append(i)

  tests = []
  for i in df2.tweets:
      x = i.index("tys. testów")
      if i[x-3].isnumeric() or i[x-3] == ",":
          test_ = i[x - 3:x - 1]
          if i[x-4].isnumeric():
              test_ = i[x - 4:x - 1]
              if i[x - 5].isnumeric():
                  test_ = i[x - 5:x - 1]
                  if i[x - 6].isnumeric():
                      test_ = i[x-6:x-1]

      test_ = float(test_.replace(",", ".")) * 1000
      test_ = int(test_)
      tests.append(test_)

  tests__ = tests[0]
  dates__ = dates[0]
  cases__ = cases[0]

  tests_old = []
  cases_old = []
  dates_old = []

  df5 = pd.read_csv("covid.csv")
  for i in df5.tests:
    tests_old.append(i)
  for i in df5.cases:
    cases_old.append(i)
  for i in df5.date:
    dates_old.append(i)


  tests_old.append(tests__)
  dates_old.append(dates__)
  cases_old.append(cases__)

  df3 = pd.DataFrame({'cases': cases_old, 'tests': tests_old, 'date': dates_old})
  df3.to_csv('covid.csv')


def draw_stats():

  # with open("covid.txt", "r") as f:
  #     for line in f.readlines():
  #         line = line.rstrip("\n").split()
  #         date, case, test = line
  #         dates.append(date)
  #         cases.append(int(case))
  #         tests.append(int(test))
  #         percent.append(float(max(tests)) * (float(case) / float(test)))
  

  df = pd.read_csv("covid.csv")
  dates = []
  tests = []
  cases = []
  percent = []
  week_average = []

  for i in df.date.index:
    date, test, case = df.date[i], df.tests[i], df.cases[i]
    dates.append(date)
    tests.append(test)
    cases.append(case)
    percent.append(float(max(tests)) * (float(case) / float(test)))


  def first_week_average(cases_, i_=0, sum_=0, divider=0):
      if i_ == 7:
          return week_average
      else:
          sum_ += cases_[i_]
          divider += 1
          week_average.append(sum_ / divider)
          i_ += 1
          first_week_average(cases_, i_, sum_, divider)


  first_week_average(cases)


  def create_week_average(cases_, week_average_):
      i = 7
      for x in range(i, len(cases_)):
          sum_ = (cases_[x] + cases_[x - 1] + cases_[x - 2] + cases_[x - 3] + cases_[x - 4] + cases_[x - 5] + cases_[
              x - 6]) / 7
          week_average_.append(sum_)
      return week_average_


  def latest_date():
    return dates[-1]
    latest_date
    
    
  create_week_average(cases, week_average)

  sns.set_theme()  # theme change

  fig, (ax1, ax2) = plt.subplots(2, 1)
  ax1.fill_between(dates, week_average, label='średnia tygodniowa')
  ax1.set_title('Średnia ruchoma tygodniowa zachorowań')
  ax1.legend(loc='upper left')

  ax2.plot(dates, percent, label='Procent testów pozytywnych')
  ax2.set_title('Stosunek testów pozytywnych do wszystkich testów')

  r = np.arange(len(dates))
  ax2.bar(dates, cases, color='r', edgecolor='r', width=0.35, label='Przypadki')
  ax2.bar(r + 0.35, tests, color='g', edgecolor='g', width=0.35, label='Testy')


  ax2.legend()

  ax1.xaxis.set_major_locator(plt.MaxNLocator(15))
  ax2.xaxis.set_major_locator(plt.MaxNLocator(15))

  fig.set_size_inches(18.5, 10.5)
  plt.savefig('stats.png', dpi=200)
  # bbox_inches='tight',
  # plt.show()
  return dates[-1]
