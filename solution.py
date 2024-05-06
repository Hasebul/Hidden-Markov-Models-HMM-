# -*- coding: utf-8 -*-
"""Ml_assignment_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vyTwKLWwh8nTTMZLVeZQHOlmdUVg9Tzr
"""

from google.colab import drive
drive.mount('/content/drive')

data_path  = '/content/drive/MyDrive/Assignment_Data/Assignment2/data.txt'
param_path = '/content/drive/MyDrive/Assignment_Data/Assignment2/parameters.txt'

with open(data_path) as f:
    lines = f.readlines()

em_arr = []
for line in lines:
    em_arr.append(float(line.strip('/n')))

print('em_arr :',em_arr)

with open(param_path ) as f:
    lines = f.readlines()
print(lines)
num_state = int(lines[0].strip('/n'))
init_prob = [ [0.7 , 0.3], [ 0.1 , 0.9] ]
mean1 = 200
mean2 = 100
sigma1 = 10 
sigma2 = 10

import math 
import numpy as np
from scipy.stats import norm

el_nino_emm = norm.pdf(em_arr,mean1,math.sqrt(sigma1))
la_nina_emm = norm.pdf(em_arr,mean2,math.sqrt(sigma2))

obs = []
for i in range (1000):
  obs.append(i)

states = ("El_Nino", "La_Nina")
start_p = {"El_Nino": 0.25, "La_Nina": 0.75 }
trans_p = {
    "El_Nino": {"El_Nino": 0.7, "La_Nina": 0.3},
    "La_Nina": {"El_Nino": 0.1, "La_Nina": 0.9},
}

emit_p = {}
emit_p['El_Nino']={}
emit_p['La_Nina']={}
for i in range(len(obs)):
  emit_p['El_Nino'][i] = el_nino_emm[i]
  emit_p['La_Nina'][i] = la_nina_emm[i]

def viterbi(obs, states, start_p, trans_p, emit_p , filename):
    V = [{}]
    for st in states:
        V[0][st] = {"prob": math.log(start_p[st] * emit_p[st][obs[0]]), "prev": None}
    # Run Viterbi when t > 0
    for t in range(1, len(obs)):
        V.append({})
        for st in states:
            max_tr_prob = V[t - 1][states[0]]["prob"] + math.log(trans_p[states[0]][st])
            prev_st_selected = states[0]
            for prev_st in states[1:]:
                tr_prob = V[t - 1][prev_st]["prob"] + math.log(trans_p[prev_st][st])
                if tr_prob > max_tr_prob:
                    max_tr_prob = tr_prob
                    prev_st_selected = prev_st

            max_prob = max_tr_prob + math.log(emit_p[st][obs[t]])
            V[t][st] = {"prob": max_prob, "prev": prev_st_selected}

    # for line in dptable(V):
    #     print(line)

    print(V)
    opt = []
    max_prob = float('-inf')
    best_st = None
    # Get most probable state and its backtrack
    for st, data in V[-1].items():
        if data["prob"] > max_prob:
            max_prob = data["prob"]
            best_st = st
    opt.append(best_st)
    previous = best_st
    print(best_st)

    # Follow the backtrack till the first observation
    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t + 1][previous]["prev"])
        previous = V[t + 1][previous]["prev"]

    print ("The steps of states are " + " ".join(opt) + " with highest probability of %s" % max_prob)
    
    with open(filename, 'w') as f:
      for v in opt:
        if v== 'La_Nina' :
             f.write('"La Nina"')
        else:
             f.write('"El Nino"')
        f.write('\n')

viterbi(obs, states, start_p, trans_p, emit_p,'data_wo_training.txt')

"""#Baum Welch Implementation"""

def forward(obs, states, start_p, tp, ep):
  V = [{}]
  for st in states:
      V[0][st] = {"prob": start_p[st] * ep[st][obs[0]], "prev": None}
  # Run Viterbi when t > 0
  sum = 0 
  for st in states:
      sum = sum + V[0][st]['prob']
  for st in states:
      V[0][st]['prob'] = V[0][st]['prob'] / sum

  for t in range(1, len(obs)):
      V.append({})
      for st in states:
          max_tr_prob = V[t - 1][states[0]]["prob"] * tp[states[0]][st]
          prev_st_selected = states[0]
          for prev_st in states[1:]:
              tr_prob = V[t - 1][prev_st]["prob"] * tp[prev_st][st]
              if tr_prob > max_tr_prob:
                  max_tr_prob = tr_prob
                  prev_st_selected = prev_st

          max_prob = max_tr_prob * ep[st][obs[t]] 
          V[t][st] = {"prob": max_prob, "prev": prev_st_selected}
     
      #normalizing 
      sum = 0 
      for st in states:
          sum = sum + V[t][st]['prob']
      if sum == 0 : continue
      for st in states:
          V[t][st]['prob'] = V[t][st]['prob'] / sum  
  #print(V)
  return V

forward(obs, states, start_p, trans_p, emit_p)

def backward(obs, states,  tp, ep):
  V = [{} for k in range(1000)]
  for st in states:
      V[len(obs)-1][st] = {"prob": 1 * ep[st][obs[len(obs)-1]], "prev": None}
  # Run Viterbi when t > 0
  sum = 0 
  for st in states:
      sum = sum + V[len(obs)-1][st]['prob']
  for st in states:
      V[len(obs)-1][st]['prob'] = V[len(obs)-1][st]['prob'] / sum

  for t in range(len(obs)-2, -1,-1):
      for st in states:
          max_tr_prob = V[t + 1][states[0]]["prob"] * tp[states[0]][st]
          prev_st_selected = states[0]
          for prev_st in states[1:]:
              tr_prob = V[t + 1][prev_st]["prob"] * tp[prev_st][st]
              if tr_prob > max_tr_prob:
                  max_tr_prob = tr_prob
                  prev_st_selected = prev_st

          max_prob = max_tr_prob * ep[st][obs[t]] 
          V[t][st] = {"prob": max_prob, "prev": prev_st_selected}
     
      #normalizing 
      sum = 0 
      for st in states:
          sum = sum + V[t][st]['prob']
      if sum == 0 : continue
      for st in states:
          V[t][st]['prob'] = V[t][st]['prob'] / sum  
  #print(V)
  return V

backward(obs, states,  trans_p, emit_p)

import numpy as np

def baum_welch(obs, states, start_p, tp, ep , n_iter=10):

  #calculate forward 
  mu_k = np.zeros(2)
  sigma_k = np.zeros(2)

  print('trans_p:', tp)
  print('emission_p:',ep)
  print('start_p: ', start_p)
  print('mu', mu_k)
  print('sigma',sigma_k)

  for step in range(n_iter):
        #calculate forward
        forw = forward(obs, states, start_p, tp, ep)
        #print('forward:',forw)
        #calculate backword
        backw = backward(obs, states,  tp, ep)
        #print('backward:',backw)
        forward_sink = 0 
        for st in states:
            forward_sink = forward_sink +  forw[len(obs)-1][st]['prob'] #last state probability summation 
        #print('forward_sink :',forward_sink)

        pi_star= np.zeros((2,len(obs)))
        for i in range(len(obs)):
          for st in range(len(states)):
              pi_star[st][i] = ( forw[i][states[st]]['prob'] * backw[i][states[st]]['prob'] / forward_sink )
              sum = 0 
              for st in range(len(states)):
                  sum = sum + pi_star[st][i]
              if sum == 0 : continue
              for st in range(len(states)):
                  pi_star[st][i] = pi_star[st][i] / sum
      
        pi_double_star = np.zeros((2,2,len(obs)))

        for i in range(len(obs)-1):
            sum = 0 
            for k in range(len(states)):
              for l in range(len(states)):
                  pi_double_star[k][l][i] = ( forw[i][states[k]]['prob'] * tp[states[k]][states[l]] * ep[states[l]][i+1] * backw[i+1][states[l]]['prob'] ) / forward_sink
                  sum = sum + pi_double_star[k][l][i]
            if sum == 0 : continue
            for k in range(len(states)):
              for l in range(len(states)):
                pi_double_star[k][l][i] = pi_double_star[k][l][i] / sum 

        #print(pi_double_star)

        #--calculate -- transition -- probability 

        for k in range(len(states)) :
          for l in range( len(states)):
              sum = 0
              for i in range(len(obs)):
                sum = sum + pi_double_star[k][l][i]
              tp[states[k]][states[l]] = sum 
        
        #normalize the transition probability  
        for k in range(len(states)):
          sum = 0
          for l in range(len(states)):
            sum = sum + tp[states[k]][states[l]]
          for l in range(len(states)):
            tp[states[k]][states[l]] = tp[states[k]][states[l]] / sum

        #print(trans_p)

        # find mu_k
       
        
        for k in range( len(states) ) :
          denumerator = 0
          numerator   = 0
          for i in range(len(obs)):
            numerator = numerator + pi_star[k][i] * em_arr[i] 
            denumerator = denumerator + pi_star[k][i]
          mu_k[k] = numerator / denumerator 
        
        #print('mu: ', mu_k)

       
        
        for k in range( len(states) ) :
          denumerator = 0
          numerator   = 0
          for i in range(len(obs)):
            numerator = numerator + pi_star[k][i] *  ( em_arr[i] - mu_k[k] ) *  ( em_arr[i] - mu_k[k] ) 
            denumerator = denumerator + pi_star[k][i]
          sigma_k[k] = math.sqrt(numerator / denumerator) 
        #print('sigma: ',sigma_k)


        #calculate emmission probability 

        el_emm = norm.pdf(em_arr,mu_k[0],math.sqrt(sigma_k[0]))
        la_emm = norm.pdf(em_arr,mu_k[0],math.sqrt(sigma_k[1]))

        for i in range(len(obs)):
          ep['El_Nino'][i] = el_emm[i]
          ep['La_Nina'][i] = la_emm[i]

        #print(emit_p)

        # #--calculate --- stationary probability ----
        # ck = ( trans_p[states[1]][states[0]] - trans_p[states[0]][states[0]] + 1 )
        # if ck != 0 : 
        #    start_p[states[0]] = (trans_p[states[1]][states[0]]) / ( trans_p[states[1]][states[0]] - trans_p[states[0]][states[0]] + 1 )
        # else :
        #    start_p[states[0]] = 0
        # start_p[states[1]] = 1 - start_p[states[0]]

  print('trans_p:', tp)
  print('emission_p:',ep)
  print('start_p: ', start_p)
  print('mu', mu_k)
  print('sigma',sigma_k)
  return tp,ep,start_p,mu_k,sigma_k

obs = []
for i in range (1000):
  obs.append(i)

states = ("El_Nino", "La_Nina")
start_p = {"El_Nino": 0.25, "La_Nina": 0.75 }
trans_p = {
    "El_Nino": {"El_Nino": 0.7, "La_Nina": 0.3},
    "La_Nina": {"El_Nino": 0.1, "La_Nina": 0.9},
}

emit_p = {}
emit_p['El_Nino']={}
emit_p['La_Nina']={}
for i in range(len(obs)):
  emit_p['El_Nino'][i] = el_nino_emm[i]
  emit_p['La_Nina'][i] = la_nina_emm[i]


tp,ep,start_p,mu_k,sigma_k = baum_welch(obs,states,start_p,trans_p,emit_p)
viterbi(obs, states, start_p, tp,ep,'data_with_training.txt')