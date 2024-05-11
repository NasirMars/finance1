import matplotlib.pyplot as plt

x_data = []
benefits_data = []
accumulate_money_data = []
invest_period = 18250
initial_money = 500
interest_rate = 0.17
saved_salary = 0
period = 365

turn = int(invest_period/period)
accumulate_money = initial_money
saved_money = initial_money

for x in range(turn):
    x_data.append(x+1)
    benefits = accumulate_money*interest_rate
    benefits_data.append(f"{benefits:.2f}")
    accumulate_money = accumulate_money + benefits + saved_salary
    accumulate_money_data.append(accumulate_money)
    saved_money = saved_money + saved_salary
    print(str(x+1)+":"+f"{accumulate_money:.2f}"+"  benefit:"+f"{benefits:.2f}"+"  saved money without investment:"+f"{saved_money:.2f}")
plt.plot(x_data, accumulate_money_data)
plt.xlabel("time")
plt.ylabel("accumulate money")
plt.title("COMPOUND INTEREST BENEFIT CHART")
plt.show()
