def caculate_rt(pros:list):
    fulltime, eachtime = 0, []
    for pro in pros:
        fulltime += pro[2]
        eachtime.append(fulltime-pro[1])
    _time, _time2 = 0,0
    # 周转时间
    for e in eachtime:
        _time += e
    # 加权周转时间
    for i in range(len(eachtime)):
        eachtime[i] = eachtime[i]/pros[i][2]
        _time2 += eachtime[i]
    return _time/len(pros), _time2/len(pros)

def FCFS(pros:list):
    que = sorted(pros,key=lambda x: x[1])
    rt1, rt2 = caculate_rt(que)
    return que, rt1, rt2

def SJF(pros:list):
    que = sorted(pros,key= lambda x: x[2])
    rt1, rt2 = caculate_rt(que)
    return que, rt1, rt2

