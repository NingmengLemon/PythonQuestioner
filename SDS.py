import tkinter as tk
from tkinter import ttk,scrolledtext
from random import shuffle
import json

#JSON数据
jsonFile = open('./SDS.json','r',encoding='utf-8')
data = json.loads(jsonFile.read())
jsonFile.close()

#生成评价文本
def makeRes(stDict,n):
    res = ''
    comp = list(stDict.keys())
    for tmp in comp:
        obj = tmp.split(',')
        i = eval(obj[0])
        o = eval(obj[1])
        if n >= i and n <= o:
            res += stDict[tmp]+'; '
    return res

#在这里修改处理总分的方式，如果要高级操作就自己改代码
def compute(score):
    return int(score*1.25)

class Test(object):
    #初始化
    def __init__(self,data):
        #复制数据
        self.data = data
        #创建分数变量
        self.score = 0
        #生成询问顺序列表
        self.askOrd = list(range(0,len(data['objects'])))
        #乱序问题
        if self.data['random'] == True:
            shuffle(self.askOrd)
        #创建开始窗口
        self.startWindow = tk.Tk()
        self.startWindow.title(self.data['name'])
        self.startWindow.minsize(300,250)
        self.startWindow.resizable(height=False,width=False)
        #组件
        sctext = scrolledtext.ScrolledText(self.startWindow,wrap=tk.WORD)
        button_start = tk.Button(self.startWindow,text='开始',command=self.start)
        #插入数据到文本框
        sctext.insert('end',self.data['description'])
        #锁定文本框
        sctext['state'] = 'disabled'
        #布局
        sctext.pack()
        button_start.pack()
        #保持窗口
        self.startWindow.mainloop()
    
    def start(self):
        #摧毁开始窗口
        self.startWindow.destroy()
        #创建主窗口
        self.window = tk.Tk()
        self.window.title(self.data['name'])
        self.window.minsize(300,200)
        self.window.resizable(height=False,width=False)
        #组件
        self.sctext = scrolledtext.ScrolledText(self.window,wrap=tk.WORD,height=10)
        self.libo_choice = tk.Listbox(self.window,height=5)
        self.btn_choice = tk.Button(self.window,text='确定')
        self.frame_prgshower = tk.Frame(self.window)
        self.prgbar = ttk.Progressbar(self.frame_prgshower,orient='horizontal',length=400,mode='determinate',maximum=len(self.askOrd),value=0)
        self.label_prg = tk.Label(self.frame_prgshower,text='0/'+str(len(self.askOrd)))
        #布局
        self.sctext.pack()
        self.libo_choice.pack()
        self.btn_choice.pack()
        self.prgbar.pack(side='left')
        self.label_prg.pack(side='right')
        self.frame_prgshower.pack(side='bottom')
        #进入循环
        self.singleLoop(0)

    def singleLoop(self,index):
        #结束循环判断
        if index >= len(self.askOrd):
            self.end()
            return
        #更新问题数据
        self.sctext['state'] = 'normal'
        self.sctext.delete(1.0,'end')
        self.sctext.insert('end',self.data['objects'][index]['text'])
        self.sctext['state'] = 'disabled'
        #更新进度数据
        self.prgbar['value'] = index+1
        self.label_prg['text'] = f'{index+1}/{len(self.askOrd)}'
        #更新选项列表数据
        self.libo_choice.delete(0,'end')
        tmp = list(self.data['objects'][index]['choice'].keys())
        for c in tmp:
            self.libo_choice.insert('end',c)
        #更新下一题按钮的指令
        self.btn_choice['command'] = lambda x=index:self.clickNext(x)
        #继续保持窗口
        self.window.mainloop()

    def clickNext(self,index):
        #如果没有选择就不执行操作
        if self.libo_choice.curselection() == ():
            return
        #读取选项
        sel = self.libo_choice.curselection()[0]
        choice = self.data['objects'][index]['choice']
        #根据选项计分
        self.score += choice[list(choice.keys())[sel]]
        #下一轮循环
        self.singleLoop(index+1)

    def end(self):
        #摧毁主窗口
        self.window.destroy()
        #算分
        self.score = compute(self.score)
        #创建结束窗口
        endWindow = tk.Tk()
        endWindow.title(self.data['name'])
        endWindow.minsize(100,100)
        endWindow.resizable(height=False,width=False)
        #组件
        res = makeRes(self.data['results'],self.score)
        rlb = tk.Label(endWindow,text='评价: '+res)
        slb = tk.Label(endWindow,text='分数: '+str(self.score))
        endBtn = tk.Button(endWindow,text='确定',command=endWindow.destroy)
        #布局
        slb.pack()
        rlb.pack()
        endBtn.pack()
        #保持窗口
        endWindow.mainloop()
        
        
test = Test(data)
