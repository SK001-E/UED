from configparser import ConfigParser
import os
import numpy as np
import pandas as pd
import skimage.draw
from tqdm import tqdm

HOME=r'C:/Users/sumit/Documents/GITHUB/UED'
PATH_peak=HOME+'/root/peakFiles'
PATH_avgData=HOME+'/data/Averaged_Intensity'

def timeDelayCalc(config_data):
    path=config_data['path']
    os.chdir(path)
    print(' Data directory is: '+os.getcwd())

    fileList=os.listdir(path)
    fileList=fileList[0:len(fileList)]

    timeDelayArray=np.zeros((len(fileList)),dtype=float)
    for i in tqdm(range(len(fileList)), desc=' Creating time stamps ...'):
        a1 = np.array(list(str.split(fileList[i],'.dat')[0]), dtype=int)[:-1]
        temp = (int(''.join(map(str,a1))))-200000
        temp=(61.95-temp/1000)/0.15
        timeDelayArray[i]=temp
    np.savetxt('../timeStamps.csv',timeDelayArray,delimiter=',')

def createArray(config_data):
    path=config_data['path']
    os.chdir(path)
    #print('Current Working directory is %s'%path)

    arrList=pd.read_csv('../timeStamps.csv',delimiter=',',header=None)
    arrList.rename({0:'Time Delay'}, axis=1, inplace=True)

    fileList=os.listdir(path)
    fileList=fileList[0:len(fileList)]
    greyVal01=np.array([])
    #greyVal02=np.array([])
    #greyVal03=np.array([])

    for j in range(len(fileList)):
        temp = np.loadtxt(fileList[j])
        #print('Loading completed on Folder %d, file %d of %d'%((i+1),(j+1),len(fileList)))
        y,x=int(config_data['peakxcoord']),int(config_data['peakycoord'])

        #create a rectangle, got coordinates from imageJ macros
        start01 = (x-20, y-20)
        extent01 = (40, 40)
        r01, c01 = skimage.draw.rectangle(start=start01, extent=extent01,shape=temp.shape)
        
        greyVal1 = np.mean([temp[r01,c01]])
        if greyVal01.size == 0:
            greyVal01=greyVal1
        else:
            greyVal01=np.append(greyVal01,greyVal1)   
    
    #*** Working on filtering and other parts of the script ****       
    #BKGAvg = np.mean([greyVal02,greyVal03],axis=0)            
    #print(greyVal01)
    
    BKGAvg=0        
    
    # *** Normalizing the intensity w.r.t intensity at t_0 and saving as a .csv file ***
    arrList['Peak%02d'%int(config_data['peaknumber'])]=greyVal01-BKGAvg
    df = arrList
    a = df.loc[df['Time Delay'] <= 0]
    average = a.mean()    
    df['Peak%02d'%int(config_data['peaknumber'])] = ((df['Peak%02d'%int(config_data['peaknumber'])])/average[1]) 
    df.to_csv('../timeSeries_%02d.csv'%int(config_data['peaknumber']),sep=',',index=None)
    
def createSingleArray(config_data):
    path=config_data['path'] 
    os.chdir(path)
    #print('Current Working directory is %s\n\n'%path)
    
    arrList=pd.read_csv('../timeSeries_01.csv',sep=',')
    for i in tqdm(range(1,int(config_data['peaknumber'])), desc= ' Working on merging time-series of all individual Bragg peaks ...'):
        filename='../timeSeries_%02d.csv'%(i+1)
        data=pd.read_csv(filename,sep=',')
        arrList['Peak%02d'%(i+1)]=data['Peak%02d'%(i+1)]

    arrList.to_csv('../timeSeries.csv',sep=',',index=None)

    for i in range(int(config_data['peaknumber'])):
        filename='../timeSeries_%02d.csv'%(i+1)
        os.remove(filename)
    print(' Saving Completed. Single time-series data generated')

config = ConfigParser()
config.read('./average_timeSeries_00.ini')
config_data=config["TOP_LEVEL"]
print(' DONE')

timeDelayCalc(config_data)

print(' Working Directory:'+config_data['path'])
print(' Approximate position of mechanical delay at t_0: '+config_data['initialtime'])
print(' Background Filtering:'+config_data['backgroundfilter'])
print(' Total number of Bragg peak in this dataset: '+config_data['foldermax'])


for i in tqdm(range(int(config_data['foldermax'])), desc=' Working on time-series of individual peaks ...'):
    config_data=config['Peak_%02d'%(i+1)]
    #print(config_data['peakycoord'])
    createArray(config_data)

createSingleArray(config_data)
