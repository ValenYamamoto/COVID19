import csv
import math
from linear_regression import Regression
import matplotlib.pyplot as plt
from process_data import state_pop, state_den, StateDay
from datetime import date
from process_data import us_daily, italy_daily, italy_by_region
from state_populations import abbr

OPERATIONS = {"positive" : StateDay.get_positive,
              "negative": StateDay.get_negative,
              "total": StateDay.get_total,
              "pending": StateDay.get_pending,
              "death": StateDay.get_death}

class LogError(Exception):

    def __init__(self, val: float):
        self.val = val

def make_date(d: str) -> date:
    return date(int(d[:4]), int(d[4:6]), int(d[6:8]))

def days_elapsed(d1: date, d2: date) -> int:
    return (d1 - d2).days

def log(n):
    try:
        if n == 0:
            return math.log(0.000001)
        return math.log(n)
    except ValueError:
        raise LogError(n)

def get_state_data(data: dict, state: str) -> dict:
    state_data = {}
    for day, values in data.items():
        if state in values:
            state_data[values[state].day] = values[state]
    return state_data

def get_province_data_by_region(data: dict, province: str, region: str) -> dict:
    pass

def plot_slope_pop_USA(start_date: str) -> None:
    start_date = date.fromisoformat(start_date)
    slopes = []
    pop = []
    
    for state in state_den:
        if state != "United States" and "Region" not in state:
            print(state)
            state_data = get_state_data(us_daily, state)

            plot_data = {days_elapsed(x, start_date): log(y.positive) for x, y in state_data.items() if x >= start_date and y.positive != -1}
            x_axis_log, y_axis_log = list(plot_data.keys()), list(plot_data.values())
            reg = Regression(x_axis_log, y_axis_log)

            slopes.append(reg.slope)
            pop.append(state_pop[state])
            plt.scatter(state_pop[state], reg.slope, label=state)
            
##    plt.scatter(densities, slopes, label="slope v density")
    slope_density_reg = Regression(pop, slopes)
    y_reg = [reg.calc(x) for x in pop]
    x_axis = [x for x in pop]
    
def plot_slope_density_USA(start_date: str) -> None:
    start_date = date.fromisoformat(start_date)
    slopes = []
    densities = []
    
    for state in state_den:
        if state != "DC":
            state_data = get_state_data(us_daily, state)

            plot_data = {days_elapsed(x, start_date): log(y.positive) for x, y in state_data.items() if x >= start_date and y.positive != -1}
            x_axis_log, y_axis_log = list(plot_data.keys()), list(plot_data.values())
            reg = Regression(x_axis_log, y_axis_log)

            slopes.append(reg.slope)
            densities.append(state_den[state])
            plt.scatter(state_den[state], reg.slope, label=state)
            
##    plt.scatter(densities, slopes, label="slope v density")
    slope_density_reg = Regression(densities, slopes)
    y_reg = [reg.calc(x) for x in densities]
    x_axis = [x for x in densities]
##    plt.plot(x_axis, y_reg, label="slope v density regression")

def plot_slope_density_states(start_date: str, *states: [str]) -> None:
    start_date = date.fromisoformat(start_date)
    slopes = []
    densities = []
    
    for state in states:
        if state != "DC":
            state_data = get_state_data(us_daily, state)

            plot_data = {days_elapsed(x, start_date): log(y.positive) for x, y in state_data.items() if x >= start_date and y.positive != -1}
            x_axis_log, y_axis_log = list(plot_data.keys()), list(plot_data.values())
            reg = Regression(x_axis_log, y_axis_log)

            slopes.append(reg.slope)
            densities.append(state_den[state])
        
            plt.scatter(state_den[state], reg.slope, label=state)
    slope_density_reg = Regression(densities, slopes)
    y_reg = [reg.calc(x) for x in densities]
    x_axis = [x for x in densities]
    
def calc_exp_regression(attr: str, state: str, start_date: str) -> Regression:
    state_data = get_state_data(us_daily, state)
    start_date = date.fromisoformat(start_date)
    
    x_axis_log, y_axis_log = get_log_plot_data(start_date, state_data, OPERATIONS[attr])
    reg = Regression(x_axis_log, y_axis_log)

    print("Slope:", reg.slope, "Intercept:", reg.intercept)
    print("R:", reg.r, "R-sq:", reg.r_sq)
    
    y_reg = [reg.calc(x) for x in x_axis_log]
    x_axis = [x for x in x_axis_log]
    y_axis = [math.exp(y) for y in y_reg]
    plt.plot(x_axis, y_axis, label=state+" "+attr+" regression")
    return reg

def plot_states(attr: str, start_date: str, *states: str) -> None:
    start_date = date.fromisoformat(start_date)
    for state in states:
        state_data = get_state_data(us_daily, state)
        plt.scatter(*get_plot_data(start_date, state_data, OPERATIONS[attr]), label=state)

def get_plot_data(start_date: date, state_data: dict, op: "func") -> ([], []):
    plot_data = {days_elapsed(x, start_date): op(y) for x, y in state_data.items() if x >= start_date and op(y) != -1}
    return list(plot_data.keys()), list(plot_data.values())

def get_log_plot_data(start_date: date, state_data: dict, op: "func") -> ([], []):
    plot_data = {days_elapsed(x, start_date): log(op(y)) for x, y in state_data.items() if x >= start_date and op(y) != -1}
    return list(plot_data.keys()), list(plot_data.values())

def plot_states_new_vs_total_cases(start_date: str, *states: str) -> None:
    """ New Confirmed Case v Total Confirmed Case, both log."""
    start_date = date.fromisoformat(start_date)
    for state in states:
        try:
            state_data = get_state_data(us_daily, state)
            x, y = get_new_vs_total_cases_log_data(start_date, state_data)
            plt.plot(x, y, label=state)
            plt.scatter(x, y)
        except LogError as e:
            print(state, e.val)
    plt.xlabel("Total Positive Cases (ln)")
    plt.ylabel("New Positive Cases (ln)")
     
def get_new_vs_total_cases_log_data(start_date: date, state_data: dict) -> ([],[]):
    plot_data = {log(y.positive): log(y.change) for x, y in state_data.items() if x >= start_date and y.change > 0 and y.positive != -1}
    return list(plot_data.keys()), list(plot_data.values())
    
def plot_italy_positives_province(pro: str, start_date: str):
    start_date = date.fromisoformat(start_date)

def plot_all_states(attr: str, start_date: str) -> None:
    start_date = date.fromisoformat(start_date)
    for state in abbr.values():
        state_data = get_state_data(us_daily, state)
        plt.scatter(*get_plot_data(start_date, state_data, OPERATIONS[attr]), label=state)

def plot_all_states_new_vs_total(start_date: str) -> None:
    plot_states_new_vs_total_cases(start_date, *tuple(abbr.values()))
    
def show_plot():
    plt.legend()
    plt.show()
    


