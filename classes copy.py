import numpy as np

class Cell:
    def __init__(self, VEGETOP , ERBAST, CARVIZ, TYPE =1 ): #1 means ground and 0 is water
        self.VEGETOP = VEGETOP
        self.ERBAST = ERBAST
        self.CARVIZ = CARVIZ
        self.Type = TYPE
    
    def grow_vegetop(self):
        if self.Type == 1:
            self.VEGETOP = min(self.VEGETOP + 1,100)
        
    def grow_carviz(self):
        if self.CARVIZ:
            self.CARVIZ[2] = self.CARVIZ[2] + 1

            if self.CARVIZ[2] % 10 == 0: #eger yasi 10 un katsayisiysa 1 enerji eksilt
                self.CARVIZ[0] = self.CARVIZ[0] - 1

            if self.CARVIZ[2] == self.CARVIZ[3]  or self.CARVIZ[0] <= 0:
                neutarilaze(self.CARVIZ)

    def grow_erbast(self):
        if self.ERBAST:
            self.ERBAST[2] = self.ERBAST[2] + 1

            if self.ERBAST[2] % 10 == 0:  # eger yasi 10 un katsayisiysa 1 enerji eksilt
                self.ERBAST[0] = self.ERBAST[0] - 1

            if self.ERBAST[2] == self.ERBAST[3] or self.ERBAST[0] <= 0:
                neutarilaze(self.ERBAST)
            
    def eat(self):

           if (self.VEGETOP != None or self.VEGETOP != 0) and self.ERBAST != None:

                    self.VEGETOP =  max(self.VEGETOP - 2,0)
                    self.ERBAST[0] = min(self.ERBAST[0] + 1, 30) #yese bile enerjisi maksimum 30 olacak sekilde ayarladik
                    if self.ERBAST[2] == self.ERBAST[3] or self.ERBAST[0] <= 0:
                        neutarilaze(self.ERBAST)
    
            
 
            
    def fight(self):
        if self.ERBAST != None and self.CARVIZ != None:
            if self.ERBAST[0] > self.CARVIZ[0]: #savastiriyoruz. Enerjisi otculdan dusukse savasirken yakalayamadigindan enerji puani kaybediyor. Diger tarafta kactigi icin enerji kaybediyor. Ama yirtici daha cok enerji kaybediyor
                self.ERBAST[0] = self.ERBAST[0] - 2
                self.CARVIZ[0] = self.CARVIZ[0] - 5

                if self.CARVIZ[2] == self.CARVIZ[3] or self.CARVIZ[0] <= 0: # kacma olayi sirqasinda enerjileri 0 olursa yine olmeleerini kontrol ediyorum cunku diger turlu bir sonrakinde - oluyor kod calismiyor olmuyorlar amk
                    neutarilaze(self.CARVIZ)
                if self.ERBAST[2] == self.ERBAST[3] or self.ERBAST[0] <= 0:
                    neutarilaze(self.ERBAST)
               

            elif self.ERBAST[0] == self.CARVIZ[0]:
                return
            else:
                if np.random.random() >= 0.77: # bundan sonra sans faktoru ekliyoruz %33 ihtimalle kacarken ayagi takiliyor ve yem olma ihtimali oluyor erbastin. Eger oyle bir sey olursa direkt yiyor yirtici
                   self.CARVIZ[0] = min(self.CARVIZ[0] + self.ERBAST[0],40)  # otculun tum enerjisini carvize ver ve hayvani oldur
                   neutarilaze(self.ERBAST)
                self.CARVIZ[0] = self.CARVIZ[0] + self.ERBAST[0] # otculun tum enerjisini carvize ver ve hayvani oldur. maksimim 40 enerji ver
                neutarilaze(self.ERBAST)


            
            

    def __repr__(self):
        return f'VEGETOP : {self.VEGETOP} , ERBAST : {self.ERBAST},CARVIZ : {self.CARVIZ},satir sonu -- '
        

def neutarilaze(creature):
    for i in range(4):
        creature[i] = 0
    return creature


