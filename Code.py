# -*- coding: utf-8 -*-
"""Robot_Localization.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1av5JcJL5DZS_OxOpHTxhJv7UvEVemkw_
"""

import numpy as np
import random
import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle
import matplotlib.gridspec as gridspec
import math
import matplotlib.patches as mpatch

"""

## Global Variables and Utility Functions"""

sensor_pos = [(15,8),(8,15),(15,15),(15,22)]
sensor_grid1 = np.zeros((9,9), np.float128)
c = 0.9
# Making the sensor grid
for i in range(5):
    for j in range(-1*i,i+1):
        sensor_grid1[4-i][4+j] = c-(0.1*i)
        sensor_grid1[4+i][4+j] = c-(0.1*i)
        sensor_grid1[4+j][4-i] = c-(0.1*i)
        sensor_grid1[4+j][4+i] = c-(0.1*i)

T = 25
l,b = 30,30
p_actions = [0.4,0.1,0.2,0.3] # up, down, left, right respectively
final_bel_filt = np.zeros((30, 30), np.float128)



def manhattan(a, b, x, y):
  err = np.zeros((len(a)))
  for i in range(len(a)):
    err[i] = np.abs(a[i]-x) + np.abs(b[i] - y)
  return np.sum(err)/len(a)

"""## Simulation"""

def sample_sensor_data(sensor_grid, position):
    sensor_out = []
    x,y = position
    for i in range(4):
        r = random.uniform(0,1)
        if r<= sensor_grid[i][x][y]:   # due to origin shifting
            sensor_out.append(1)   # shows present
        else:
            sensor_out.append(0)   # shows absent
    return sensor_out

def simulate(sensor_grid,p_actions,T, initial_pos, l, b):
    positions = [initial_pos]
    actions =[]
    sensors_data = []
    sensors_data.append(sample_sensor_data(sensor_grid,initial_pos))


    for i in range(T):
        # sample an action and apply it
        r = random.uniform(0,1)      
        action = None
        next_pos = None
        if r<=p_actions[0]:
            action = 'up'
            next_pos = (min(b-1,positions[-1][0]+1) ,positions[-1][1] )

        elif r<= (p_actions[0]+p_actions[1]):
            action = 'down'
            next_pos = (max(0,positions[-1][0]-1), positions[-1][1] )

        elif r<= (p_actions[0]+ p_actions[1]+ p_actions[2]):
            action = 'left'
            next_pos = (positions[-1][0],max(0,positions[-1][1]-1))

        elif r<= 1:
            action = 'right'
            next_pos = (positions[-1][0],min(l-1,positions[-1][1]+1))

        actions.append(action)
        positions.append(next_pos)        
        
        # sample sensor data according to next pos
        # remember sensors are independent so sample again and again
        sensors_data.append(sample_sensor_data(sensor_grid,next_pos))

    return actions, sensors_data, positions


def getProbability(pos, sensor_grid, z):
    x,y = pos
    p=1
    for i in range(4):
        temp = sensor_grid[i][x][y]
        if z[i] ==0:
            temp = 1-temp
        p=p*temp
    return p
            

def generateSensorGrid(sensor_pos):
    grid = np.zeros((30,30), np.float64)
    x,y = sensor_pos
    c=0.9
    for i in range(5):
        for j in range(-1*i,i+1):
            grid[x-i][y+j] = c-(0.1*i)
            grid[x+i][y+j] = c-(0.1*i)
            grid[x+j][y-i] = c-(0.1*i)
            grid[x+j][y+i] = c-(0.1*i)
    return grid
    




#sensor_pos = [(15,8),(8,15),(15,15),(15,22)] # mapped positions to a matrix by moving the origin in the grid to the origin of a numpy matrix

"""### Running the simulation"""

sensor_grid = [generateSensorGrid((15,8)),generateSensorGrid((8,15)),generateSensorGrid((15,15)),generateSensorGrid((15,22))]

initial_pos = (10, 10)
actions, sensors_data, positons = simulate(sensor_grid,p_actions,T, initial_pos,l,b)
#print(actions)
print(sensors_data)
#print(positons)
#print()

# def plot(belief_grid, i):
#     fig = plt.figure()

#     plt.imshow(belief_grid,cmap='gray')
#     plt.title('Log likelihoods at time {i}')
#     plt.show()

def plot_with_max_and_gnd(belief_mat, a, b, x, y):
  fig= plt.figure(figsize = (60,200))
  gs1 = gridspec.GridSpec(math.ceil(T/3), 3)
  gs1.update(wspace=0.025, hspace=0.04)
  
  for j in range(belief_mat.shape[0]):
    ax = fig.add_subplot(gs1[j])
    plt.imshow(belief_mat[j], cmap = 'bone')
    for i in range(len(a[j])):
      ax.add_patch(Rectangle((b[j][i]-0.5, a[j][i]-0.5),1, 1, fill=False, edgecolor='red', lw=1.5))
    ax.add_patch(Rectangle((x[j][1]-0.5, x[j][0]-0.5),1, 1, fill=False, edgecolor='blue', lw=1.5))
    #plt.axis('off') 
    plt.title("t = {}".format(j+y), fontsize = 80)
  #fig.colorbar(im, ax=axes.ravel().tolist()).set_label(label="Log Likelihood heat map over the states", size=40, weight='bold') 
    plt.colorbar(orientation="horizontal").set_label(label="Log Likelihood", size=50, weight='bold') 
    
  plt.show()





def plot_with_max(belief_mat, a, b, y):
  fig= plt.figure(figsize = (60,200))
  gs1 = gridspec.GridSpec(math.ceil(T/3), 3)
  gs1.update(wspace=0.025, hspace=0.04)
  
  for j in range(belief_mat.shape[0]):
    ax = fig.add_subplot(gs1[j])
    plt.imshow(belief_mat[j], cmap = 'bone')
    for i in range(len(a[j])):
      ax.add_patch(Rectangle((b[j][i]-0.5, a[j][i]-0.5),1, 1, fill=False, edgecolor='red', lw=1.5))
    plt.title("t = {}".format(j+y), fontsize = 80)
    plt.colorbar(orientation="horizontal").set_label(label="Log Likelihood", size=50, weight='bold') 
    
  plt.show()

def plot_path(a, x, y):
  fig= plt.figure(figsize = (60,200))
  gs1 = gridspec.GridSpec(math.ceil(T/3), 3)
  gs1.update(wspace=0.025, hspace=0.1)
  #C = np.zeros((30, 30))
  for j in range(len(a)):
    ax = fig.add_subplot(gs1[j])
    #plt.imshow(C, color = 'white')
    ax.add_patch(Rectangle((a[j][1], a[j][0]),1, 1, color='red', lw=1, label = "Estimated"))
    ax.add_patch(Rectangle((x[j][1], x[j][0]),1, 1, color='blue', lw=1, label = "Ground Truth"))
    plt.xlim([0, 30]) 
    plt.ylim([0, 30])   
    plt.title("t = {}".format(j+y), fontsize = 80)
    handles, labels = ax.get_legend_handles_labels()
    plt.legend(handles, labels, loc='upper center')
    major_ticks = np.arange(0, 31, 5)
    minor_ticks = np.arange(0, 31, 1)

    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_yticks(major_ticks)
    ax.set_yticks(minor_ticks, minor=True)

    
    ax.grid(True, which='both')
    plt.minorticks_on
  
  plt.show()

likelihood = np.zeros((4, 30, 30), np.float128)

# 3D matrix, containing the likelihood distributions of the sensor observations projected onto the 30x30 grid. 
for i in range(4):
  a = sensor_pos[i][0]-4
  b = sensor_pos[i][0]+5
  c = sensor_pos[i][1]-4
  d = sensor_pos[i][1]+5
  likelihood[i][a:b, c:d] = sensor_grid1
  #print(likelihood[i][a:b, c:d])

# for forward likelihood prediction
# t < 25
# P: Prev likelihood matrix

def filtering(P, z):
  Q = np.zeros((30, 30), np.float128)
  Q[0:29] += 0.4*P[1:30]
  Q[1:30] += 0.1*P[0:29]
  Q[:, 0:29] += 0.2*P[:, 1:30]
  Q[:, 1:30] += 0.3*P[:, 0:29]

  # for i in range(30):
  #   for j in range(30):
  #     if (i > 0): 
  #       Q[i][j] = 0.1*P[i-1][j]
  #     if (i < 29):
  #       Q[i][j] = 0.4*P[i+1][j]
  #     if (j > 0):
  #       Q[i][j] = 0.3*P[i][j-1]
  #     if (j < 29):
  #       Q[i][j] = 0.2*P[i][j+1]
  zgivenx = np.ones((30, 30), np.float128)
  for i in range(4):
    if (z[i]):
      zgivenx = np.multiply(zgivenx, sensor_grid[i])
    else:
      zgivenx = np.multiply(zgivenx, 1-sensor_grid[i])
  Q = np.multiply(zgivenx, P)
  x = np.sum(Q)
  Q = Q/x
  return Q

# l, b = 30, 30
# p_actions = [0.4,0.1,0.2,0.3] # up, down, left, right respectively
    
# initial_pos = (15,15)
# sensor_grid1 = [generateSensorGrid((15,8)),generateSensorGrid((8,15)),generateSensorGrid((15,15)),generateSensorGrid((15,22))]
# actions, sensors_data, positions = simulate(sensor_grid1, p_actions,25, initial_pos,l, b)

P = np.ones((30, 30), np.float64 )
P = (1/900)*P
#plot_with_max_and_gnd(np.log(P), [], [], positons[0])
#plot(P)
error_fil = np.zeros((T))
error_fil1 = np.zeros((T))
belief_mat = np.zeros((T, 30, 30))
A = [[] for i in range(T)]
B = [[] for i in range(T)]
for i in range(T):
  P = filtering(P, sensors_data[i+1])
  #plot(P)
  #print(P)
  #plot(np.log(P))
  
  print(i)
  # print(sensors_data[i])
  # print(np.where(P == np.amax(P)))
  a, b = np.where(P == np.amax(P))
  A[i] = a
  B[i] = b
  belief_mat[i] = P
  error_fil[i] = manhattan(a, b, positons[i+1][0], positons[i+1][1])
  error_fil1[i:] += manhattan(a, b, positons[i+1][0], positons[i+1][1])
  #print(unravel_index(P.argmax(), P.shape))
plot_with_max_and_gnd(np.log(belief_mat[:math.floor(T/2)]), A[:math.floor(T/2)], B[:math.floor(T/2)], positons[1:math.floor(T/2)+1], 0)
plot_with_max_and_gnd(np.log(belief_mat[math.floor(T/2):]), A[math.floor(T/2):], B[math.floor(T/2):], positons[math.floor(T/2)+1:], math.floor(T/2))
final_bel_filt = P

"""## Smoothing"""


def backward(b, e):
  zgivenx = np.ones((30, 30), np.float64)
  for i in range(4):
    if (e[0][i]):
      zgivenx = np.multiply(zgivenx, likelihood[i])
    else:
      zgivenx = np.multiply(zgivenx, 1-likelihood[i])
  R = np.multiply(zgivenx, b)
  Q = np.zeros((30, 30), np.float64)
  Q[0:29] += 0.1*R[1:30]
  Q[1:30] += 0.4*R[0:29]
  Q[:, 0:29] += 0.3*R[:, 1:30]
  Q[:, 1:30] += 0.2*R[:, 0:29]
  return Q

# P is the prior of the forward pass
def forward_backward(sensors_data, P, T):
  Q = np.zeros((T+1, 30, 30), np.float64)
  Q[0] = P
  #A = np.zeros((30, 30))
  for i in range(1,T+1):
    Q[i] = filtering(Q[i-1], sensors_data[i-1])
  b = np.ones((30, 30), np.float64)
  sv = np.zeros((T, 30, 30), np.float64)
  for i in range(T, 0, -1):
    sv[i-1] = np.multiply(Q[i], b)
    x = np.sum(sv[i-1])
    sv[i-1] /= x
    b = backward(b, sensors_data[i-1: T])
  return sv

# l, b = 30, 30
# p_actions = [0.4,0.1,0.2,0.3] # up, down, left, right respectively
    
# initial_pos = (15,15)
# sensor_grid1 = [generateSensorGrid((15,8)),generateSensorGrid((8,15)),generateSensorGrid((15,15)),generateSensorGrid((15,22))]
# actions, sensors_data, positions = simulate(sensor_grid1, p_actions,25, initial_pos,l, b)

P = np.ones((30, 30), np.float64)
P = (1/900)*P
#plot(np.log(P))
#plot_with_max_and_gnd(np.log(P), [], [], positons[0])
sv = forward_backward(sensors_data, P, 25)
#error_smo = np.zeros((T))
error_smo = np.zeros((T))
error_smo1 = np.zeros((T))
positions = np.array([[10, 10], [11, 10], [12, 10], [12, 11], [13, 11], [13, 10], [14, 10], [13, 10], [13, 11], [12, 11], [11, 11], [12, 11], [13, 11], [14, 11], [14, 12], [14, 11], [15, 11], [15, 12], [15, 13], [14, 13], [15, 13], [16, 13], [17, 13], [17, 12], [17, 13], [17, 14]])
belief_mat = np.zeros((T, 30, 30))
A = [[] for i in range(T)]
B = [[] for i in range(T)]
for i in range(T):
  #plot(np.log(sv[i]))
  a, b = np.where(sv[i] == np.amax(sv[i]))
  A[i] = a
  B[i] = b
  belief_mat[i] = sv[i]
  print(np.where(sv[i] == np.amax(sv[i])))
  error_smo[i] = manhattan(a, b, positons[i+1][0], positons[i+1][1])
  error_smo1[i:] += error_smo[i]
  
  #print(unravel_index(sv[i].argmax(), sv[i].shape)) ## NOT SURE IF THIS IS A GOOD WAY
plot_with_max_and_gnd(np.log(belief_mat[:math.floor(T/2)]), A[:math.floor(T/2)], B[:math.floor(T/2)], positons[1:math.floor(T/2)+1], 0)
plot_with_max_and_gnd(np.log(belief_mat[math.floor(T/2):]), A[math.floor(T/2):], B[math.floor(T/2):], positons[math.floor(T/2)+1:], math.floor(T/2))

"""## Error between actual path and path found using filtering and Smoothing"""

def plot_error():
  
  ax = plt.subplot(111)
  y = np.array([i for i in range(T)])
  ax.bar(y-0.1, error_fil, width=0.2, color='b', align='center', label = "Filtering")
  ax.bar(y+0.1, error_smo, width=0.2, color='r', align='center', label = "Smoothing")
  #ax.bar(x+0.2, k, width=0.2, color='r', align='center')
  plt.xlabel("Time Steps")
  plt.ylabel("Error")
  plt.title("Manhattan Distance Error compared with Ground Truth")
  plt.legend()
  plt.grid()
  plt.show()

def plot_error_int():
  x = [i for i in range(T)]
  plt.plot(x, error_fil1, label = "Filtering Error")
  plt.plot(x, error_smo1, label = "Smoothing Error") 
  plt.xlabel('Time steps')
  plt.ylabel('Error')
  plt.title('Comparing the error in Filtering and Smoothing Paths using Manhattan Distance')
  plt.legend()
  plt.grid()
  plt.show()

plot_error()
plot_error_int()
print(error_fil)
print(error_smo)

"""## Predictive Likelihood"""

ts = 10

def prediction():
  P = final_bel_filt
  Q = np.zeros((30, 30), np.float64)
  belief_mat = np.zeros((ts, 30, 30))
  A = [[] for i in range(ts)]
  B = [[] for i in range(ts)]
  for i in range(ts):
    
    Q[0:29] += 0.4*P[1:30]
    Q[1:30] += 0.1*P[0:29]
    Q[:, 0:29] += 0.2*P[:, 1:30]
    Q[:, 1:30] += 0.3*P[:, 0:29]
    a, b = np.where(Q == np.amax(Q)) 
    #print(unravel_index(Q.argmax(), Q.shape))
    A[i] = a
    B[i] = b
    belief_mat[i] = Q
    print(np.where(Q == np.amax(Q)))
    P = Q
  # plot_with_max(np.log(belief_mat[:math.floor(ts/2)]), A[:math.floor(ts/2)], B[:math.floor(ts/2)], 0)
  # plot_with_max(np.log(belief_mat[math.floor(ts/2):]), A[math.floor(ts/2):], B[math.floor(ts/2):], math.floor(ts/2))
  plot_with_max(np.log(belief_mat), A, B, 0)

prediction()

"""## Most Likely Path """

def most_likely(P, seq, z):
  maxi = [[(0, 0) for i in range(30)] for j in range(30)]
  Q = np.zeros((30, 30), np.float64)
  R = np.zeros((30, 30), np.float64)
  R[0:29] = 0.4*P[1:30]
  for i in range(29):
    for j in range(30):
      if (R[i][j] > Q[i][j]):
        Q[i][j] = R[i][j]
        maxi[i][j] = (i+1, j)
        
  R[1:30] = 0.1*P[0:29]
  for i in range(1, 30):
    for j in range(30):
      if (R[i][j] > Q[i][j]):
        Q[i][j] = R[i][j]
        maxi[i][j] = (i-1, j)
        
  R[:, 0:29] = 0.2*P[:, 1:30]
  for i in range(30):
    for j in range(29):
      if (R[i][j] > Q[i][j]):
        Q[i][j] = R[i][j]
        maxi[i][j] = (i, j+1)

  R[:, 1:30] = 0.3*P[:, 0:29]
  for i in range(30):
    for j in range(1, 30):
      if (R[i][j] > Q[i][j]):
        Q[i][j] = R[i][j]
        maxi[i][j] = (i, j-1)
      #print(type(seq[maxi[i][j][0]][maxi[i][j][1]]))

  seq1 = [[[(i, j)] for i in range(30)] for j in range(30)]
      
  for i in range(30):
    for j in range(30):
      a, b = maxi[i][j]
      seq1[i][j] = seq[a][b].copy()
      seq1[i][j].append((i, j))
      
  

  zgivenx = np.ones((30, 30), np.float64)
  for i in range(4):
    if (z[i]):
      zgivenx = np.multiply(zgivenx, sensor_grid[i])
    else:
      zgivenx = np.multiply(zgivenx, 1-sensor_grid[i])
  Q = np.multiply(zgivenx, P)
  x = np.sum(Q)
  Q = Q/x
  return Q, seq1

P = np.ones((30, 30), np.float64)
P = (1/900)*P
#plot(np.log(P))
#plot(P)
seq = [[[] for i in range(30)] for j in range(30)]
for i in range(T):
  P, seq = most_likely(P, seq, sensors_data[i])
  #plot(P)
  # plot(np.log(P))
  # print(sensors_data[i])
#(a, b) = unravel_index(P.argmax(), P.shape)
a, b = np.where(P == np.amax(P))
for i in range(len(a)):
  print(seq[a[0]][b[0]])
  print()
plot_path(seq[a[0]][b[0]][:math.floor(T/2)], positons[1:math.floor(T/2)+1], 0)
plot_path(seq[a[0]][b[0]][math.floor(T/2):], positons[math.floor(T/2)+1:], math.floor(T/2))

print(len(seq[a[0]][b[0]]))
print(a, b)

print(positons)
print(sensors_data)
