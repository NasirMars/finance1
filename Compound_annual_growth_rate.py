import matplotlib.pyplot as plt

BegVal = 1000

Manager_A = [1.2, -0.6, 0.5]
Manager_B = [0.12, 0.08, 0.09]

NumYears_A = len(Manager_A)
NumYears_B = len(Manager_B)

def M_EndVal(Val, manager):
  for x in range(len(manager)):
    Val = Val * (1 + manager[x])
  return Val
def M_return(EndVal, BegVal, NumYears):
  return (EndVal / BegVal)**(1/NumYears) - 1

M_A_EndVal = M_EndVal(BegVal, Manager_A)
M_B_EndVal = M_EndVal(BegVal, Manager_B)

print("Manager A final return "+"{:.4f}".format(M_A_EndVal))
print("Manager B final return "+"{:.4f}".format(M_B_EndVal))
print("Manager A CAGR return: "+"{:.2%}".format(M_return(M_A_EndVal, BegVal, NumYears_A)))
print("Manager B CAGR return: "+"{:.2%}".format(M_return(M_B_EndVal, BegVal, NumYears_B)))

plt.figure(figsize=(10, 6))
plt.xticks(rotation=30)
plt.grid(True, which='both', linestyle=':', linewidth=1, color='black')
plt.plot(range(1, len(Manager_A) + 1), Manager_A, marker='o', color='red', label='Manager A')
plt.plot(range(1, len(Manager_B) + 1), Manager_B, marker='o', color='blue', label='Manager B')
plt.axhline(y=0, color='black', linestyle='-', linewidth=5)
plt.xlabel("YEAR")
plt.ylabel("CAGR return")
plt.title("CAGR CHART")
plt.show()
