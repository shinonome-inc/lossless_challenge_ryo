import numpy as np 

def runlength_encode(data):
    out = []

    cnt = 1
    for i in range(1, len(data)):
        if data[i] == data[i-1]:
            cnt += 1
            continue
        
        out.append(data[i-1])

        if cnt != 1:
            out.append(data[i-1])
            out.append(cnt)
            cnt = 1
    
    if cnt == 1:
        out.append(data[-1])
    else:
        out.append(data[-1])
        out.append(data[-1])
        out.append(cnt)
    
    return out

def runlength_decode(data, size=28**2):
    out = []
    decode_flag = False
    continue_flag = False
    
    for i in range(0, len(data)-1):
        if continue_flag:
            continue_flag = False
            continue
            
        if decode_flag:
            out += [data[i]]*data[i+1]
            decode_flag = False
            continue_flag = True
            continue
            
        if data[i] == data[i+1]:
            decode_flag = True
        else:
            out.append(data[i])
            
    if len(out) != size:
        out.append(data[-1])
        
    return out
