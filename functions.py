import calendar
import json

def get_current_schedule(start_first_day = 27, start_first_month = 8, start_first_year = 2024):

    week_days = {
        1: "Понедельник",
        2: "Вторник",
        3: "Среда",
        4: "Четверг",
        5: "Пятница",
        6: "Суббота",
        7: "Воскресенье",
    }

    named_days = [
        "☀️ — День #1",
        "☀️ — День #2",
        "🌒 — Ночь #1",
        "🌒 — Ночь #2",
        "🕊️ — Выходной",
        "🕊️ — Выходной",
    ]

    # start_first_day = 27
    # start_first_month = 8
    # start_first_year = 2024

    result = []


    def get_current_backward_id(current_day):
        if current_day - 1 < 0:
            return len(named_days) - 1
        else:
            return current_day - 1

    def get_current_forward_id(current_day):
        if current_day + 1 == len(named_days):
            return 0
        else:
            return current_day + 1

    current_day = 0

    for month in range(start_first_month, 0, -1):
        for day in range(calendar.monthrange(start_first_year, month)[1], 0, -1):
            if not (month == start_first_month and day > start_first_day):
                if month == start_first_month and day == start_first_day:
                    result.append({"day": day, "month": month, "year": start_first_year, "activity": named_days[0]})
                else:
                    if week_days[calendar.weekday(start_first_year, month, day) + 1] == "Воскресенье":
                        result.append({"day": day, "month": month, "year": start_first_year, "activity": named_days[-1]})
                    else:
                        result.append({"day": day, "month": month, "year": start_first_year, "activity": named_days[current_day]})

                current_day = get_current_backward_id(current_day)

    current_day = 1

    for month in range(start_first_month, 13):
        for day in range(1, calendar.monthrange(start_first_year, month)[1] + 1):
            if not (month == start_first_month and day <= start_first_day):
                if not (month == start_first_month and day == start_first_day):
                    if week_days[calendar.weekday(start_first_year, month, day) + 1] == "Воскресенье":
                        result.append({"day": day, "month": month, "year": start_first_year, "activity": named_days[-1]})
                    else:
                        result.append({"day": day, "month": month, "year": start_first_year, "activity": named_days[current_day]})

                current_day = get_current_forward_id(current_day)

    for year in range(start_first_year+1, start_first_year+5):
        for month in range(1, 13):
            for day in range(1, calendar.monthrange(year, month)[1] + 1):
                if week_days[calendar.weekday(year, month, day) + 1] == "Воскресенье":
                    result.append({"day": day, "month": month, "year": year, "activity": named_days[-1]})
                else:
                    result.append({"day": day, "month": month, "year": year, "activity": named_days[current_day]})

                current_day = get_current_forward_id(current_day)

    result.sort(key=lambda x: x["month"])

    # with open("data.json", "w", encoding="utf-8") as f:
    #     json.dump(result, f, ensure_ascii=False, indent=4)
    #
    # print(result)

    return result

# if __name__ == "__main__":
#     get_current_schedule()