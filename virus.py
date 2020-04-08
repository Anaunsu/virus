import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

Day = 40
berth = 200
situation = 3

"""
1 不隔离  不戴口罩
2 不隔离  戴口罩
3 隔离    戴口罩
"""

class People(object):
    def __init__(self, count=5000, first_infected_num=1):
        self.count = count
        self.round = 1
        self.people = np.random.randint(-200, 200, size=(self.count, 2))
        self.status = np.zeros(self.count)
        self.time = np.zeros(self.count)
        self.init_state(first_infected_num, 1)

    @property
    def healthy(self):
        return self.people[self.status == 0]

    @property
    def infected(self):
        return self.people[self.status == 1]

    @property
    def confirmed(self):
        return self.people[self.status == 2]

    def init_state(self, num, state=1):
        now = 0
        while now < num:
            index = np.random.randint(0, self.count)
            if self.status[index] == state:
                continue
            else:
                self.status[index] = state
                self.time[index] = self.round
                now += 1

    def update(self):
        for i in range(self.count):
            x = np.random.randint(7,10)
            if self.status[i] == 1 and (self.round - self.time[i]) >= x:
                self.status[i] = 2
                self.time[i] = self.round
                if situation == 3:
                    if len(self.confirmed) < berth:
                        self.time[i] = -1
                        if(len(self.confirmed)<=100):
                            self.people[i][0] = -190 + 4 * len(self.confirmed)
                            self.people[i][1] = -220
                        else:
                            self.people[i][0] = -190 + 4 * (len(self.confirmed)-100)
                            self.people[i][1] = -240

    def infect_people(self,safe_distance=2.0):
        for infect in self.infected:
            temp = (self.people - infect) ** 2
            distance = temp.sum(axis=1) ** 0.5
            for i in distance.argsort():
                if distance[i] >= safe_distance / 2:
                    break
                if self.status[i] != 0:
                    continue
                x = np.random.randint(1,10)
                if x <= 4:
                    continue
                self.status[i] = 1
                self.time[i] = self.round
        if len(self.confirmed) > berth or situation != 3:
            for infect in self.confirmed:
                temp = (self.people - infect) ** 2
                distance = temp.sum(axis=1) ** 0.5
                for i in distance.argsort():
                    if distance[i] >= safe_distance:
                        break
                    if self.status[i] != 0:
                        continue
                    self.status[i] = 1
                    self.time[i] = self.round

    def move(self):
        movement = np.random.normal(0, 20, (self.count, 2))
        if situation==3:
            movement[self.time==-1]=0
        self.people = self.people + movement
        for i in range(self.count):
            if self.time[i] != -1:
                if self.people[i][1]<-200 or self.people[i][1] > 200:
                    self.people[i][1] = np.random.randint(-200,200)
                elif self.people[i][0] < -200 or self.people[i][0] > 200:
                    self.people[i][0] = np.random.randint(-200, 200)

    def display(self):
        p1 = plt.scatter(self.healthy[:, 0], self.healthy[:, 1], s=5)
        p2 = plt.scatter(self.infected[:, 0], self.infected[:, 1], s=5, c='yellow')
        p3 = plt.scatter(self.confirmed[:, 0], self.confirmed[:, 1], s=5, c='red')
        plt.plot([-250, 250], [-200, -200], linestyle='--', linewidth=2.5, color='red')
        plt.plot([-200, -200], [-200, 200], linestyle='--', linewidth=1.5, color='white')
        plt.plot([-200, 200], [200, 200], linestyle='--', linewidth=1.5, color='white')
        plt.plot([200, 200], [200, -200], linestyle='--', linewidth=1.5, color='white')
        plt.xlim(-250,250)
        plt.ylim(-250,250)
        plt.legend([p1, p2, p3], ['健康', '潜伏期', '感染'], loc='upper right', scatterpoints=1)
        message = "第 %s 天, 健康人数: %s, 潜伏期人数: %s, 确诊人数: %s" % \
            (self.round, len(self.healthy), len(self.infected), len(self.confirmed))
        plt.text(-200, 210, message, ha='left', wrap=True, color = "w",fontsize = 15)
        plt.text(-240, -230, '医院', ha='left', wrap=True, color="r", fontsize = 15)

def main():
    plt.figure(figsize=(10, 10))
    plt.style.use('dark_background')
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    p = People(1500, 1)
    plt.ion()
    for day in range(Day):
        for i in range(20):
            p.update()
            p.infect_people(safe_distance = 2 if situation >1 else 4)
            p.move()
            plt.cla()
            p.display()
            plt.pause(0.001)
        p.round += 1
    plt.ioff()

if __name__ == '__main__':
    main()