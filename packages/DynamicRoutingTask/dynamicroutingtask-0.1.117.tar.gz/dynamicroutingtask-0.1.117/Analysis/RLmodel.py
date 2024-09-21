#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 14:47:48 2023

@author: samgale
"""

import copy
import glob
import os
import numpy as np
import scipy.stats
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['pdf.fonttype'] = 42
import sklearn.metrics
from DynamicRoutingAnalysisUtils import getSessionData, calcDprime
from RLmodelHPC import calcLogisticProb, runModel


baseDir = r"\\allen\programs\mindscope\workgroups\dynamicrouting\Sam"

clustData = np.load(os.path.join(baseDir,'clustData.npy'),allow_pickle=True).item()


# plot relationship bewtween tau and q values
q = np.arange(0,1.01,0.01)
beta = np.arange(51)
bias = (0,0.25)
xticks = np.arange(0,q.size+1,int(q.size/4))
yticks = np.arange(0,50,10)
for bi in bias:
    p = np.zeros((beta.size,q.size))
    for i,bt in enumerate(beta):
        p[i] = calcLogisticProb(q,bt,bi,0)
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    im = ax.imshow(p,clim=(0,1),cmap='magma',origin='lower',aspect='auto')
    ax.set_xticks(xticks)
    ax.set_xticklabels(np.round(q[xticks],1))
    ax.set_yticks(yticks)
    ax.set_yticklabels(beta[yticks])
    ax.set_xlabel('Q')
    ax.set_ylabel(r'$\beta$')
    ax.set_title('response probability, bias='+str(bi))
    plt.colorbar(im)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
for bt,clr in zip((2,40,30),'rgb'):
    for bi,ls in zip(bias,('-','--')):
        ax.plot(q,calcLogisticProb(q,bt,bi,0),color=clr,ls=ls,label=r'$\beta$='+str(bt)+', bias='+str(bi))
for side in ('right','top'):
    ax.spines[side].set_visible(False)
ax.tick_params(direction='out',top=False,right=False,labelsize=12)
ax.set_xticks(np.arange(-1,1.1,0.5))
ax.set_yticks(np.arange(0,1.1,0.5))
ax.set_xlim([0,1])
ax.set_ylim([0,1])
ax.set_xlabel('Q',fontsize=14)
ax.set_ylabel('response probability',fontsize=14)
ax.legend()
plt.tight_layout()



# get fit params from HPC output
fitClusters = False
if fitClusters:
    nClusters = 8
    clusterColors = [clr for clr in 'rgkbmcy']+['0.6']
    trainingPhases = ('clusters',)
    trainingPhaseColors = 'k'
else:
    trainingPhases = ('initial training','after learning')
    # trainingPhases = ('nogo','noAR','rewardOnly','no reward') 
    # trainingPhases = ('opto',)
    trainingPhaseColors = 'mgrbck'
if trainingPhases[0] == 'opto':
    modelTypes = ('contextRLOpto','mixedAgentRLOpto')
else:
    modelTypes = ('basicRL','contextRL','mixedAgentRL')#,'perseverativeRL')
modelTypeColors = 'krgb'

paramNames = {}
paramBounds = {}
fixedParamNames = {}
fixedParamValues = {}
nModelParams = {}
for modelType in modelTypes:
    paramNames[modelType] = ('betaAction','biasAction','lapseRate','biasAttention','visConf','audConf','wContext','alphaContext','decayContext','alphaReinforcement','rewardBias','rewardBiasDecay','wPerseveration','alphaPerseveration')
    paramBounds[modelType] = ([0,40],[-0.5,0.5],[0,0.5],[-1,1],[0.5,1],[0.5,1],[0,1],[0,1],[10,300],[0,0.5],[0,0.5],[1,30],[0,1],[0,1])
    if fitClusters:
        fixedParamNames[modelType] = ('Full model',)
        fixedParamValues[modelType] = (None,)
    elif modelType in ('contextRLOpto','mixedAgentRLOpto'):
        paramNames[modelType] += ('betaActionOpto','biasActionOpto')
        paramBounds[modelType] += ([0,40],[-1,1])
        fixedParamNames[modelType] = ('Full model',)
        fixedParamValues[modelType] = (None,)
        if modelType == 'contextRLOpto':
            fixedParamNames[modelType] += ('beta','bias')
            fixedParamValues[modelType] += (0,0)
        elif modelType == 'mixedAgentRLOpto':
            paramNames[modelType] += ('wContextOpto',)
            paramBounds[modelType] += ([0,1],)
            fixedParamNames[modelType] += ('beta,bias','wContext')
            fixedParamValues[modelType] += (0,0)
    else:
        fixedParamNames[modelType] = ('Full model','biasAction','lapseRate','biasAttention','visConf','audConf')
        fixedParamValues[modelType] = (None,0,0,0,1,1)
        if modelType == 'basicRL':
            fixedParamNames[modelType] += ('alphaReinforcement','rewardBias')
        else:
            fixedParamNames[modelType] += ('decayContext','alphaReinforcement','rewardBias')
        if modelType == 'contextRL':
            fixedParamNames[modelType] += (('decayContext','rewardBias'),)
        fixedParamValues[modelType] += (0,) * (len(fixedParamNames[modelType]) - 5)

modelTypeParams = {}
modelData = {phase: {} for phase in trainingPhases}
dirPath = os.path.join(baseDir,'RLmodel')
if trainingPhases[0] == 'opto':
    dirPath = os.path.join(dirPath,'opto')
elif fitClusters:
    dirPath = os.path.join(dirPath,'clusters')
filePaths = glob.glob(os.path.join(dirPath,'*.npz'))
for fileInd,f in enumerate(filePaths):
    print(fileInd)
    mouseId,sessionDate,sessionTime,trainingPhase,modelType = os.path.splitext(os.path.basename(f))[0].split('_')
    if trainingPhase not in trainingPhases or modelType not in modelTypes:
        continue
    session = sessionDate+'_'+sessionTime
    with np.load(f,allow_pickle=True) as data:
        if 'params' not in data:
            continue
        params = data['params']
        logLoss = data['logLoss']
        termMessage = data['terminationMessage']
        if 'trainSessions' in data:
            trainSessions = data['trainSessions']
        else:
            trainSessions = None
        if modelType not in modelTypeParams:
            modelTypeParams[modelType] = {key: val for key,val in data.items() if key not in ('params','logLoss','terminationMessage','trainSessions')}
            if 'optoLabel' in modelTypeParams[modelType] and len(modelTypeParams[modelType]['optoLabel'].shape)==0:
                modelTypeParams[modelType]['optoLabel'] = None
    d = modelData[trainingPhase]
    p = {'params': params, 'logLossTrain': logLoss, 'terminationMessage': termMessage, 'trainSessions': trainSessions}
    if mouseId not in d:
        d[mouseId] = {session: {modelType: p}}
    elif session not in d[mouseId]:
        d[mouseId][session] = {modelType: p}
    elif modelType not in d[mouseId][session]:
        d[mouseId][session][modelType] = p


# print fit termination message
# for trainingPhase in trainingPhases:
#     for mouse in modelData[trainingPhase]:
#         for session in modelData[trainingPhase][mouse]:
#             for modelType in modelTypes:
#                 print(modelData[trainingPhase][mouse][session][modelType]['terminationMessage'])


# get experiment data and model variables
sessionData = {phase: {} for phase in trainingPhases}  
for trainingPhase in trainingPhases:
    print(trainingPhase)
    d = modelData[trainingPhase]
    for mouse in d:
        for session in d[mouse]:
            if mouse not in sessionData[trainingPhase]:
                sessionData[trainingPhase][mouse] = {session: getSessionData(mouse,session)}
            elif session not in sessionData[trainingPhase][mouse]:
                sessionData[trainingPhase][mouse][session] = getSessionData(mouse,session)
            obj = sessionData[trainingPhase][mouse][session]
            naivePrediction = np.full(obj.nTrials,obj.trialResponse.mean())
            d[mouse][session]['Naive'] = {'logLossTest': sklearn.metrics.log_loss(obj.trialResponse,naivePrediction)}
            for modelType in modelTypes:
                s = d[mouse][session][modelType]
                if fitClusters:
                    s['pContext'] = [[] for _ in range(len(fixedParamNames[modelType]))]
                    s['qReinforcement'] = copy.deepcopy(s['pContext'])
                    s['qReward'] = copy.deepcopy(s['pContext'])
                    s['qTotal'] = copy.deepcopy(s['pContext'])
                    s['prediction'] = copy.deepcopy(s['pContext'])
                    s['logLossTest'] = [[[] for _ in range(nClusters)] for _ in range(len(fixedParamNames[modelType]))]
                    s['simulation'] = copy.deepcopy(s['pContext'])
                    s['simAction'] = copy.deepcopy(s['pContext'])
                    s['logLossSimulation'] = []
                    for i,prms in enumerate(s['params']):
                        for clustInd,params in enumerate(prms):
                            if np.all(np.isnan(params)):
                                pContext,qReinforcement,qReward,qTotal,pAction,action,pSimulate = [np.nan] * 7
                            else:
                                pContext,qReinforcement,qReward,qTotal,pAction,action = [val[0] for val in runModel(obj,*params,**modelTypeParams[modelType])]
                                pSimulate,simAction = runModel(obj,*params,useHistory=False,nReps=1,**modelTypeParams[modelType])[-2:]
                                pSimulate = np.mean(pSimulate,axis=0)
                                simAction = simAction[0]
                            s['pContext'][i].append(pContext)
                            s['qReinforcement'][i].append(qReinforcement)
                            s['qReward'][i].append(qReward)
                            s['qTotal'][i].append(qTotal)
                            s['prediction'][i].append(pAction)
                            s['simulation'][i].append(pSimulate)
                            s['simAction'][i].append(simAction)
                            resp = obj.trialResponse
                            pred = pAction
                            if not np.any(np.isnan(pred)):
                                clustTrials = clustData['trialCluster'][mouse][session] == clustInd+1
                                for blockInd in range(6):
                                    trials = clustTrials & (obj.trialBlock==blockInd+1)
                                    if np.any(trials):
                                        if np.all(resp[trials]):
                                            s['logLossTest'][i][clustInd].append(np.mean(np.log(pred[trials])))
                                        elif not np.any(resp[trials]):
                                            s['logLossTest'][i][clustInd].append(np.mean(np.log(1-pred[trials])))
                                        else:
                                            s['logLossTest'][i][clustInd].append(sklearn.metrics.log_loss(resp[trials],pred[trials]))
                else:
                    s['pContext'] = []
                    s['qReinforcement'] = []
                    s['qReward'] = []
                    s['qTotal'] = []
                    s['prediction'] = []
                    s['logLossTest'] = []
                    s['simulation'] = []
                    s['simAction'] = []
                    s['logLossSimulation'] = []                   
                    for i,params in enumerate(s['params']):
                        pContext,qReinforcement,qReward,qTotal,pAction,action = [val[0] for val in runModel(obj,*params,**modelTypeParams[modelType])]
                        s['pContext'].append(pContext)
                        s['qReinforcement'].append(qReinforcement)
                        s['qReward'].append(qReward)
                        s['qTotal'].append(qTotal)
                        s['prediction'].append(pAction)
                        if 'optoLabel' in modelTypeParams[modelType] and modelTypeParams[modelType]['optoLabel'] is not None:
                            trials = np.in1d(obj.trialOptoLabel,('no opto',)+tuple(modelTypeParams[modelType]['optoLabel']))
                        else:
                            trials = np.ones(obj.nTrials,dtype=bool)
                        s['logLossTest'].append(sklearn.metrics.log_loss(obj.trialResponse[trials],pAction[trials]))
                        pSimulate,simAction = runModel(obj,*params,useHistory=False,nReps=1,**modelTypeParams[modelType])[-2:]
                        pSimulate = np.mean(pSimulate,axis=0)
                        simAction = simAction[0]
                        s['simulation'].append(pSimulate)
                        s['simAction'].append(simAction)
                        s['logLossSimulation'].append(sklearn.metrics.log_loss(obj.trialResponse,pSimulate))


# simulate with missing parameters 
for trainingPhase in trainingPhases:
    d = modelData[trainingPhase]
    for mouse in d:
        for session in d[mouse]:
            for modelType in modelTypes:
                obj = sessionData[trainingPhase][mouse][session]
                s = d[mouse][session][modelType]
                s['simMissingParam'] = []
                s['simMissingParamAction'] = []                
                for fixedParam in fixedParamNames[modelType]:
                    params = s['params'][fixedParamNames[modelType].index('Full model')].copy()
                    if fixedParam != 'Full model':
                        params[paramNames[modelType].index(fixedParam)] = fixedParamValues[modelType][fixedParamNames[modelType].index(fixedParam)]
                    pSimulate,simAction = runModel(obj,*params,useHistory=False,nReps=1,**modelTypeParams[modelType])[-2:]
                    pSimulate = np.mean(pSimulate,axis=0)
                    simAction = simAction[0]
                    s['simMissingParam'].append(pSimulate)
                    s['simMissingParamAction'].append(simAction)

                        
# fit psytrack and  glmhmm
modelTypes += ('psytrack','glmhmm')
d = modelData['after learning']
for mouse in d:
    sessions = []
    params = []
    for session in d[mouse]:
        sessions.append(sessionData['after learning'][mouse][session])
        params.append(d[mouse][session]['mixedAgentRL']['params'][fixedParamNames['mixedAgentRL'].index('decayContext')])
    for modelType in ('psytrack','glmhmm'):
        if modelType == 'psytrack':
            inputs,weights,hyper,optList = getModelRegressors(modelType,modelTypeParams['mixedAgentRL'],np.mean(params,axis=0),sessions)
            hyp,evd,wMode,hessInfo = psytrack.hyperOpt(d,hyper,weights,optList)
            n = inputs['y'].size 
            i = n % cvFolds
            likelihood,probNoLick = psytrack.crossValidate(psytrack.trim(inputs,START=i), hyper, weights, optList, F=cvFolds, seed=0)
            likelihood,probNoLick = psytrack.crossValidate(psytrack.trim(inputs,END=n-i), hyper, weights, optList, F=cvFolds, seed=0)
        elif modelType == 'glmhmm':
            nCategories = 2 # binary choice (go/nogo)
            obsDim = 1 # number of observed dimensions (choice)
            inputDim = 4 # input dimensions
            nStates = 3
            # list of ntrials x nregressors array for each session
            inputs,resp = getModelRegressors(modelType,modelTypeParams['mixedAgentRL'],np.mean(params,axis=0),sessions)
            glmhmm = ssm.HMM(nStates,obsDim,inputDim,observations="input_driven_obs",observation_kwargs=dict(C=nCategories),transitions="standard")
            fitLL = glmhmm.fit(resp,inputs,method="em",num_iters=200,tolerance=10**-4)
            return -fitLL[-1]

                        

# model simulation with synthetic params
betaAction = 8
biasAction = 0.1
biasAttention = 0
visConfidence = 1
audConfidence = 1
wContext = 0
alphaContext = 0.4
decayContext = 20
alphaReinforcement = 0.01
rewardBias = 0
rewardBiasDecay = 16
wPerseveration = 0
alphaPerseveration = 0
betaActionOpto = 0
biasActionOpto = 0
valScalingOpto = 0
wContextOpto = 0

params = (betaAction,biasAction,biasAttention,visConfidence,audConfidence,wContext,alphaContext,decayContext,
          alphaReinforcement,rewardBias,rewardBiasDecay,wPerseveration,alphaPerseveration,
          betaActionOpto,biasActionOpto,valScalingOpto,wContextOpto)

trainingPhase = 'after learning'

fig = plt.figure(figsize=(8,4.5))
ax = fig.add_subplot(1,1,1)
preTrials = 15
postTrials = 15
x = np.arange(-preTrials,postTrials+1)    
ax.plot([0,0],[0,1],'--',color='0.5')
d = sessionData[trainingPhase]
for stimLbl,clr in zip(('rewarded target stim','unrewarded target stim'),'gm'):
    y = []
    for mouse in d:
        y.append([])
        for session in d[mouse]:
            obj = d[mouse][session]
            pAction = np.mean(runModel(obj,*params,useHistory=False,nReps=1)[-2],axis=0)
            for blockInd,rewStim in enumerate(obj.blockStimRewarded):
                if blockInd > 0:
                    stim = np.setdiff1d(obj.blockStimRewarded,rewStim) if 'unrewarded' in stimLbl else rewStim
                    trials = (obj.trialStim==stim)# & ~obj.autoRewardScheduled
                    y[-1].append(np.full(preTrials+postTrials+1,np.nan))
                    pre = pAction[(obj.trialBlock==blockInd) & trials]
                    i = min(preTrials,pre.size)
                    y[-1][-1][preTrials-i:preTrials] = pre[-i:]
                    post = pAction[(obj.trialBlock==blockInd+1) & trials]
                    i = min(postTrials,post.size)
                    y[-1][-1][preTrials+1:preTrials+1+i] = post[:i]
        y[-1] = np.nanmean(y[-1],axis=0)
    m = np.nanmean(y,axis=0)
    s = np.nanstd(y,axis=0)/(len(y)**0.5)
    ax.plot(x,m,color=clr,label=stimLbl)
    ax.fill_between(x,m+s,m-s,color=clr,alpha=0.25)
for side in ('right','top'):
    ax.spines[side].set_visible(False)
ax.tick_params(direction='out',top=False,right=False,labelsize=10)
ax.set_xticks(np.arange(-20,21,5))
ax.set_yticks([0,0.5,1])
ax.set_xlim([-preTrials-0.5,postTrials+0.5])
ax.set_ylim([0,1.01])
ax.set_xlabel('Trials of indicated type after block switch',fontsize=12)
ax.set_ylabel('Response rate',fontsize=12)
ax.legend(bbox_to_anchor=(1,1),loc='upper left',fontsize=12)
#ax.set_title(str(len(y))+' mice',fontsize=12)
plt.tight_layout()


# compare model prediction and model simulation            
for trainingPhase in trainingPhases:
    d = modelData[trainingPhase]
    for modelType in modelTypes:
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        pred = []
        sim = []
        for mouse in d:
            for session in d[mouse]: 
                s = d[mouse][session][modelType]
                pred.append(s['logLossTest'][0])
                sim.append(s['logLossSimulation'][0])
        ax.plot(pred,sim,'o',mec='k',mfc=None,alpha=0.25)
        ax.set_xlim([0,1.5])
        ax.set_ylim([0,1.5])
        ax.set_aspect('equal')
        ax.set_xlabel('log loss of model prediction')
        ax.set_ylabel('log loss of model simulation')
        slope,yint,rval,pval,stderr = scipy.stats.linregress(pred,sim)
        ax.set_title(trainingPhase+', '+modelType+'\nr = '+str(round(rval,2)))
 
for trainingPhase in trainingPhases:
    d = modelData[trainingPhase]
    for modelType in modelTypes:
        r = []  
        for mouse in d:
            for session in d[mouse]: 
                s = d[mouse][session][modelType]
                pred = s['prediction'][0]
                sim = s['simulation'][0]
                slope,yint,rval,pval,stderr = scipy.stats.linregress(pred,sim)
                r.append(rval**2)
        print(trainingPhase,modelType,round(np.median(r),2))
        

# get performance data
performanceData = {trainingPhase: {modelType: {} for modelType in modelTypes} for trainingPhase in trainingPhases}
for trainingPhase in trainingPhases:
    for modelType in modelTypes:
        for fixedParam in ('mice',) + fixedParamNames[modelType]:
            performanceData[trainingPhase][modelType][fixedParam] = {'respFirst': [],'respLast': [],'dprime': []}
            if fixedParam == 'mice':
                d = sessionData[trainingPhase]
            else:
                d = modelData[trainingPhase]
            for mouse in d:
                respFirst = []
                respLast = []
                dprime = []
                for session in d[mouse]:
                    obj = sessionData[trainingPhase][mouse][session]
                    if fixedParam == 'mice':
                        resp = obj.trialResponse
                    else:
                        resp = d[mouse][session][modelType]['prediction'][fixedParamNames[modelType].index(fixedParam)]
                    for blockInd,rewStim in enumerate(obj.blockStimRewarded):
                        for stim in ('vis1','sound1'):
                            stimTrials = (obj.trialStim==stim) & ~obj.autoRewardScheduled
                            trials = stimTrials & (obj.trialBlock==blockInd+1)
                            n = trials.sum()
                            r = resp[trials].mean()
                            if stim == rewStim:
                                hitRate = r
                                hitTrials = n
                            else:
                                falseAlarmRate = r
                                falseAlarmTrials = n
                                if blockInd > 0: 
                                    respFirst.append(resp[trials][0])
                                    respLast.append(resp[stimTrials & (obj.trialBlock==blockInd)][-1])
                        dprime.append(calcDprime(hitRate,falseAlarmRate,hitTrials,falseAlarmTrials))
                performanceData[trainingPhase][modelType][fixedParam]['respFirst'].append(np.mean(respFirst))
                performanceData[trainingPhase][modelType][fixedParam]['respLast'].append(np.mean(respLast))
                performanceData[trainingPhase][modelType][fixedParam]['dprime'].append(np.mean(dprime))


# plot performance data
for modelType in modelTypes:
    fig = plt.figure(figsize=(10,4))
    ax = fig.add_subplot(1,1,1)
    xlbls = ('mice',) + fixedParamNames[modelType]
    for trainingPhase,clr in zip(trainingPhases,trainingPhaseColors):
        for x,lbl in enumerate(xlbls):
            d = performanceData[trainingPhase][modelType][lbl]['dprime']
            m = np.mean(d)
            s = np.std(d)/(len(d)**0.5)
            lbl = trainingPhase if x==0 else None
            ax.plot(x,m,'o',mec=clr,mfc='none',ms=10,mew=2,label=lbl)
            ax.plot([x,x],[m-s,m+s],color=clr,lw=2)
    for side in ('right','top'):
        ax.spines[side].set_visible(False)
    ax.tick_params(direction='out',top=False,right=False)
    ax.set_xticks(np.arange(len(xlbls)))
    ax.set_xticklabels(['mice','full model']+[name+'='+str(val) for name,val in zip(fixedParamNames[modelType][1:],fixedParamValues[modelType][1:])])
    ax.set_xlim([-0.25,len(xlbls)+0.25])
    # ax.set_ylim([0,0.7])
    ax.set_ylabel('cross-modal d\'')
    ax.set_title(modelType)
    ax.legend(loc='upper right')
    plt.tight_layout()
    
fig = plt.figure(figsize=(16,4))
ax = fig.add_subplot(1,1,1)
xlbls = ('mice',) + fixedParamNames['contextRL']
for x,lbl in enumerate(xlbls):
    for i,(modelType,clr) in enumerate(zip(modelTypes[1:],modelTypeColors[1:])):
        if lbl=='mice':
            if i>0:
                continue
            c = 'k'
            lb = 'mice'
        else:
            c = clr
            lb = modelType if x==1 else None
        d = performanceData['after learning'][modelType][lbl]['dprime']
        m = np.mean(d)
        s = np.std(d)/(len(d)**0.5)
        ax.plot(x,m,'o',mec=c,mfc='none',ms=10,mew=2,label=lb)
        ax.plot([x,x],[m-s,m+s],color=c,lw=2)
for side in ('right','top'):
    ax.spines[side].set_visible(False)
ax.tick_params(direction='out',top=False,right=False)
ax.set_xticks(np.arange(len(xlbls)))
ax.set_xticklabels(['mice','full model']+[name+'='+str(val) for name,val in zip(fixedParamNames[modelType][1:],fixedParamValues[modelType][1:])])
ax.set_xlim([-0.25,len(xlbls)+0.25])
# ax.set_ylim([0,0.7])
ax.set_ylabel('cross-modal d\'')
ax.set_title('after learning')
ax.legend(loc='lower left')
plt.tight_layout()
    
for modelType in modelTypes:
    fig = plt.figure(figsize=(10,4))
    ax = fig.add_subplot(1,1,1)
    xlbls = ('mice',) + fixedParamNames[modelType]
    ax.plot([-1,len(xlbls)+1],[0,0],'k--')
    for trainingPhase,clr in zip(trainingPhases,trainingPhaseColors):
        for x,lbl in enumerate(xlbls):
            respFirst = performanceData[trainingPhase][modelType][lbl]['respFirst']
            respLast = performanceData[trainingPhase][modelType][lbl]['respLast']
            d = np.array(respFirst) - np.array(respLast)
            m = np.mean(d)
            s = np.std(d)/(len(d)**0.5)
            lbl = trainingPhase if x==0 else None
            ax.plot(x,m,'o',mec=clr,mfc='none',ms=10,mew=2,label=lbl)
            ax.plot([x,x],[m-s,m+s],color=clr,lw=2)
    for side in ('right','top'):
        ax.spines[side].set_visible(False)
    ax.tick_params(direction='out',top=False,right=False)
    ax.set_xticks(np.arange(len(xlbls)))
    ax.set_xticklabels(['mice','full model']+[name+'='+str(val) for name,val in zip(fixedParamNames[modelType][1:],fixedParamValues[modelType][1:])])
    ax.set_xlim([-0.25,len(xlbls)+0.25])
    # ax.set_ylim([0,0.7])
    ax.set_ylabel('$\Delta$ Response rate to non-rewarded target\n(first trial - last trial previous block)')
    ax.set_title(modelType)
    ax.legend(loc='lower right')
    plt.tight_layout()

fig = plt.figure(figsize=(16,4))
ax = fig.add_subplot(1,1,1)
xlbls = ('mice',) + fixedParamNames['contextRL']
ax.plot([-1,len(xlbls)+1],[0,0],'k--')
for x,lbl in enumerate(xlbls):
    for i,(modelType,clr) in enumerate(zip(modelTypes[1:],modelTypeColors[1:])):
        if lbl=='mice':
            if i>0:
                continue
            c = 'k'
            lb = 'mice'
        else:
            c = clr
            lb = modelType if x==1 else None
        respFirst = performanceData[trainingPhase][modelType][lbl]['respFirst']
        respLast = performanceData[trainingPhase][modelType][lbl]['respLast']
        d = np.array(respFirst) - np.array(respLast)
        m = np.mean(d)
        s = np.std(d)/(len(d)**0.5)
        ax.plot(x,m,'o',mec=c,mfc='none',ms=10,mew=2,label=lb)
        ax.plot([x,x],[m-s,m+s],color=c,lw=2)
for side in ('right','top'):
    ax.spines[side].set_visible(False)
ax.tick_params(direction='out',top=False,right=False)
ax.set_xticks(np.arange(len(xlbls)))
ax.set_xticklabels(['mice','full model']+[name+'='+str(val) for name,val in zip(fixedParamNames[modelType][1:],fixedParamValues[modelType][1:])])
ax.set_xlim([-0.25,len(xlbls)+0.25])
# ax.set_ylim([0,0.7])
ax.set_ylabel('$\Delta$ Response rate to non-rewarded target\n(first trial - last trial previous block)')
ax.set_title('after learning')
ax.legend(loc='upper left')
plt.tight_layout()


# plot logloss
fig = plt.figure(figsize=(14,4))
ax = fig.add_subplot(1,1,1)
xlbls = ('Naive',) + modelTypes
for trainingPhase,clr in zip(trainingPhases,trainingPhaseColors):
    d = modelData[trainingPhase]
    if len(d) > 0:
        for x,xlbl in enumerate(xlbls):
            val = np.array([np.mean([session[xlbl]['logLossTest'] for session in mouse.values()],axis=0) for mouse in d.values()])
            if xlbl != 'Naive':
                val = val[:,fixedParamNames[xlbl].index('Full model')]
            m = val.mean()
            s = val.std()/(len(val)**0.5)
            lbl = trainingPhase if x==0 else None
            ax.plot(x,m,'o',mec=clr,mfc='none',ms=10,mew=2,label=lbl)
            ax.plot([x,x],[m-s,m+s],color=clr,lw=2)
for side in ('right','top'):
    ax.spines[side].set_visible(False)
ax.tick_params(direction='out',top=False,right=False)
ax.set_xticks(np.arange(len(xlbls)))
ax.set_xticklabels(('Naive model\n(constant response probability)',) + modelTypes)
ax.set_xlim([-0.25,len(xlbls)+0.25])
ax.set_ylim([0,0.7])
ax.set_ylabel('Negative log-likelihood')
ax.legend(loc='lower right')
plt.tight_layout()

fig = plt.figure(figsize=(14,4))
ax = fig.add_subplot(1,1,1)
xlbls = ('Naive',) + modelTypes
for trainingPhase,clr in zip(trainingPhases,trainingPhaseColors):
    d = modelData[trainingPhase]
    if len(d) > 0:
        naive = np.array([np.mean([session['Naive']['logLossTest'] for session in mouse.values()],axis=0) for mouse in d.values()])
        for x,xlbl in enumerate(xlbls):
            val = np.array([np.mean([session[xlbl]['logLossTest'] for session in mouse.values()],axis=0) for mouse in d.values()])
            if xlbl != 'Naive':
                val = val[:,fixedParamNames[xlbl].index('Full model')]
            val -= naive
            m = val.mean()
            s = val.std()/(len(val)**0.5)
            lbl = trainingPhase if x==0 else None
            ax.plot(x,m,'o',mec=clr,mfc='none',ms=10,mew=2,label=lbl)
            ax.plot([x,x],[m-s,m+s],color=clr,lw=2)
for side in ('right','top'):
    ax.spines[side].set_visible(False)
ax.tick_params(direction='out',top=False,right=False)
ax.set_xticks(np.arange(len(xlbls)))
ax.set_xticklabels(('Naive model\n(constant response probability)',) + modelTypes)
ax.set_xlim([-0.25,len(xlbls)+0.25])
# ax.set_ylim([0,0.7])
ax.set_ylabel('Negative log-likelihood')
ax.legend(loc='lower right')
plt.tight_layout()

for modelType in modelTypes:
    fig = plt.figure(figsize=(10,4))
    ax = fig.add_subplot(1,1,1)
    xticks = np.arange(len(fixedParamNames[modelType]))
    xlim = [-0.25,xticks[-1]+0.25]
    ax.plot(xlim,[0,0],'--',color='0.5')
    for trainingPhase,clr in zip(trainingPhases,trainingPhaseColors):
        d = modelData[trainingPhase]
        if len(d) > 0:
            val = np.array([np.mean([session[modelType]['logLossTest'] for session in mouse.values()],axis=0) for mouse in d.values()])
            val -= val[:,fixedParamNames[modelType].index('Full model')][:,None]
            mean = val.mean(axis=0)
            sem = val.std(axis=0)/(len(val)**0.5)
            ax.plot(xticks,mean,'o',mec=clr,mfc='none',ms=10,mew=2,label=trainingPhase)
            for x,m,s in zip(xticks,mean,sem):
                ax.plot([x,x],[m-s,m+s],color=clr,lw=2)
    for side in ('right','top'):
        ax.spines[side].set_visible(False)
    ax.tick_params(direction='out',top=False,right=False)
    ax.set_xticks(xticks)
    ax.set_xticklabels([fixedParamNames[modelType][0]]+[name+'='+str(val) for name,val in zip(fixedParamNames[modelType][1:],fixedParamValues[modelType][1:])])
    ax.set_xlim(xlim)
    ax.set_ylim([-0.03,0.09])
    ax.set_ylabel(r'$\Delta$ NLL')
    ax.set_title(modelType)
    ax.legend(loc='upper left')
    plt.tight_layout()
    
fig = plt.figure(figsize=(14,4))
ax = fig.add_subplot(1,1,1)
xticks = np.arange(len(fixedParamNames['mixedAgentRL']))
xlim = [-0.25,xticks[-1]+0.25]
ax.plot(xlim,[0,0],'--',color='0.5')
for modelType,clr in zip(modelTypes,modelTypeColors):
    d = modelData['after learning']
    if len(d) > 0:
        val = np.array([np.mean([session[modelType]['logLossTest'] for session in mouse.values()],axis=0) for mouse in d.values()])
        val -= val[:,fixedParamNames[modelType].index('Full model')][:,None]
        mean = val.mean(axis=0)
        sem = val.std(axis=0)/(len(val)**0.5)
        ax.plot(xticks,mean,'o',mec=clr,mfc='none',ms=10,mew=2,label=modelType)
        for x,m,s in zip(xticks,mean,sem):
            ax.plot([x,x],[m-s,m+s],color=clr,lw=2)
for side in ('right','top'):
    ax.spines[side].set_visible(False)
ax.tick_params(direction='out',top=False,right=False)
ax.set_xticks(xticks)
ax.set_xticklabels([fixedParamNames[modelType][0]]+[name+'='+str(val) for name,val in zip(fixedParamNames[modelType][1:],fixedParamValues[modelType][1:])])
ax.set_xlim(xlim)
ax.set_ylabel(r'$\Delta$ NLL')
ax.set_title('after learning')
ax.legend(loc='upper left')
plt.tight_layout()

for modelType in modelTypes:
    fig = plt.figure(figsize=(5,10))
    for i,(fixedParam,fixedVal) in enumerate(zip(fixedParamNames[modelType],fixedParamValues[modelType])):
        ax = fig.add_subplot(len(fixedParamNames[modelType]),1,i+1)
        ax.plot([0,0],[0,1],'--',color='0.5')
        for trainingPhase,clr in zip(trainingPhases,trainingPhaseColors):
            d = modelData[trainingPhase]
            if len(d) > 0:
                logLoss = np.array([np.mean([session[modelType]['logLossTest'] for session in mouse.values()],axis=0) for mouse in d.values()])          
                logLoss = logLoss[:,i] - logLoss[:,fixedParamNames[modelType].index('Full model')] if fixedParam != 'Full model' else logLoss[:,i]
                dsort = np.sort(logLoss)
                cumProb = np.array([np.sum(dsort<=i)/dsort.size for i in dsort])
                ax.plot(dsort,cumProb,color=clr,label=trainingPhase)
        for side in ('right','top'):
            ax.spines[side].set_visible(False)
        ax.tick_params(direction='out',top=False,right=False)
        ax.set_xlim(([0,1] if fixedParam == 'Full model' else [-0.05,0.2]))
        ax.set_ylim([0,1.01])
        ax.set_xlabel(('NLL' if fixedParam == 'Full model' else r'$\Delta$ NLL'))
        ax.set_title((fixedParam+' (modelType'+')' if fixedParam == 'Full model' else fixedParam+'='+str(fixedVal)))
        if i==0:
            ax.legend(loc='upper left',bbox_to_anchor=(1,1))
    plt.tight_layout()
    
fig = plt.figure(figsize=(8,10))
modelType = 'multiAgent'
nrows = len(fixedParamNames[modelType])//2 + 1
gs = matplotlib.gridspec.GridSpec(nrows,2)
for i,(fixedParam,fixedVal) in enumerate(zip(fixedParamNames[modelType],fixedParamValues[modelType])):
    if i < nrows:
        row = i
        col = 0
    else:
        row = i-nrows+1
        col = 1
    ax = fig.add_subplot(gs[row,col])
    ax.plot([0,0],[0,1],'--',color='0.5')
    for modelType,clr in zip(modelTypes,modelTypeColors):
        d = modelData[trainingPhase]
        if len(d) > 0:
            logLoss = np.array([np.mean([session[modelType]['logLossTest'] for session in mouse.values()],axis=0) for mouse in d.values()])          
            logLoss = logLoss[:,i] - logLoss[:,fixedParamNames[modelType].index('Full model')] if fixedParam != 'Full model' else logLoss[:,i]
            dsort = np.sort(logLoss)
            cumProb = np.array([np.sum(dsort<=i)/dsort.size for i in dsort])
            ax.plot(dsort,cumProb,color=clr,label=(modelType if i==0 else None))
    for side in ('right','top'):
        ax.spines[side].set_visible(False)
    ax.tick_params(direction='out',top=False,right=False)
    ax.set_xlim(([0,1] if fixedParam == 'Full model' else [-0.05,0.2]))
    ax.set_ylim([0,1.01])
    ax.set_xlabel(('NLL' if fixedParam == 'Full model' else r'$\Delta$ NLL'))
    if i==nrows//2:
        ax.set_ylabel('Cumulative fracion of mice')
    ax.set_title((fixedParam if fixedParam == 'Full model' else fixedParam+'='+str(fixedVal)))
    if i==0:
        ax.legend(loc='upper left',bbox_to_anchor=(1,1))
plt.tight_layout()
                
                
# plot param values
for modelType in modelTypes:
    fig = plt.figure(figsize=(11,11))
    gs = matplotlib.gridspec.GridSpec(len(fixedParamNames[modelType]),len(paramNames[modelType]))
    for i,(fixedParam,fixedVal) in enumerate(zip(fixedParamNames[modelType],fixedParamValues[modelType])):
        for j,(param,xlim) in enumerate(zip(paramNames[modelType],paramBounds[modelType])):
            ax = fig.add_subplot(gs[i,j])
            for trainingPhase,clr in zip(trainingPhases,trainingPhaseColors):
                d = modelData[trainingPhase]
                if len(d) > 0:
                    paramVals = np.array([np.mean([session[modelType]['params'][i,j] for session in mouse.values()]) for mouse in d.values()])
                    if len(np.unique(paramVals)) > 1:
                        dsort = np.sort(paramVals)
                        cumProb = np.array([np.sum(dsort<=s)/dsort.size for s in dsort])
                        ax.plot(dsort,cumProb,color=clr,label=trainingPhase)
                        if trainingPhase=='after learning' and fixedParam in ('Full model','decayContext'):
                            print(modelType,fixedParam,param,np.median(paramVals))
                    else:
                        ax.plot(paramVals[0],1,'o',mfc=clr,mec=clr)
                        if trainingPhase=='after learning' and fixedParam in ('Full model','decayContext'):
                            print(modelType,fixedParam,param,paramVals[0])
            for side in ('right','top'):
                ax.spines[side].set_visible(False)
            ax.tick_params(direction='out',top=False,right=False)
            ax.set_xlim([xlim[0]-0.02,xlim[1]+0.02])
            ax.set_ylim([0,1.01])
            if j>0:
                ax.set_yticklabels([])
            if i<len(fixedParamNames[modelType])-1:
                ax.set_xticklabels([])
            else:
                ax.set_xlabel(param)
            if j==0 and i==len(fixedParamNames[modelType])//2:
                ax.set_ylabel('Cum. Prob.')
            if j==len(paramNames[modelType])//2:
                ax.set_title((fixedParam+'('+modelType+')' if fixedParam == 'Full model' else fixedParam+'='+str(fixedVal)))
            if i==0 and j==len(paramNames[modelType])-1:
                ax.legend(bbox_to_anchor=(1,1))
    plt.tight_layout()
    
fig = plt.figure(figsize=(14,11))
modelType = 'contextRL'
gs = matplotlib.gridspec.GridSpec(len(fixedParamNames[modelType]),len(paramNames[modelType]))
for i,(fixedParam,fixedVal) in enumerate(zip(fixedParamNames[modelType],fixedParamValues[modelType])):
    for j,(param,xlim) in enumerate(zip(paramNames[modelType],paramBounds[modelType])):
        ax = fig.add_subplot(gs[i,j])
        for modelType,clr in zip(modelTypes[1:],modelTypeColors[1:]):
            d = modelData['after learning']
            if len(d) > 0:
                paramVals = np.array([np.mean([session[modelType]['params'][i,j] for session in mouse.values()]) for mouse in d.values()])
                if len(np.unique(paramVals)) > 1:
                    dsort = np.sort(paramVals)
                    cumProb = np.array([np.sum(dsort<=s)/dsort.size for s in dsort])
                    ax.plot(dsort,cumProb,color=clr,label=(modelType if i==0 and j==len(paramNames[modelType])-1 else None))
                    print(modelType,param,np.median(paramVals))
                else:
                    ax.plot(paramVals[0],1,'o',mfc=clr,mec=clr)
        for side in ('right','top'):
            ax.spines[side].set_visible(False)
        ax.tick_params(direction='out',top=False,right=False)
        ax.set_xlim([xlim[0]-0.02,xlim[1]+0.02])
        ax.set_ylim([0,1.01])
        if j>0:
            ax.set_yticklabels([])
        if i<len(fixedParamNames[modelType])-1:
            ax.set_xticklabels([])
        else:
            ax.set_xlabel(param)
        if j==0 and i==len(fixedParamNames[modelType])//2:
            ax.set_ylabel('Cum. Prob.')
        if j==len(paramNames[modelType])//2:
            ax.set_title((fixedParam+'(after learning)' if fixedParam == 'Full model' else fixedParam+'='+str(fixedVal)))
        if i==0 and j==len(paramNames[modelType])-1:
            ax.legend(bbox_to_anchor=(1,1))
plt.tight_layout()


# opto
trainingPhase = 'opto'
optoLbl = ('lFC','PFC')
stimNames = ('vis1','vis2','sound1','sound2')
xticks = np.arange(len(stimNames))

for modelType in modelTypes:
    for i,(fixedParam,fixedVal) in enumerate(zip(('mice',) + fixedParamNames[modelType],(None,)+fixedParamValues[modelType])):
        if fixedParam == 'mice':
            d = sessionData[trainingPhase]
        else:
            d = modelData[trainingPhase]
        fig = plt.figure()
        fig.suptitle(modelType+', '+fixedParam)
        for i,goStim in enumerate(('vis1','sound1')):
            ax = fig.add_subplot(2,1,i+1)
            for lbl,clr in zip(('no opto',optoLbl),'kb'):
                rr = []
                for mouse in d:
                    n = np.zeros(len(stimNames))
                    resp = n.copy()
                    for session in d[mouse]:
                        obj = sessionData[trainingPhase][mouse][session]
                        if fixedParam == 'mice':
                            r = obj.trialResponse
                        else:
                            r = d[mouse][session][modelType]['simulation'][fixedParamNames[modelType].index(fixedParam)]
                        blockTrials = (obj.rewardedStim==goStim) & ~obj.autoRewardScheduled
                        optoTrials = obj.trialOptoLabel=='no opto' if lbl=='no opto' else np.in1d(obj.trialOptoLabel,lbl)
                        for j,stim in enumerate(stimNames):
                            trials = blockTrials & optoTrials & (obj.trialStim==stim)
                            n[j] += trials.sum()
                            resp[j] += r[trials].sum()
                    rr.append(resp/n)
                mean = np.mean(rr,axis=0)
                sem = np.std(rr,axis=0)/(len(rr)**0.5)
                ax.plot(xticks,mean,color=clr,lw=2,label=lbl)
                for x,m,s in zip(xticks,mean,sem):
                    ax.plot([x,x],[m-s,m+s],color=clr,lw=2)
            for side in ('right','top'):
                ax.spines[side].set_visible(False)
            ax.tick_params(direction='out',top=False,right=False)
            ax.set_xticks(xticks)
            if i==1:
                ax.set_xticklabels(stimNames)
            else:
                ax.set_xticklabels([])
            ax.set_xlim([-0.25,len(stimNames)-0.75])
            ax.set_ylim([-0.01,1.01])
            ax.set_ylabel('Response Rate')
            ax.legend(bbox_to_anchor=(1,1),loc='upper left')
        plt.tight_layout()



# compare model and mice
for modelType in modelTypes:
    var = 'simMissingParam' #'simulation'
    stimNames = ('vis1','vis2','sound1','sound2')
    preTrials = 5
    postTrials = 15
    x = np.arange(-preTrials,postTrials+1)
    for trainingPhase in trainingPhases:
        fig = plt.figure(figsize=(12,10))
        nRows = int(np.ceil((len(fixedParamNames[modelType])+1)/2))
        gs = matplotlib.gridspec.GridSpec(nRows,4)
        for i,(fixedParam,fixedVal) in enumerate(zip(('mice',) + fixedParamNames[modelType],(None,)+fixedParamValues[modelType])):
            if fixedParam == 'mice':
                d = sessionData[trainingPhase]
            else:
                d = modelData[trainingPhase]
            if len(d) == 0:
                continue
            for j,(rewardStim,blockLabel) in enumerate(zip(('vis1','sound1'),('visual rewarded blocks','sound rewarded blocks'))):
                if i>=nRows:
                    row = i-nRows
                    col = j+2
                else:
                    row,col = i,j
                ax = fig.add_subplot(gs[row,col])
                for stim,clr,ls in zip(stimNames,'ggmm',('-','--','-','--')):
                    y = []
                    for mouse in d:
                        y.append([])
                        for session in d[mouse]:
                            obj = sessionData[trainingPhase][mouse][session]
                            if fixedParam == 'mice':
                                resp = obj.trialResponse
                            else:
                                resp = d[mouse][session][modelType][var][fixedParamNames[modelType].index(fixedParam)]
                            for blockInd,rewStim in enumerate(obj.blockStimRewarded):
                                if rewStim==rewardStim and blockInd > 0:
                                    trials = (obj.trialStim==stim) #& ~obj.autoRewardScheduled
                                    y[-1].append(np.full(preTrials+postTrials+1,np.nan))
                                    pre = resp[(obj.trialBlock==blockInd) & trials]
                                    k = min(preTrials,pre.size)
                                    y[-1][-1][preTrials-k:preTrials] = pre[-k:]
                                    post = resp[(obj.trialBlock==blockInd+1) & trials]
                                    k = min(postTrials,post.size)
                                    y[-1][-1][preTrials+1:preTrials+1+k] = post[:k]
                        y[-1] = np.nanmean(y[-1],axis=0)
                    m = np.nanmean(y,axis=0)
                    s = np.nanstd(y,axis=0)/(len(y)**0.5)
                    ax.plot(x,m,color=clr,ls=ls,label=stim)
                    ax.fill_between(x,m+s,m-s,color=clr,alpha=0.25)
                for side in ('right','top'):
                    ax.spines[side].set_visible(False)
                ax.tick_params(direction='out',top=False,right=False)
                ax.set_xticks(np.arange(-5,20,5))
                ax.set_yticks([0,0.5,1])
                ax.set_xlim([-preTrials-0.5,postTrials+0.5])
                ax.set_ylim([0,1.01])
                if i==len(fixedParamNames[modelType]):
                    ax.set_xlabel('Trials after block switch')
                if j==0:
                    ax.set_ylabel(('Response\nrate' if fixedParam=='mice' else var))
                if fixedParam=='mice':
                    title = 'mice, '+blockLabel+' (n='+str(len(y))+')'
                elif fixedParam=='Full model':
                    title = fixedParam + '(' + modelType + ')'
                else:
                    title = fixedParam+'='+str(fixedVal)
                ax.set_title(title)
                if i==0 and j==1:
                    ax.legend(bbox_to_anchor=(1,1))
        plt.tight_layout()

# first block  
for modelType in modelTypes:        
    preTrials = 0
    postTrials = 15
    x = np.arange(-preTrials,postTrials+1)
    a = -1
    for var,yticks,ylim,ylbl in zip(('simulation','expectedValue'),([0,0.5,1],[-1,0,1]),([0,1.01],[-1.01,1.01]),('Response\nrate','Expected\nvalue')):
        if var=='expectedValue':
            continue
        for trainingPhase in trainingPhases:
            fig = plt.figure(figsize=(8,10))
            gs = matplotlib.gridspec.GridSpec(3,2)#len(fixedParamNames[modelType])+1,2)
            for i,(fixedParam,fixedVal) in enumerate(zip(('mice',) + fixedParamNames[modelType],(None,)+fixedParamValues[modelType])):
                if fixedParam == 'mice':
                    d = sessionData[trainingPhase]
                elif fixedParam in ('Full model','alphaReinforcement'):
                    d = modelData[trainingPhase]
                else:
                    continue
                if len(d) == 0:
                    continue
                a += 1
                for j,(rewardStim,blockLabel) in enumerate(zip(('vis1','sound1'),('visual rewarded blocks','sound rewarded blocks'))):
                    ax = fig.add_subplot(gs[a,j])
                    for stim,clr,ls in zip(stimNames,'ggmm',('-','--','-','--')):
                        y = []
                        for mouse in d:
                            y.append([])
                            for session in d[mouse]:
                                obj = sessionData[trainingPhase][mouse][session]
                                if fixedParam == 'mice':
                                    resp = obj.trialResponse
                                else:
                                    resp = d[mouse][session][modelType][var][fixedParamNames[modelType].index(fixedParam)]
                                for blockInd,rewStim in enumerate(obj.blockStimRewarded):
                                    if rewStim==rewardStim and blockInd == 0:
                                        trials = (obj.trialStim==stim) #& ~obj.autoRewardScheduled
                                        y[-1].append(np.full(preTrials+postTrials+1,np.nan))
                                        pre = resp[(obj.trialBlock==blockInd) & trials]
                                        k = min(preTrials,pre.size)
                                        y[-1][-1][preTrials-k:preTrials] = pre[-k:]
                                        post = resp[(obj.trialBlock==blockInd+1) & trials]
                                        k = min(postTrials,post.size)
                                        y[-1][-1][preTrials+1:preTrials+1+k] = post[:k]
                            y[-1] = np.nanmean(y[-1],axis=0)
                        m = np.nanmean(y,axis=0)
                        s = np.nanstd(y,axis=0)/(len(y)**0.5)
                        ax.plot(x,m,color=clr,ls=ls,label=stim)
                        ax.fill_between(x,m+s,m-s,color=clr,alpha=0.25)
                    for side in ('right','top'):
                        ax.spines[side].set_visible(False)
                    ax.tick_params(direction='out',top=False,right=False)
                    ax.set_xticks(np.arange(-5,20,5))
                    ax.set_yticks(([0,0.5,1] if fixedParam=='mice' else yticks))
                    ax.set_xlim([-preTrials-0.5,postTrials+0.5])
                    ax.set_ylim(([0,1.01] if fixedParam=='mice' else ylim))
                    if i==len(fixedParamNames):
                        ax.set_xlabel('Trials after block switch')
                    if j==0:
                        ax.set_ylabel(('Response\nrate' if fixedParam=='mice' else ylbl))
                    if fixedParam=='mice':
                        title = 'mice, '+blockLabel+' (n='+str(len(y))+')'
                    elif fixedParam=='Full model':
                        title = fixedParam
                    else:
                        title = fixedParam+'='+str(fixedVal)
                    ax.set_title(title)
                    if i==0 and j==1:
                        ax.legend(bbox_to_anchor=(1,1))
            plt.tight_layout()
        
        
# less plots
var = 'simulation'
stimNames = ('vis1','vis2','sound1','sound2')
stimLabels = ('visual target','visual non-target','auditory target','auditory non-target')
preTrials = 5
postTrials = 15
x = np.arange(-preTrials,postTrials+1)
for modelType in ('contextRL',): #modelTypes:
    for trainingPhase in trainingPhases:
        for fixedParam in ('mice','Full model','alphaReinforcement','wReward','decayContext'):
            if fixedParam == 'mice' and modelType=='basicRL':
                d = sessionData[trainingPhase]
            elif fixedParam in fixedParamNames[modelType]:
                d = modelData[trainingPhase]
            else:
                continue
            fig = plt.figure(figsize=(8,4.5))
            if fixedParam=='mice':
                title = 'Mice, '+trainingPhase
            else:
                title = modelType + ', ' + trainingPhase + ', ' + fixedParam
            fig.suptitle(title)
            for i,(rewardStim,blockLabel) in enumerate(zip(('vis1','sound1'),('visual rewarded blocks','auditory rewarded blocks'))):
                ax = fig.add_subplot(1,2,i+1)
                for stim,stimLbl,clr,ls in zip(stimNames,stimLabels,'ggmm',('-','--','-','--')):
                    y = []
                    for mouse in d:
                        y.append([])
                        for session in d[mouse]:
                            obj = sessionData[trainingPhase][mouse][session]
                            if fixedParam == 'mice':
                                resp = obj.trialResponse
                            else:
                                resp = d[mouse][session][modelType][var][fixedParamNames[modelType].index(fixedParam)]
                            for blockInd,rewStim in enumerate(obj.blockStimRewarded):
                                if rewStim==rewardStim and blockInd > 0:
                                    trials = (obj.trialStim==stim) #& ~obj.autoRewardScheduled
                                    y[-1].append(np.full(preTrials+postTrials+1,np.nan))
                                    pre = resp[(obj.trialBlock==blockInd) & trials]
                                    k = min(preTrials,pre.size)
                                    y[-1][-1][preTrials-k:preTrials] = pre[-k:]
                                    post = resp[(obj.trialBlock==blockInd+1) & trials]
                                    k = min(postTrials,post.size)
                                    y[-1][-1][preTrials+1:preTrials+1+k] = post[:k]
                        y[-1] = np.nanmean(y[-1],axis=0)
                    m = np.nanmean(y,axis=0)
                    s = np.nanstd(y,axis=0)/(len(y)**0.5)
                    ax.plot(x,m,color=clr,ls=ls,label=stimLbl)
                    ax.fill_between(x,m+s,m-s,color=clr,alpha=0.25)
                for side in ('right','top'):
                    ax.spines[side].set_visible(False)
                ax.tick_params(direction='out',top=False,right=False)
                ax.set_xticks(np.arange(-5,20,5))
                ax.set_yticks([0,0.5,1])
                ax.set_xlim([-preTrials-0.5,postTrials+0.5])
                ax.set_ylim([0,1.01])
                ax.set_xlabel('Trials after block switch')
                if i==0:
                    ax.set_ylabel('Response rate')
                ax.set_title(blockLabel)
                if i==1:
                    ax.legend(loc='upper left',bbox_to_anchor=(1,1))
            plt.tight_layout()
        

# plot pContext and wHabit
modelType = 'contextQ'
preTrials = 20
postTrials = 60
x = np.arange(-preTrials,postTrials+1)
for var,ylbl in zip(('pContext','wHabit'),('Context belief','Habit weight')):
    for trainingPhase in trainingPhases:
        d = modelData[trainingPhase]
        if len(d) == 0:
            continue
        fig = plt.figure(figsize=(10,10))
        gs = matplotlib.gridspec.GridSpec(len(fixedParamNames),2)
        for i,(fixedParam,fixedVal) in enumerate(zip(fixedParamNames,fixedParamValues)):
            for j,(rewardStim,blockLabel) in enumerate(zip(('vis1','sound1'),('visual rewarded blocks','sound rewarded blocks'))):
                ax = fig.add_subplot(gs[i,j])
                contexts,clrs = (('visual','auditory'),'gm') if var=='pContext' else ((None,),'k')
                for contextInd,(context,clr) in enumerate(zip(contexts,clrs)):
                    y = []
                    for mouse in d:
                        y.append([])
                        for session in d[mouse]:
                            obj = sessionData[trainingPhase][mouse][session]
                            v = d[mouse][session][modelType][var][fixedParamNames.index(fixedParam)]
                            if var=='pContext':
                                v = v[:,contextInd]
                            for blockInd,rewStim in enumerate(obj.blockStimRewarded):
                                if rewStim==rewardStim and blockInd > 0:
                                    y[-1].append(np.full(preTrials+postTrials+1,np.nan))
                                    pre = v[(obj.trialBlock==blockInd)]
                                    k = min(preTrials,pre.size)
                                    y[-1][-1][preTrials-k:preTrials] = pre[-k:]
                                    post = v[(obj.trialBlock==blockInd+1)]
                                    k = min(postTrials,post.size)
                                    y[-1][-1][preTrials+1:preTrials+1+k] = post[:k]
                        y[-1] = np.nanmean(y[-1],axis=0)
                    m = np.nanmean(y,axis=0)
                    s = np.nanstd(y,axis=0)/(len(y)**0.5)
                    ax.plot(x,m,color=clr,label=context)
                    ax.fill_between(x,m+s,m-s,color=clr,alpha=0.25)
                for side in ('right','top'):
                    ax.spines[side].set_visible(False)
                ax.tick_params(direction='out',top=False,right=False)
                ax.set_xticks(np.arange(-20,60,20))
                ax.set_yticks([0,0.5,1])
                ax.set_xlim([-preTrials-0.5,postTrials+0.5])
                ax.set_ylim([0,1.01])
                if i==len(fixedParamNames)-1:
                    ax.set_xlabel('Trials after block switch')
                if j==0:
                    ax.set_ylabel(ylbl)
                if fixedParam=='Full model':
                    title = fixedParam+', '+blockLabel
                else:
                    title = fixedParam+'='+str(fixedVal)
                ax.set_title(title)
                if var=='pContext' and i==0 and j==1:
                    ax.legend(bbox_to_anchor=(1,1))
        plt.tight_layout()

preTrials = 0
postTrials = 60
x = np.arange(-preTrials,postTrials+1)
for var,ylbl in zip(('pContext','wHabit'),('Context belief','Habit weight')):
    for trainingPhase in trainingPhases:
        d = modelData[trainingPhase]
        if len(d) == 0:
            continue
        fig = plt.figure(figsize=(10,10))
        gs = matplotlib.gridspec.GridSpec(len(fixedParamNames),2)
        for i,(fixedParam,fixedVal) in enumerate(zip(fixedParamNames,fixedParamValues)):
            for j,(rewardStim,blockLabel) in enumerate(zip(('vis1','sound1'),('visual rewarded blocks','sound rewarded blocks'))):
                ax = fig.add_subplot(gs[i,j])
                contexts,clrs = (('visual','auditory'),'gm') if var=='pContext' else ((None,),'k')
                for contextInd,(context,clr) in enumerate(zip(contexts,clrs)):
                    y = []
                    for mouse in d:
                        y.append([])
                        for session in d[mouse]:
                            obj = sessionData[trainingPhase][mouse][session]
                            v = d[mouse][session][modelType][var][fixedParamNames.index(fixedParam)]
                            if var=='pContext':
                                v = v[:,contextInd]
                            for blockInd,rewStim in enumerate(obj.blockStimRewarded):
                                if rewStim==rewardStim and blockInd == 0:
                                    y[-1].append(np.full(preTrials+postTrials+1,np.nan))
                                    pre = v[(obj.trialBlock==blockInd)]
                                    k = min(preTrials,pre.size)
                                    y[-1][-1][preTrials-k:preTrials] = pre[-k:]
                                    post = v[(obj.trialBlock==blockInd+1)]
                                    k = min(postTrials,post.size)
                                    y[-1][-1][preTrials+1:preTrials+1+k] = post[:k]
                        y[-1] = np.nanmean(y[-1],axis=0)
                    m = np.nanmean(y,axis=0)
                    s = np.nanstd(y,axis=0)/(len(y)**0.5)
                    ax.plot(x,m,color=clr,label=context)
                    ax.fill_between(x,m+s,m-s,color=clr,alpha=0.25)
                for side in ('right','top'):
                    ax.spines[side].set_visible(False)
                ax.tick_params(direction='out',top=False,right=False)
                ax.set_xticks(np.arange(-20,60,20))
                ax.set_yticks([0,0.5,1])
                ax.set_xlim([-preTrials-0.5,postTrials+0.5])
                ax.set_ylim([0,1.01])
                if i==len(fixedParamNames)-1:
                    ax.set_xlabel('Trials after block switch')
                if j==0:
                    ax.set_ylabel(ylbl)
                if fixedParam=='Full model':
                    title = fixedParam+', '+blockLabel
                else:
                    title = fixedParam+'='+str(fixedVal)
                ax.set_title(title)
                if var=='pContext' and i==0 and j==1:
                    ax.legend(bbox_to_anchor=(1,1))
        plt.tight_layout()
        
        
# plot q values
modelType = 'contextRL'
preTrials = 20
postTrials = 60
for trainingPhase in trainingPhases:
    d = modelData[trainingPhase]
    if len(d) == 0:
        continue
    for qval in ('qReinforcement',):
        fig = plt.figure(figsize=(10,10))
        gs = matplotlib.gridspec.GridSpec(len(fixedParamNames[modelType][:1]),2)
        for i,(fixedParam,fixedVal) in enumerate(zip(fixedParamNames[modelType][:1],fixedParamValues[modelType][:1])):
            for j,(rewardStim,blockLabel) in enumerate(zip(('vis1','sound1'),('visual rewarded blocks','sound rewarded blocks'))):
                ax = fig.add_subplot(gs[i,j])
                y = []
                for mouse in d:
                    y.append([])
                    for session in d[mouse]:
                        obj = sessionData[trainingPhase][mouse][session]
                        q = d[mouse][session][modelType][qval][fixedParamNames[modelType].index(fixedParam)]
                        if qval=='qContext':
                            q = q.reshape(obj.nTrials,8)
                        for blockInd,rewStim in enumerate(obj.blockStimRewarded):
                            if rewStim==rewardStim and blockInd > 0:
                                y[-1].append(np.full((q.shape[1],preTrials+postTrials),np.nan))
                                pre = q[(obj.trialBlock==blockInd)]
                                k = min(preTrials,len(pre))
                                y[-1][-1][:,preTrials-k:preTrials] = pre[-k:].T
                                post = q[(obj.trialBlock==blockInd+1)]
                                k = min(postTrials,len(post))
                                y[-1][-1][:,preTrials:preTrials+k] = post[:k].T
                    y[-1] = np.nanmean(y[-1],axis=0)
                m = np.nanmean(y,axis=0)
                im = ax.imshow(m,clim=(0,1),cmap='gray')
                for side in ('right','top'):
                    ax.spines[side].set_visible(False)
                ax.tick_params(direction='out',top=False,right=False)
                ax.set_xticks(np.arange(0,preTrials+postTrials,20))
                ax.set_xticklabels(np.arange(-20,postTrials,20))
                # ax.set_yticks([0,0.5,1])
                ax.set_xlim([-0.5,preTrials+postTrials+0.5])
                # ax.set_ylim([0,1.01])
                if i==len(fixedParamNames)-1:
                    ax.set_xlabel('Trials after block switch')
                if j==0:
                    ax.set_ylabel('state')
                if fixedParam=='Full model':
                    title = fixedParam+', '+blockLabel
                else:
                    title = fixedParam+'='+str(fixedVal)
                ax.set_title(title)
                if i==0 and j==1:
                    cb = plt.colorbar(im,ax=ax,fraction=0.05,pad=0.04,shrink=0.5)
                    cb.ax.tick_params(length=0)
                    cb.set_ticks([0,0.5,1])
        plt.tight_layout()
        

# time dependence of effect of prior reward or response
trainingPhase = 'after learning'
stimType = ('rewarded target','non-rewarded target','non-target (rewarded modality)','non-target (unrewarded modality)')
prevTrialTypes = ('response to rewarded target','response to non-rewarded target','response to either target')[:1]
d = modelData[trainingPhase]
for modelType in ('mice','contextRL','mixedAgentRL'):
    for fixedParam in ((None,) if modelType=='mice' else ('Full model','rewardBias','decayContext')):
        resp = {s: [] for s in stimType}
        trialsSince = {prevTrial: {s: [] for s in stimType} for prevTrial in prevTrialTypes}
        timeSince = copy.deepcopy(trialsSince)
        for mouse in d:
            for session in d[mouse]:
                obj = sessionData[trainingPhase][mouse][session]
                if modelType=='mice': 
                    r = obj.trialResponse
                else:
                    r = d[mouse][session][modelType]['simAction'][fixedParamNames[modelType].index(fixedParam)]
                for blockInd,rewStim in enumerate(obj.blockStimRewarded):
                    # if obj.hitRate[blockInd] < 0.85:
                    #     continue
                    otherModalTarget = np.setdiff1d(obj.blockStimRewarded,rewStim)[0]
                    blockTrials = (obj.trialBlock==blockInd+1) & ~obj.catchTrials & ~obj.autoRewardScheduled
                    rewTargetTrials = blockTrials & (obj.trialStim==rewStim)
                    nonRewTargetTrials = blockTrials & (obj.trialStim==otherModalTarget)
                    targetTrials = rewTargetTrials | nonRewTargetTrials
                    for s in stimType:
                        if s=='rewarded target':
                            stim = rewStim
                        elif s=='non-rewarded target':
                            stim = otherModalTarget
                        elif s=='non-target (rewarded modality)':
                            stim = rewStim[:-1]+'2'
                        else:
                            stim = otherModalTarget[:-1]+'2'
                        stimTrials = np.where(blockTrials & (obj.trialStim==stim))[0]
                        for prevTrialType,trials in zip(prevTrialTypes,(rewTargetTrials,nonRewTargetTrials,targetTrials)):
                            respTrials = np.where(trials & r)[0]
                            if len(respTrials) > 0:
                                prevRespTrial = respTrials[np.searchsorted(respTrials,stimTrials) - 1]
                                anyTargetTrials = np.array([np.any(np.in1d(obj.trialStim[p+1:s],(rewStim,otherModalTarget))) for s,p in zip(stimTrials,prevRespTrial)])
                                notValid = (stimTrials <= respTrials[0]) | (stimTrials > np.where(trials)[0][-1]) | anyTargetTrials
                                tr = stimTrials - prevRespTrial
                                tr[notValid] = -1
                                tm = obj.stimStartTimes[stimTrials] - obj.stimStartTimes[prevRespTrial]
                                tm[notValid] = np.nan
                                trialsSince[prevTrialType][s].extend(tr)
                                timeSince[prevTrialType][s].extend(tm)
                            else:
                                trialsSince[prevTrialType][s].extend(np.full(len(stimTrials),np.nan))
                                timeSince[prevTrialType][s].extend(np.full(len(stimTrials),np.nan))
                        resp[s].extend(r[stimTrials])
        
        for i,prevTrialType in enumerate(prevTrialTypes):
            for s in stimType:
                trialsSince[prevTrialType][s] = np.array(trialsSince[prevTrialType][s])
                timeSince[prevTrialType][s] = np.array(timeSince[prevTrialType][s])
                if i==0:
                    resp[s] = np.array(resp[s])

        # minTrials = 20
        # trialBins = np.arange(100)
        # for prevTrialType in prevTrialTypes:
        #     fig = plt.figure(figsize=(8,4.5))
        #     ax = fig.add_subplot(1,1,1)
        #     for s,clr,ls in zip(stimType,'gmgm',('-','-','--','--')):
        #         n = np.zeros(trialBins.size)
        #         p = np.zeros(trialBins.size)
        #         for i in trialBins:
        #             if i>0:
        #                 j = trialsSince[prevTrialType][s]==i
        #                 n[i] += j.sum()
        #                 p[i] += resp[s][j].sum()
        #         p /= n
        #         ci = np.array([[b/n[i] for b in scipy.stats.binom.interval(0.95,n[i],p[i])] for i in trialBins])
        #         ax.plot(trialBins,p,color=clr,ls=ls,label=s)
        #         ax.fill_between(trialBins,ci[:,0],ci[:,1],color=clr,alpha=0.25)
        #     for side in ('right','top'):
        #         ax.spines[side].set_visible(False)
        #     ax.tick_params(direction='out',top=False,right=False)
        #     #ax.set_xlim([0,np.where(n>minTrials)[0][-1]])
        #     ax.set_ylim([0,1.01])
        #     ax.set_xlabel('Non-target trials since last '+prevTrialType)
        #     ax.set_ylabel('Response rate')
        #     ax.set_title(modelType + ('' if fixedParam is None else ', ' + fixedParam))
        #     ax.legend(bbox_to_anchor=(1,1),loc='upper left')
        #     plt.tight_layout()
            
        y = {prevTrial: {} for prevTrial in prevTrialTypes}
        binWidth = 5
        timeBins = np.array([0,5,10,15,20,25,30,40,50,60,80,100])
        x = timeBins[:-1] + np.diff(timeBins)/2
        for prevTrialType in prevTrialTypes:    
            fig = plt.figure(figsize=(8,4.5))
            ax = fig.add_subplot(1,1,1)
            for s,clr,ls in zip(stimType,'gmgm',('-','-','--','--')):
                n = np.zeros(x.size)
                p = np.zeros(x.size)
                for i,t in enumerate(timeBins[:-1]):
                    j = (timeSince[prevTrialType][s] >= t) & (timeSince[prevTrialType][s] < timeBins[i+1])
                    n[i] += j.sum()
                    p[i] += resp[s][j].sum()
                p /= n
                ci = np.array([[b/n[i] for b in scipy.stats.binom.interval(0.95,n[i],p[i])] for i in range(x.size)])
                ax.plot(x,p,color=clr,ls=ls,label=s)
                ax.fill_between(x,ci[:,0],ci[:,1],color=clr,alpha=0.25)
                y[prevTrialType][s] = p
            for side in ('right','top'):
                ax.spines[side].set_visible(False)
            ax.tick_params(direction='out',top=False,right=False,labelsize=10)
            # ax.set_xlim([0,timeBins[np.where(n>minTrials)[0][-1]]+binWidth/2])
            # ax.set_xlim([0,52.5])
            # ax.set_ylim([0,1.01])
            ax.set_xlabel('Time since last '+prevTrialType+' (s)',fontsize=12)
            ax.set_ylabel('Response rate',fontsize=12)
            ax.set_title(modelType + ('' if fixedParam is None else ', ' + fixedParam))
            ax.legend(bbox_to_anchor=(1,1),loc='upper left',fontsize=10)
            plt.tight_layout()


# no reward blocks, target stimuli only
for modelType in modelTypes:
    fig = plt.figure(figsize=(8,10))
    gs = matplotlib.gridspec.GridSpec(len(fixedParamNames[modelType])+1,2)
    preTrials = 15
    postTrials = 15
    x = np.arange(-preTrials,postTrials+1)  
    for i,(fixedParam,fixedVal) in enumerate(zip(('mice',) + fixedParamNames[modelType],(None,)+fixedParamValues[modelType])):
        if fixedParam == 'mice':
            d = sessionData['no reward']
        else:
            d = modelData['no reward']
        if len(d) == 0:
            continue
        for j,(blockRewarded,title) in enumerate(zip((True,False),('switch to rewarded block','switch to unrewarded block'))):
            ax = fig.add_subplot(gs[i,j])
            ax.plot([0,0],[0,1],'--',color='0.5')
            for stimLbl,clr in zip(('previously rewarded target stim','other target stim'),'mg'):
                y = []
                for mouse in d:
                    y.append([])
                    for session in d[mouse]:
                        obj = sessionData['no reward'][mouse][session]
                        if fixedParam == 'mice':
                            resp = obj.trialResponse
                        else:
                            resp = d[mouse][session][modelType]['simulation'][fixedParamNames[modelType].index(fixedParam)]
                        for blockInd,rewStim in enumerate(obj.blockStimRewarded):
                            if blockInd > 0 and ((blockRewarded and rewStim != 'none') or (not blockRewarded and rewStim == 'none')):
                                if blockRewarded:
                                    stim = np.setdiff1d(('vis1','sound1'),rewStim) if 'previously' in stimLbl else rewStim
                                else:
                                    prevRewStim = obj.blockStimRewarded[blockInd-1]
                                    stim = np.setdiff1d(('vis1','sound1'),prevRewStim) if 'other' in stimLbl else prevRewStim
                                trials = (obj.trialStim==stim)
                                y[-1].append(np.full(preTrials+postTrials+1,np.nan))
                                pre = resp[(obj.trialBlock==blockInd) & trials]
                                k = min(preTrials,pre.size)
                                y[-1][-1][preTrials-k:preTrials] = pre[-k:]
                                post = resp[(obj.trialBlock==blockInd+1) & trials]
                                k = min(postTrials,post.size)
                                y[-1][-1][preTrials+1:preTrials+1+k] = post[:k]
                    y[-1] = np.nanmean(y[-1],axis=0)
                m = np.nanmean(y,axis=0)
                s = np.nanstd(y,axis=0)/(len(y)**0.5)
                ax.plot(x,m,color=clr,label=stimLbl)
                ax.fill_between(x,m+s,m-s,color=clr,alpha=0.25)
            for side in ('right','top'):
                ax.spines[side].set_visible(False)
            ax.tick_params(direction='out',top=False,right=False,labelsize=10)
            ax.set_xticks(np.arange(-20,21,5))
            ax.set_yticks([0,0.5,1])
            ax.set_xlim([-preTrials-0.5,postTrials+0.5])
            ax.set_ylim([0,1.01])
            ax.set_xlabel('Trials of indicated type after block switch',fontsize=12)
            ax.set_ylabel('Response rate',fontsize=12)
            # ax.legend(bbox_to_anchor=(1,1),loc='upper left')
            # ax.set_title(title+' ('+str(len(y))+' mice)',fontsize=12)
    plt.tight_layout()

for modelType in modelTypes:
    for var,ylbl in zip(('pContext','wHabit'),('Context belief','Habit weight')):
        fig = plt.figure(figsize=(10,10))
        gs = matplotlib.gridspec.GridSpec(len(fixedParamNames)+1,2)
        preTrials = 20
        postTrials = 60
        x = np.arange(-preTrials,postTrials+1)  
        for i,(fixedParam,fixedVal) in enumerate(zip(fixedParamNames,fixedParamValues)):
            d = modelData['no reward']
            if len(d) == 0:
                continue
            for j,(blockRewarded,blockLabel) in enumerate(zip((True,False),('switch to rewarded block','switch to unrewarded block'))):
                ax = fig.add_subplot(gs[i,j])
                ax.plot([0,0],[0,1],'--',color='0.5')
                contexts,clrs = (('visual','auditory'),'gm') if var=='pContext' else ((None,),'k')
                for contextInd,(context,clr) in enumerate(zip(contexts,clrs)):
                    y = []
                    for mouse in d:
                        y.append([])
                        for session in d[mouse]:
                            obj = sessionData['no reward'][mouse][session]
                            v = d[mouse][session][modelType][var][fixedParamNames.index(fixedParam)]
                            if var=='pContext':
                                v = v[:,contextInd]
                            for blockInd,rewStim in enumerate(obj.blockStimRewarded):
                                if blockInd > 0 and ((blockRewarded and rewStim != 'none') or (not blockRewarded and rewStim == 'none')):
                                    y[-1].append(np.full(preTrials+postTrials+1,np.nan))
                                    pre = v[obj.trialBlock==blockInd]
                                    k = min(preTrials,pre.size)
                                    y[-1][-1][preTrials-k:preTrials] = pre[-k:]
                                    post = v[obj.trialBlock==blockInd+1]
                                    k = min(postTrials,post.size)
                                    y[-1][-1][preTrials+1:preTrials+1+k] = post[:k]
                        y[-1] = np.nanmean(y[-1],axis=0)
                    m = np.nanmean(y,axis=0)
                    s = np.nanstd(y,axis=0)/(len(y)**0.5)
                    ax.plot(x,m,color=clr,label=context)
                    ax.fill_between(x,m+s,m-s,color=clr,alpha=0.25)
                for side in ('right','top'):
                    ax.spines[side].set_visible(False)
                ax.tick_params(direction='out',top=False,right=False,labelsize=10)
                ax.set_xticks(np.arange(-20,60,20))
                ax.set_yticks([0,0.5,1])
                ax.set_xlim([-preTrials-0.5,postTrials+0.5])
                ax.set_ylim([0,1.01])
                if i==len(fixedParamNames)-1:
                    ax.set_xlabel('Trials after block switch')
                if j==0:
                    ax.set_ylabel(ylbl)
                if fixedParam=='Full model':
                    title = fixedParam+', '+blockLabel
                else:
                    title = fixedParam+'='+str(fixedVal)
                ax.set_title(title)
                if var=='pContext' and i==0 and j==1:
                    ax.legend(bbox_to_anchor=(1,1))
        plt.tight_layout()



# cluster fit comparison of model and mice
for fixPrmInd,fixedParam in enumerate(fixedParamNames['contextRL']):
    for clustInd in range(nClusters): 
        fig = plt.figure(figsize=(8,10))
        fig.suptitle(('alphaStim=0' if 'alphaStim' in fixedParam else 'full model') + ', cluster ' + str(clustInd+1))
        gs = matplotlib.gridspec.GridSpec(len(modelTypes)+1,2)
        stimNames = ('vis1','vis2','sound1','sound2')
        postTrials = 15
        x = np.arange(postTrials)+1
        for i,modelType in enumerate(('mice',)+modelTypes):  
            d = modelData['clusters']
            for j,(rewardStim,blockLabel) in enumerate(zip(('vis1','sound1'),('visual rewarded blocks','sound rewarded blocks'))):
                ax = fig.add_subplot(gs[i,j])
                for stim,clr,ls in zip(stimNames,'ggmm',('-','--','-','--')):
                    y = []
                    for mouse in d:
                        for session in d[mouse]:
                            obj = sessionData[trainingPhase][mouse][session]
                            clustTrials = np.array(clustData['trialCluster'][mouse][session]) == clustInd + 1
                            if np.any(clustTrials):
                                if not np.any(np.isnan(d[mouse][session]['basicRL']['prediction'][fixPrmInd][clustInd])):
                                    if modelType == 'mice':
                                        resp = obj.trialResponse
                                    else:
                                        resp = d[mouse][session][modelType]['prediction'][fixPrmInd][clustInd]
                                    for blockInd,rewStim in enumerate(obj.blockStimRewarded):
                                        if rewStim==rewardStim:
                                            trials = clustTrials & (obj.trialBlock==blockInd+1) & (obj.trialStim==stim) & ~obj.autoRewardScheduled 
                                            if np.any(trials):
                                                y.append(np.full(postTrials,np.nan))
                                                post = resp[trials]
                                                k = min(postTrials,post.size)
                                                y[-1][:k] = post[:k]
                    m = np.nanmean(y,axis=0)
                    s = np.nanstd(y,axis=0)/(len(y)**0.5)
                    ax.plot(x,m,color=clr,ls=ls,label=stim)
                    ax.fill_between(x,m+s,m-s,color=clr,alpha=0.25)
                for side in ('right','top'):
                    ax.spines[side].set_visible(False)
                ax.tick_params(direction='out',top=False,right=False)
                ax.set_xticks(np.arange(-5,20,5))
                ax.set_yticks([0,0.5,1])
                ax.set_xlim([0.5,postTrials+0.5])
                ax.set_ylim([0,1.01])
                if i==len(modelTypes):
                    ax.set_xlabel('Trials after block switch cues')
                if j==0:
                    ax.set_ylabel(('Response rate' if modelType=='mice' else 'Prediction'))
                if modelType=='mice':
                    title = 'mice, ' if rewardStim=='vis1' else ''
                    title += blockLabel+' (n='+str(len(y))+')'
                else:
                    title = modelType
                ax.set_title(title)
                if i==0 and j==1:
                    ax.legend(loc='upper left',bbox_to_anchor=(1,1))
        plt.tight_layout()

  
# cluster fit log loss
for i,fixedParam in enumerate(fixedParamNames['contextRLmultiState']):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    for modelType,clr in zip(modelTypes,modelTypeColors):
        for j in range(nClusters):
            val = []
            for mouse in modelData['clusters'].values():
                for session in mouse.values():
                    val.extend(session[modelType]['logLossTest'][i][j])
            val = np.array(val)
            val[np.isinf(val)] = np.nan
            m = np.nanmean(val)
            s = np.nanstd(val)/(len(val)**0.5)
            ax.plot(j,m,'o',mec=clr,mfc='none',ms=10,mew=2,label=(modelType if j==0 else None))
            ax.plot([j,j],[m-s,m+s],color=clr,lw=2)
    for side in ('right','top'):
        ax.spines[side].set_visible(False)
    ax.tick_params(direction='out',top=False,right=False)
    ax.set_xticks(np.arange(nClusters))
    ax.set_xticklabels(np.arange(nClusters)+1)
    ax.set_xlim([-0.25,nClusters-0.25])
    ax.set_ylim([0.35,0.6])
    ax.set_xlabel('Cluster')
    ax.set_ylabel('Negative log-likelihood')
    ax.legend(loc='upper left',bbox_to_anchor=(1,1))
    plt.tight_layout()
    

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot([-1,nClusters+1],[0,0],'k--')
for modelType,clr in zip(modelTypes,modelTypeColors):
    for j in range(nClusters):
        val = []
        for mouse in modelData['clusters'].values():
            for session in mouse.values():
                val.extend([b-a for a,b in zip(session[modelType]['logLossTest'][0][j],session[modelType]['logLossTest'][1][j])])
        val = np.array(val)
        val[np.isinf(val)] = np.nan
        m = np.nanmean(val)
        s = np.nanstd(val)/(len(val)**0.5)
        ax.plot(j,m,'o',mec=clr,mfc='none',ms=10,mew=2,label=(modelType if j==0 else None))
        ax.plot([j,j],[m-s,m+s],color=clr,lw=2)
for side in ('right','top'):
    ax.spines[side].set_visible(False)
ax.tick_params(direction='out',top=False,right=False)
ax.set_xticks(np.arange(nClusters))
ax.set_xticklabels(np.arange(nClusters)+1)
ax.set_xlim([-0.25,nClusters-0.25])
ax.set_xlabel('Cluster')
ax.set_ylabel('$\Delta$ Negative log-likelihood')
ax.legend(loc='upper left',bbox_to_anchor=(1,1))
plt.tight_layout()


# cluster fit param values
for fixPrmInd,fixedParam in enumerate(fixedParamNames['contextRL']):
    fig = plt.figure(figsize=(14,11))
    gs = matplotlib.gridspec.GridSpec(len(modelTypes),len(paramNames[modelTypes[-1]]))
    for i,modelType in enumerate(modelTypes):
        for j,(param,xlim) in enumerate(zip(paramNames[modelType],paramBounds[modelType])):
            ax = fig.add_subplot(gs[i,j])
            for clustInd,clr in enumerate(clusterColors):
                if clustInd<3:
                    continue
                paramVals = []
                for mouse in modelData['clusters'].values():
                    for session in mouse.values():
                        vals = session[modelType]['params'][fixPrmInd][clustInd]
                        if not np.all(np.isnan(vals)):
                            paramVals.append(vals[j])
                if len(np.unique(paramVals)) > 1:
                    dsort = np.sort(paramVals)
                    cumProb = np.array([np.sum(dsort<=s)/dsort.size for s in dsort])
                    ax.plot(dsort,cumProb,color=clr,label='cluster '+str(clustInd+1))
                else:
                    ax.plot(paramVals[0],1,'o',mfc=clr,mec=clr)
            for side in ('right','top'):
                ax.spines[side].set_visible(False)
            ax.tick_params(direction='out',top=False,right=False)
            ax.set_xlim([xlim[0]-0.02,xlim[1]+0.02])
            ax.set_ylim([0,1.01])
            if j>0:
                ax.set_yticklabels([])
            if i<len(modelTypes)-1:
                ax.set_xticklabels([])
            else:
                ax.set_xlabel(param)
            if j==0 and i==len(modelTypes)//2:
                ax.set_ylabel('Cum. Prob.')
            if j==len(paramNames[modelTypes[-1]])//2:
                ax.set_title(modelType)
            if i==1 and j==len(paramNames[modelTypes[-1]])-1:
                ax.legend(loc='upper left',bbox_to_anchor=(1,1))
    plt.tight_layout()



