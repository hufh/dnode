import json
import time

def runProcess():
    print "Doing some clever stuff"
    #time.sleep(10)

    with open('/mnt/state/job.json') as jobSpecFile, open('/mnt/state/output.txt', 'w') as output:    
        jobSpec = json.load(jobSpecFile)
        output.write(jobSpec["outputText"])

if __name__ == '__main__':
    runProcess()