#!/usr/bin/env python

import wx
import exp
import time
import threading


class Controller():
    def __init__(self,parent):
        # self.pros = []  # [[NAME,INTIME,RUNTIME,WEIGHT],]
        self.que = []
        self.rt1, self.rt2 = 0, 0
        self.algorithm = 1  # 默认FCFS
        self.parent = parent

    def addpro(self, pro: list):
        # pro 格式应为：[NAME,INTIME,RUNTIME,WEIGHT]
        lock = threading.Lock()
        lock.acquire()
        self.que.append(pro)
        lock.release()
        # print(self.que)
        self.deal()

    def pop(self,index:int):
        if self.que.__len__()!=0:
            lock = threading.Lock()
            lock.acquire()

            # self.pros.remove(self.que[index])
            self.que.pop(index)

            print('after pop',self.que)
            lock.release()

    def changeAlgorithm(self, i: int):
        if i == 1 or i == 2 or i == 3:
            self.algorithm = i

    def deal(self):
        # self.que = self.pros
        if self.algorithm == 1:
            self.que, self.rt1, self.rt2 = exp.FCFS(self.que)
        elif self.algorithm == 2:
            self.que, self.rt1, self.rt2 = exp.SJF(self.que)
        elif self.algorithm == 3:
            self.HRRN(self.que)



    def HRRN(self,que:list):
        pros_new = []
        for pro in que:
            waiting = self.parent.nowtime - pro[1]
            Rp = (waiting + pro[2]) / pro[2]
            pro[3] = Rp
            pros_new.append(pro)
        self.que = sorted(pros_new, key=lambda x: x[3])
        if len(self.que)!=0:
            self.rt1, self.rt2 = exp.caculate_rt(que)



class ProcessManagement(threading.Thread):

    def __init__(self, parent):
        super(ProcessManagement, self).__init__()  # 继承
        self.parent = parent
        self.setDaemon(True)  # 设置为守护线程， 即子线程是守护进程，主线程结束子线程也随之结束。

    def run(self):
        while 1:
            if self.parent.ctl.que != []:
                element = self.parent.ctl.que[0]
                self.parent.ctl.pop(0)
            else:
                element = None
            if element != None:
                lock = threading.Lock()
                lock.acquire()

                self.parent.output_text.AppendText(element[0]+'running----\n')
                time.sleep(element[2])
                self.parent.output_text.AppendText(element[0]+'end--------\n')
                print(self.parent.ctl.que)

                lock.release()

            if element == None:
                time.sleep(1)

class myFrame(wx.Frame):
    def __init__(self):

        # 界面渲染
        wx.Frame.__init__(self, None, -1, '模拟调度实验',size=(400, 400))
        panel = wx.Panel(self, -1)
        # 创建单选按钮
        radio1 = wx.RadioButton(panel, -1, "FCFS", pos=(20, 50), style=wx.RB_GROUP)
        radio2 = wx.RadioButton(panel, -1, "SJF", pos=(20, 80))
        radio3 = wx.RadioButton(panel, -1, "HRRN", pos=(20, 110))

        self.input_text = wx.TextCtrl(panel, -1, '', pos = (20, 150))
        self.output_text= wx.TextCtrl(panel, -1, '', pos = (20, 200),size = (340,150),style=wx.TE_MULTILINE|wx.TE_READONLY)
        for eachRadio in [radio1, radio2, radio3]:#绑定事件
            self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio, eachRadio)

        btn = wx.Button(panel,-1,'确定',pos = (170,148))
        self.Bind(wx.EVT_BUTTON,self.OnClick,btn)

        # 状态栏
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('当前经过时间: ')

        # 时间控制
        self.start_time = int(time.time())  # 秒级时间戳

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER,self.OnTimer,self.timer)
        self.timer.Start(1000)
        self.nowtime = 0

        # 初始化调度控制器
        self.ctl = Controller(self)

        self.name = '0'                 # 给作业起名


        # 线程
        self.progress = ProcessManagement(self)
        self.progress.start()



    def OnTimer(self,event):
        self.nowtime = int(time.time())-self.start_time
        self.statusbar.SetStatusText('当前经过时间: '+str(self.nowtime))
        # print(self.nowtime)
        if self.ctl.algorithm == 3:
            self.ctl.deal()




    def OnRadio(self, event):#事件处理器
        radioSelectd = event.GetEventObject()
        text = radioSelectd.GetLabel()
        if text == 'FCFS':
            self.ctl.changeAlgorithm(1)
        elif text == 'SJF':
            self.ctl.changeAlgorithm(2)
        elif text == 'HRRN':
            self.ctl.changeAlgorithm(3)
        self.output_text.AppendText('change mode into '+text+'\n')

    def OnClick(self,event):
        if self.input_text.GetLineText(0)=='':
            wx.MessageBox('请输入新进程运行时间，秒为单位，不能为空！')
        else:
            lock = threading.Lock()
            t = self.nowtime  # 入栈时间
            lock.acquire()

            self.name = ''+str(int(self.name)+1)
            runtime = int(self.input_text.GetLineText(0))
            self.ctl.addpro([self.name, t, runtime, 0])

            lock.release()
            self.input_text.Clear()
            self.output_text.AppendText('add process'+self.name+' intime:'+str(t)+' runtime:'+str(runtime)+'\n')

class myApp(wx.App):
    def OnInit(self):
        frame = myFrame()
        frame.Show()
        return True




if __name__ == '__main__':
    app = myApp()
    app.MainLoop()

