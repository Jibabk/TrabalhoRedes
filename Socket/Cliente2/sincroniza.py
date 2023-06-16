import zipfile
import os
import datetime
import sys

def main():

    def sincronize(changes):
        for change in changes:
            caminho = ''
            for letter in change:
                if letter == "\\":
                    letter = "/"
                caminho += letter
            with zipfile.ZipFile(os.path.join(sys.path[0], 'recive\ZipArquivo.zip'), 'r') as zip_ref:
                zip_ref.extract(caminho, os.path.join(sys.path[0], 'FolderToSinc'))




    RecivertimeList = []
    for path,dirs,files in os.walk(os.path.join(sys.path[0], 'FolderToSinc')):
        for file in files:
            filename = os.path.join(path,file)
            relpath = os.path.relpath(filename,os.path.join(sys.path[0], 'FolderToSinc'))
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

    #print(RecivertimeList)
    senderTimeList = []
    #print(os.getcwd())
    with open(os.path.join(sys.path[0], "SenderTime.txt"), "r") as arq:   
        data = arq.readlines()
        for i in data:
            aux = i.split(',')
            aux[2]=aux[2][:-1]
            senderTimeList.append(aux)

        #print(senderTimeList)
        
    #print('aaaaaaaaa')
    #print(senderTimeList[0][0])
    changes = []
    #print(RecivertimeList)
    #print(senderTimeList)
    #print('bbbbbbbbb')

    for dateSender in senderTimeList:
        flag = False
        for dateReciver in RecivertimeList:
            if dateSender[0] == dateReciver[0]:
                flag = True
                #print(f"dateSender:{dateSender[2]},DateReciver:{dateReciver[2]}")
                if datetime.datetime.strptime(dateSender[2], '%Y-%m-%d %H:%M:%S.%f') >= datetime.datetime.strptime(dateReciver[2], '%Y-%m-%d %H:%M:%S.%f'):
                    changes.append(dateReciver[0])
        if not flag:
            changes.append(dateSender[0])

    #for i in changes: print(i)

    sincronize(changes)

if __name__ == "__main__":
    main()


