from datetime import datetime, timedelta
# generate random integer values
from numpy.random import seed, randint
import numpy as np
import time



start_date = datetime.now()
time_diff = timedelta(days=0,hours=1,minutes=0,seconds=0)
end_date = start_date + time_diff

tarDate = start_date
time_diff = timedelta(days=0,hours=0,minutes=0,seconds=1)
seed(1)

f = open('blah.csv','w+')
f.write('time,RBS,connRef,Transaction,connectedUsers\n')

rbsConnectedUsers = [1102,1324,888,919,432, 919, 879, 1010, 1001, 1024,
                     2310,1766,818,919,432, 911, 819, 1410]

connectionsToBeReleasedTime = {}

# sweep through every second
while tarDate < end_date:
    # sweep through a range of base stations
    for rbs in range(12, 30, 1):
        idx = rbs-12
        connAttempts = randint(4, 340)
        # each RBS will have a different number of successful connections at a given point in time
        for a in range(1, connAttempts,1):
            # generate internal random access identifier
            value = randint(12001, 65000)
            tDate = tarDate.strftime("%d/%m/%Y %H:%M:%S")
            # Add one more connection to the RBS
            #rbsConnectedUsers[rbs] += 1;
            rbsConnectedUsers[idx] += 1;

            writeStr = "%s, RBS100%d, %d, Initial Attach,%d\n" % (tDate, idx, value,rbsConnectedUsers[idx])
            print(writeStr)
            f.write(writeStr)

            #Generate when this connection is going to get released
            if randint(3,3000) % 9 == 0:
                tDiff2 = timedelta(days=0,hours=0,minutes=0,seconds=randint(2, 6))
                connTime = tarDate + tDiff2
                connTimeStr = connTime.strftime("%d/%m/%Y %H:%M:%S")
                idxStr = "%s_%d_%d" % (connTimeStr, a, idx)
                connectionsToBeReleasedTime[idxStr] = value
            else:
                tDiff2 = timedelta(days=0, hours=0, minutes=0, seconds=randint(8, 24))
                connTime = tarDate + tDiff2
                connTimeStr = connTime.strftime("%d/%m/%Y %H:%M:%S")
                idxStr = "%s_%d_%d" % (connTimeStr,a,idx)
                connectionsToBeReleasedTime[idxStr] = value


        # Release connections that are due for release in this time interval
        tDate = tarDate.strftime("%d/%m/%Y %H:%M:%S")
        print(tDate)
        for z in range(12, 30, 1):
            zz = z-12
            for y in range(4,340,1):
                searchIdxStr = "%s_%d_%d" % (tDate,y,z)
                if searchIdxStr in connectionsToBeReleasedTime:
                    val = connectionsToBeReleasedTime[searchIdxStr];
                    rbsConnectedUsers[idx] -= 1;
                    writeStr = "%s, RBS100%d, %d, Context Release,%d\n" % (tDate, idx, val, rbsConnectedUsers[idx] )
                    print (writeStr)
                    f.write(writeStr)
                    del connectionsToBeReleasedTime[searchIdxStr]

        tarDate = tarDate + time_diff

f.close()

