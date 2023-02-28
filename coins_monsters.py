import pygame
from random import randint

class Peli:
    def __init__(self):
        pygame.init()

        self.peli_aktiivinen=True
        self.leveys=480 
        self.korkeus=800
        self.naytto=pygame.display.set_mode((self.leveys,self.korkeus))
        pygame.display.set_caption("Coins & Monsters")
        self.fontti=pygame.font.Font(None,50)
        

        self.robo=pygame.image.load("robo.png")
        self.robo_hahmo=self.robo.get_rect(midbottom=(self.leveys/2 ,self.korkeus))
        self.hirvio=pygame.image.load("hirvio.png")
        self.hirvio_rect=self.hirvio.get_rect(center=(randint(0,480-self.hirvio.get_width()),randint(-40,0)) )
        self.kolikko=pygame.image.load("kolikko.png")
        self.kolikko_rect=self.kolikko.get_rect()
        self.nopeus=5
        self.hirvio_nopeus=3
        self.kolikko_nopeus=3
        self.kolikko_rect.x=randint(0,480-self.kolikko_rect.width)
        self.kolikko_rect.y=randint(-40,0)
        self.vasemmalle=False
        self.oikealle=False
        self.pisteet=0
        self.laskin=0
        self.kello=pygame.time.Clock()
        self.hirvio_lista=[]
        self.ajastin= pygame.USEREVENT + 1
        pygame.time.set_timer(self.ajastin,900)
        self.silmukka()

    def pistetaulu(self):
        return self.fontti.render("Pisteet: "+ str(self.pisteet),False,(0, 230, 0))

    def piirra(self):
        self.naytto.fill((51, 102, 204))
        self.hirviot()
        self.naytto.blit(self.robo,self.robo_hahmo)        
        self.naytto.blit(self.kolikko,self.kolikko_rect)
        self.naytto.blit(self.pistetaulu(),((self.leveys-self.pistetaulu().get_width())/2, 0))
        pygame.display.flip()
    
    def tapahtumat(self):
        for tapahtuma in pygame.event.get():
                if tapahtuma.type==pygame.QUIT:
                    exit()
                if tapahtuma.type==self.ajastin:
                    self.hirvio_lista.append(self.hirvio.get_rect(center=(randint(0,480-self.hirvio.get_width()),randint(-40,0)) ))
        
        kb=pygame.key.get_pressed()
        if kb[pygame.K_LEFT] or kb[pygame.K_a]: 
            if self.robo_hahmo.x>0:
                self.robo_hahmo.x-=self.nopeus
        if kb[pygame.K_RIGHT] or kb[pygame.K_d]: 
            if self.robo_hahmo.x<self.leveys-self.robo_hahmo.width:
                self.robo_hahmo.x+=self.nopeus
        if kb[pygame.K_ESCAPE]:
            exit()
        if kb[pygame.K_F2]:
            Peli()
                    
    def hirviot(self):   
        if self.hirvio_lista:           
            for hirvio_rect in self.hirvio_lista:              
                hirvio_rect.y+=self.hirvio_nopeus
                self.naytto.blit(self.hirvio,hirvio_rect)

            self.hirvio_lista=[hirvio for hirvio in self.hirvio_lista if hirvio.y<self.korkeus+50 ]

    def kolikot(self):
        self.kolikko_rect.y+=self.kolikko_nopeus
        if self.kolikko_rect.y>self.korkeus:
            self.kolikko_rect.x=randint(0,480-self.kolikko_rect.width)
            self.kolikko_rect.y=randint(-40,0)

    def tormays(self):
        if self.hirvio_lista:           
            for hirvio_rect in self.hirvio_lista:                     
                if self.robo_hahmo.colliderect(hirvio_rect):
                    self.peli_aktiivinen=False
        if self.robo_hahmo.colliderect(self.kolikko_rect):
            self.kolikko_rect.x=randint(0,480-self.hirvio_rect.width)
            self.kolikko_rect.y=0
            self.pisteet+=1
            self.laskin+=1
            if self.laskin==5:
                self.laskin=0
                self.hirvio_nopeus+=2
                self.kolikko_nopeus+=2
            
    def silmukka(self):
        while True:
            if self.peli_aktiivinen:
                self.tapahtumat()
                
                self.kolikot()
                self.piirra()           
                self.tormays()
                
            else:
                self.naytto.fill((0, 0, 0))
                havisit_teksti=self.fontti.render(f"Pisteet: {self.pisteet} | Uusi peli F2",False,(230, 0, 0))
                self.naytto.blit(havisit_teksti,((50, (self.korkeus-havisit_teksti.get_height())/2)))
                pygame.display.flip()
                self.tapahtumat()
            self.kello.tick(60)

if __name__=="__main__":
    Peli()
    
