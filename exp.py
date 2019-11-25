import time
pros=[]
que =[]
file = open('./pros.txt').readlines()
for line in file:
    _list = line.replace('\n', '').split(' ')
    _pro = []
    for l in range(len(_list)):
        if _list[l].isalpha():
            _pro.append(_list[l])
        elif _list[l].isdigit():
            _pro.append(int(_list[l]))
    pros.append(_pro)

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

def HRRN(pros:list):
    pros_new = []
    for pro in pros:
        Rp = (pro[1] + pro[2]) / pro[2]
        pro[3] = Rp
        pros_new.append(pro)
    que = sorted(pros_new,key=lambda x: x[3])
    rt1,rt2 = caculate_rt(que)
    return que, rt1, rt2

if __name__ == '__main__':

    print(HRRN(pros))




