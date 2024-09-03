import pandas as pd
import matplotlib.pyplot as plt #import plotting library

# load data
my_df = pd.read_csv('milk_temp.csv')

fig = plt.figure()
# ax1 = plt.axes(projection="3d")
ax1 = plt.axes()
ax1.set_xlabel('time (s)')
ax1.set_ylabel('temp (C)')
ax1.set_xlim(0, 180)
ax1.set_ylim(0, 90)
plt.plot(my_df.t, my_df.T_c)

# plot hot temp
plt.plot([0, 180] , [my_df.T_h[0], my_df.T_h[0]])

# plot room temp
plt.plot([0, 180] , [20, 20])

# plot body temp
plt.plot([0, 180] , [37, 37])

plt.show()