from calendar import Calendar


x = Calendar()
for day in Calendar().itermonthdates(2025, 1):
    print(day.strftime("%A"))
