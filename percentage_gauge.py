import pygame
import pygame.gfxdraw
import math
import socket
import argparse

class Gauge:
    def __init__(self, screen, FONT, x_cord, y_cord, thickness, radius, circle_colour, glow=True):
        self.screen = screen
        self.Font = FONT
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.thickness = thickness
        self.radius = radius
        self.circle_colour = circle_colour
        self.glow = glow

    def draw(self, percent):
        fill_angle = int(percent*270/100)
        per=percent
        if percent > 100:
            percent = 100
        if per <=40:
            per=0
        if per > 100:
            per = 100
        ac = [int(255-per*255/100),int(per*255/100),int(0), 255]
        for indexi in range(len(ac)):
            if ac[indexi] < 0:
                ac[indexi] = 0
            if ac[indexi] > 255:
                ac[indexi] = 255
        # print(ac)

        pertext = self.Font.render(str(percent) + "%", True, ac)
        pertext_rect = pertext.get_rect(center=(int(self.x_cord), int(self.y_cord)))
        self.screen.blit(pertext, pertext_rect)

        for i in range(0, self.thickness):

            pygame.gfxdraw.arc(self.screen, int(self.x_cord), int(self.y_cord), self.radius - i, -225, 270 - 225, self.circle_colour)
            if percent >4:
                pygame.gfxdraw.arc(self.screen, int(self.x_cord), int(self.y_cord), self.radius - i, -225, fill_angle - 225-8, ac)

        if percent < 4:
            return

        if self.glow:
            for i in range(0,15):
                ac [3] = int(150 - i*10)
                pygame.gfxdraw.arc(self.screen, int(self.x_cord), int(self.y_cord), self.radius + i, -225, fill_angle - 225-8, ac)

            for i in range(0,15):
                ac [3] = int(150 - i*10)
                pygame.gfxdraw.arc(self.screen, int(self.x_cord), int(self.y_cord), self.radius -self.thickness - i, -225, fill_angle - 225-8, ac)

            angle_r = math.radians(fill_angle-225-8)
            lx,ly = int((self.radius-self.thickness/2)*math.cos(angle_r)), int( (self.radius-self.thickness/2)*math.sin(angle_r))
            ac[3] = 255
            lx = int(lx+self.x_cord)
            ly = int(ly + self.y_cord)

            pygame.draw.circle(self.screen,ac,(lx,ly),int(self.thickness/2),0)


            for i in range(0,10):
                ac [3] = int(150 - i*15)
                pygame.gfxdraw.arc(self.screen, int(lx), int(ly), (self.thickness//2)+i , fill_angle -225-10, fill_angle - 225-180-10, ac)

class GaugeHandler(Gauge):
	def __init__(self):	
		self.settings = {
			'background color' : (56, 56, 56),
			'circle color' : (55, 77, 91),
			'screen width' : 640,
			'screen height' : 480,
			'frame rate fps' : 100,
			'font type' : 'Franklin Gothic Heavy',
			'font size' : 100,
			'thickness' : 50,
			'radius' : 200,
			'glow' : False,
			'caption' : 'FMRI interactive gauge'
		}
		pygame.init()
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((self.settings['screen width'],self.settings['screen height']))
		pygame.display.set_caption(self.settings['caption'])
		FONT = pygame.font.SysFont(self.settings['font type'],self.settings['font size'])
		self.gauge = Gauge(screen=self.screen,FONT=FONT,x_cord=self.settings['screen width']/2,y_cord=self.settings['screen height']/2,
			thickness=self.settings['thickness'], radius=self.settings['radius'],circle_colour=self.settings['circle color'],glow=self.settings['glow'])
		self.set(percentage=0)
	def set(self,percentage):
		assert(0 <= percentage and percentage <= 100)
		self.percentage = percentage
		self.screen.fill(self.settings['background color'])
		self.gauge.draw(percent=self.percentage)
		pygame.display.update()
		self.clock.tick(self.settings['frame rate fps'])
		
	def clear(self):
		self.screen.fill(self.settings['background color'])
		pygame.display.update()
		self.clock.tick(self.settings['frame rate fps'])
class GaugeServer():
	def __init__(self,host,port):
		self.gauge = GaugeHandler()
		self.gauge.set(0)
		self.host = host
		self.port = port
		while True:
			self.next_int()
			
	def next_int(self):
		with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
			sock.bind((self.host,self.port))
			sock.listen()
			conn, addr = sock.accept()
			with conn:
				print("Connected by" + str(addr))
				while True:
					data = conn.recv(1024)
					if not data:
						break
					msg = data.decode()
					print(msg)
					self.gauge.set(int(msg))			

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--host', type=str, required=True)
	parser.add_argument('--port', type=int, required=True)
	args = parser.parse_args()
	server = GaugeServer(args.host,args.port)
	
        
