import matplotlib.pyplot as plt

covid = []
dates = []
cases = []
with open("covid.txt", "r") as f:
    for line in f.readlines():
        line = line.rstrip("\n").split()
        date, case, tests = line
        dates.append(date)
        cases.append(int(case))
        case = int(case)
        tests = int(tests)
        covid.append([date, case, tests])

plt.figure(figsize=(9, 9))
plt.subplot()

plt.bar(dates, cases)

# plt.subplot(132)
# plt.scatter(dates, cases)
# plt.subplot(133)
# plt.plot(dates, cases)
plt.suptitle('Covid cases in Poland')
plt.xticks(rotation=45)
plt.show()
