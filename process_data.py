import csv
from datetime import date
from state_populations import state_pop, state_den

def make_date(d: str) -> date:
    return date(int(d[:4]), int(d[4:6]), int(d[6:8]))

def make_date_not_iso(d: str) -> date:
    d = d.split()[0].split("-")
    return date(int(d[2]), int(d[0]), int(d[1]))

class StateDay:

    def __init__(self, day, state, positive=0, negative=0, pending=0, death=0, total=0):
        self.state = state
        self.day = day
        self.positive = self._to_numeric(positive)
        self.negative = self._to_numeric(negative)
        self.pending = self._to_numeric(pending)
        self.death = self._to_numeric(death)
        self.total = self._to_numeric(total)
        self.change = -1
        if state in state_pop:
            self.population = state_pop[state]
        else:
            self.population = -1
        if state in state_den:
            self.density = state_den[state]
        else:
            self.den = -1

    def get_positive(self):
        return self.positive

    def get_negative(self):
        return self.negative

    def get_pending(self):
        return self.pending

    def get_death(self):
        return self.death

    def get_total(self):
        return self.total

    def update(self, state_day):
        self.positive = self._aggr_total_clean(state_day.positive)
        self.negative = self._aggr_total_clean(state_day.negative)
        self.pending = self._aggr_total_clean(state_day.pending)
        self.death = self._aggr_total_clean(state_day.death)
        self.total = self._aggr_total_clean(state_day.total)
        
    def _aggr_total_clean(self, val):
        if val == -1:
            return 0
        return val
    
    def _to_numeric(self, val):
        if val != '':
            return float(val)
        return -1

    def __str__(self):
        return f"{self.day} {self.state} {self.positive} {self.negative} {self.pending} {self.death} {self.total}"

us_daily = {}

with open('us_states_covid19_daily.csv') as file:
    reader = csv.reader(file)
    last_total = False
    for row in reader:
        if row[0].isdigit():
            day = make_date(row[0])
            state_day = StateDay(day, row[1], row[2], row[3], row[4], row[5], row[6])
            if last_total != False:
                state_day.change = state_day.positive - last_total
            if day in us_daily:
                us_daily[day][row[1]] = state_day
            else:
                us_daily[day] = {row[1]: state_day}
            last_total = state_day.get_positive()


last_positve = False
for day in us_daily:
    us_day = StateDay(day, "USA")
    for state_day in us_daily[day].values():
        us_day.update(state_day)
    if last_total != False:
        us_day.change = us_day.positive - last_positve
    last_total = us_day.get_positive()
    us_daily[day]["USA"] = us_day
        
italy_daily = {}
italy_by_region ={}
##with open("covid19_italy_province.csv") as file:
##    reader = csv.reader(file)
##    for row in reader:
##        if row[0].isdigit():
##            day = date.fromisoformat(row[1].split()[0])
##            data = StateDay(day, row[6], row[10])
##            
##            if day in italy_daily:
##                italy_daily[day][row[6]] = [data]
##            else:
##                italy_daily[day] = {row[6]: data}
##
##            region = row[4]
##            
##            if region in italy_by_region:
##                if day in italy_by_region:
##                    italy_by_region[region][row[6]] = [data]
##                else:
##                    italy_by_region[region] = {row[6]: data}
##            else:
##                italy_by_region[region] = {day: {row[6]: data}}
