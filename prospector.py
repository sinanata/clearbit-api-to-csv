import clearbit
import pandas as pd
from pandas.io.json import json_normalize
import json
import time
import requests

clearbit.key = 'YOUR API KEY HERE'

def RateLimited(maxPerSecond):
    minInterval = 2.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rateLimitedFunction(*args,**kargs):
            elapsed = time.clock() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.clock()
            return ret
        return rateLimitedFunction
    return decorate

@RateLimited(1)  # 2 per 10 seconds at most
def PrintNumber(num):
    pass

if __name__ == "__main__":
    print ("Process started")
    
    with open('capterra-targeted.txt', 'r') as f:
        for i, line in enumerate(f, start=1):
            print('Processing line {} = domain {}'.format(i, line.strip()))
            
            try:
                response = clearbit.Prospector.search(domain=line)
                result_count = 0
                for person in response['results']:
                    result_count = result_count + 1
                    df = json_normalize(person)
                    df.to_csv('output.csv', mode='a', index=False, header=None, encoding='utf-8')
                PrintNumber(result_count)
                print('--> '+ str(result_count) +' prospects found')
                print('------------------------------------------------')
            except Exception:
                print('some error')
                pass 
