import math

class Regression:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.slope = self.calc_slope()
        self.intercept = self.calc_intercept()
        self.r = self.calc_r()
        self.r_sq = self.r ** 2

    def std_sum_xx(self):
        avg = sum(self.x) / len(self.x)
        total = 0
        for i in self.x:
            total += (i - avg) ** 2
        return total

    def std_sum_yy(self):
        avg = sum(self.y) / len(self.y)
        total = 0
        for i in self.y:
            total += (i - avg) ** 2
        return total

    def std_sum_xy(self):
        avg_x = sum(self.x) / len(self.x)
        avg_y = sum(self.y) / len(self.y)
        total = 0
        
        for i in range(len(self.x)):
            total += ((self.x[i] - avg_x)) * ((self.y[i] - avg_y))
        return total
    
    def calc_slope(self):
        return self.std_sum_xy() / self.std_sum_xx()

    def calc_intercept(self):
        avg_x = sum(self.x) / len(self.x)
        avg_y = sum(self.y) / len(self.y)

        return avg_y - self.slope * avg_x

    def calc(self, x_hat: float) -> float:
        return self.slope * x_hat + self.intercept

    def calc_r(self):
        return self.std_sum_xy() / math.sqrt(self.std_sum_xx() * self.std_sum_yy())
