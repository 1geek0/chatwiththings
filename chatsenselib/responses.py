from chatsenselib.variables import *

def getAllScalarQuantities():
    mScalarQuantities = []
    for sensorType in mLangMapDB.all():
        mScalarQuantities.extend(sensorType['words'])
    return mScalarQuantities

def getAllLocations():
    mLocations = []
    for sensor in mSensorDB.all():
        mLocations.append(sensor['location'])
    return mLocations
