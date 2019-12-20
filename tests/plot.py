import os
import sys
import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

client = pymongo.MongoClient("mongodb://localhost")
diDatabase = client["diDatabase"]

# collections 
competitions = diDatabase["competitions"]
events = diDatabase["events"]
users = diDatabase["users"]
athletes = diDatabase["athletes"]
teams = diDatabase["teams"]
apps = diDatabase["apps"]

df = pd.DataFrame(list(users.find()))

df.plot(kind='bar',x='userID',y={'gamesAnnotated'},rot=0,legend=False,yticks=[0,1,2,3,4,5,6,7,8,9,10], ylim=[0,10.5])
plt.ylabel('Number of Games Annotated')
ax = df['averageRating'].plot(secondary_y=True, color='k', marker='o')
ax.set_ylabel('Average Rating')
ax.set_yticks([0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
ax.set_ylim(0.0, 1.05)
ax.set_xlim(np.array([-0.5, 0.5])+ax.get_xlim())

plt.show()
