import zipfile
import os
import datetime
import sys
import shutil

def sincronize(changes):
    if changes:
        with zipfile.ZipFile(os.path.join(sys.path[0], 'recive\ZipArquivo.zip'), 'r') as zip_ref:
            zip_ref.extractall(os.path.join(sys.path[0], 'FolderToSinc'))



RecivertimeList = []
for path,dirs,files in os.walk('FolderToSink'):
    for file in files:
        filename = os.path.join(path,file)
        relpath = os.path.relpath(filename,'FolderToSink')
        filesize = os.path.getsize(filename)
        # create a file path
        #print(relpath)
        # get creation time on windows

        try:
            # file modification timestamp of a file
            m_time = os.path.getmtime(path)
            # convert timestamp into DateTime object
            dt_m = datetime.datetime.fromtimestamp(m_time)     
            # file creation timestamp in float
            c_time = os.path.getctime(path)
            # convert creation timestamp into DateTime object
            dt_c = datetime.datetime.fromtimestamp(c_time)        

            RecivertimeList.append([str(relpath),str(dt_c),str(dt_m)])
        except:
            continue


senderTimeList = []
print(os.getcwd())
with open(os.path.join(sys.path[0], "SenderTime.txt"), "r") as arq:   
    data = arq.readlines()
    for i in data:
        aux = i.split(',')
        aux[2]=aux[2][:-1]
        senderTimeList.append(aux)

    print(senderTimeList)
    
changes = []
for dateSender in senderTimeList:
    flag = False
    for dateReciver in RecivertimeList:
        if dateSender[0] == dateReciver[0]:
            flag = True
            if datetime.datetime.strptime(dateSender[2], '%Y-%m-%d %H:%M:%S.%f') <= datetime.datetime.strptime(dateReciver[2], '%Y-%m-%d %H:%M:%S.%f'):
                changes.append(dateReciver[0])
    if not flag:
        changes.append(dateSender[0])


sincronize(changes)


