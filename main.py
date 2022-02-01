import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

dates = []
cases = []
tests = []
percent = []
with open("covid.txt", "r") as f:
    for line in f.readlines():
        line = line.rstrip("\n").split()
        date, case, test = line
        dates.append(date)
        cases.append(int(case))
        tests.append(int(test))
        percent.append(float(max(tests)) * (float(case) / float(test)))
week_average = []


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


create_week_average(cases, week_average)

sns.set_theme()  # theme change

fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.fill_between(dates, week_average, label='średnia tygodniowa')
ax1.set_title('Średnia ruchoma tygodniowa zachorowań')
ax1.legend(loc='upper left')

ax2.plot(dates, percent, label='Procent testów pozytywnych')
ax2.set_title('Stosunek testów pozytywnych do wszystkich testów')

r = np.arange(len(dates))
ax2.bar(dates, cases, color='r', width=0.25, edgecolor='black', label='Przypadki')
ax2.bar(r + 0.25, tests, color='g', width=0.25, edgecolor='black', label='Testy')

ax2.legend()

ax1.xaxis.set_major_locator(plt.MaxNLocator(15))
ax2.xaxis.set_major_locator(plt.MaxNLocator(15))

plt.show()
