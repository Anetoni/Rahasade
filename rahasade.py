import pygame
from random import randint
 
class Robo():
    def __init__(self, png, korkeus, leveys):
        self.png = png
        self.korkeus = korkeus
        self.leveys = leveys
        self.x = 640/2
        self.y = 480 - self.korkeus
 
class Hirvio:
    def __init__(self, png, korkeus, leveys, x, y):
        self.png = png
        self.korkeus = korkeus
        self.leveys = leveys
        self.x = x
        self.y = y
 
class Kolikko:
    def __init__(self, png, korkeus, leveys, x, y):
        self.png = png
        self.korkeus = korkeus
        self.leveys = leveys
        self.x = x
        self.y = y
 
class Rahasade:
    def __init__(self):
        pygame.init()
 
        self.lataa_kuvat()
 
        self.nayton_korkeus = 480
        self.nayton_leveys = 640
        self.naytto = pygame.display.set_mode((self.nayton_leveys, self.nayton_korkeus))
 
        self.fontti = pygame.font.SysFont("Arial", 28)
 
        pygame.display.set_caption("Rahasade")
 
        self.robo = Robo(self.kuvat[2], self.kuvat[2].get_height(), self.kuvat[2].get_width())
        self.luo_hirviot()
        self.luo_kolikot()
 
        self.pisteet = 0
 
        self.oikealle = False
        self.vasemmalle = False
 
        self.silmukka()
    
    def silmukka(self):
        #pyörittää pelin kulkua
        self.kello = pygame.time.Clock()
        while True:
            self.tapahtumat()
            self.piirra_naytto()
 
            self.kello.tick(60)
    
    def piirra_naytto(self):
        #funktiota kutsutaan silmukassa, ja näyttöä päivitetään
        self.naytto.fill((255, 255, 255))
 
        teksti = self.fontti.render("Pisteet: " + str(self.pisteet), True, (255, 0, 0))
        self.naytto.blit(teksti, (self.nayton_leveys - 105, self.nayton_korkeus - 470))
        self.naytto.blit(self.robo.png, (self.robo.x, self.robo.y))
 
        self.piirra_kolikot()
        self.piirra_hirviot()
 
        pygame.display.flip()
    
    def piirra_kolikot(self):
        for coin in self.kolikot:
            self.naytto.blit(coin.png, (coin.x, coin.y))
            coin.y += 1
 
    def piirra_hirviot(self):
        for monster in self.hirviot:
            self.naytto.blit(monster.png, (monster.x, monster.y))
            monster.y += 1
    
    def lataa_kuvat(self):
        #lataa käytettävät kuvat
        self.kuvat = []
        for nimi in ["hirvio", "kolikko", "robo"]:
            self.kuvat.append(pygame.image.load(nimi + ".png"))
 
    def luo_hirviot(self):
        #Luo hirviöt, joita hyödynnetään pelin ajan
        self.hirviot = []
        png = self.kuvat[0]
        while len(self.hirviot) < 10:
            x = randint(0, self.nayton_leveys-png.get_width())
            y = -randint(100, 1000)
            hirvio = Hirvio(png, png.get_width(), png.get_height(), x, y)
            self.hirviot.append(hirvio)
    
    def luo_kolikot(self):
        #luo kolikot, joita hyödynnetään pelin ajan
        self.kolikot = []
        png = self.kuvat[1]
        while len(self.kolikot) < 10:
            x = randint(0, self.nayton_leveys-png.get_width())
            y = -randint(100, 1000)
            kolikko = Kolikko(png, png.get_width(), png.get_height(), x, y)
            self.kolikot.append(kolikko)
 
    def tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = True
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = True
 
            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = False
 
            if tapahtuma.type == pygame.QUIT:
                exit()
 
        self.liiku()
        self.tarkista_tormaykset()
    
    def liiku(self):
        #liikuttaa robottia nuolinäppäimen osoittamaan suuntaan
        if self.oikealle and self.robo.x < 640 - self.robo.leveys:
            self.robo.x += 4
        if self.vasemmalle and self.robo.x > 0:
            self.robo.x -= 4
    
    def tarkista_tormaykset(self):
        # Törmäyksien käsittely, funktio tarkistaa, onko robo osunut kolikkoon tai hirviöön aina kun robottia liikutetaan
        robo_keski = self.robo.x + self.robo.leveys/2
        self.kolikko_tormays(robo_keski)
        self.hirvio_tormays(robo_keski)
        
 
    def kolikko_tormays(self, robo_keski):
        #Kolikkojen törmäysten käsittely, jos osuu robottiin, saa pisteen, jos menee näytön ulkopuolelle, kolikko sijoitetaan uusiin koordinaatteihin
        for coin in self.kolikot:
            if coin.y + coin.korkeus >= self.nayton_korkeus:
                coin.x = randint(0, self.nayton_leveys-coin.leveys)
                coin.y = -randint(100, 1000)
 
            if coin.y + coin.korkeus >= self.robo.y:
                kolikko_keski = coin.x + coin.leveys/2
                if abs(robo_keski - kolikko_keski) <= (self.robo.leveys + coin.leveys)/2:
                    coin.x = randint(0, self.nayton_leveys-coin.leveys)
                    coin.y = -randint(100, 1000)
                    self.pisteet += 1
 
    def hirvio_tormays(self, robo_keski):
        #Hirviöiden törmäysten käsittely, jos osuu robottiin, peli loppuu. Jos menee näytön ulkopuolelle, hirviö sijoitetaan uusiin koordinaatteihin.
        for monster in self.hirviot:
            if monster.y + monster.korkeus >= self.nayton_korkeus:
                monster.x = randint(0, self.nayton_leveys-monster.leveys)
                monster.y = -randint(100, 1000)
            
            if monster.y + monster.korkeus >= self.robo.y:
                monster_keski = monster.x + monster.leveys / 2
                if abs(robo_keski - monster_keski) <= (self.robo.leveys + monster.leveys)/2:
                    self.game_over()
    
    def game_over(self):
        #Tulostaa GAME OVER näkymän
        while True:
            self.naytto.fill((255, 0, 0))
            teksti = self.fontti.render(f"Hirviö nappasi sinut! Sait {str(self.pisteet)} pistettä", True, (255, 255, 255))
            teksti2 = self.fontti.render("Paina ENTER-näppäintä yrittääksesi uudelleen", True, (255, 255, 255))
            text_rect = teksti.get_rect(center = self.naytto.get_rect().center)
 
            self.naytto.blit(teksti, text_rect)
            self.naytto.blit(teksti2, (self.nayton_leveys/2 - 225, self.nayton_korkeus/2 + 50))
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.__init__()
                
                if event.type == pygame.QUIT:
                    exit()
 
            pygame.display.flip()
 
if __name__ == "__main__":
    Rahasade()
