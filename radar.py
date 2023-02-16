import pygame
import configparser
import platform
import time

#load variables from config file
config = configparser.RawConfigParser()
config.read('settings.cfg')

#print all settings (debug)
for section in config.sections():
    print(section)
    for option in config.options(section):
        text = '{} {}'.format(option, config.get(section,option))
        print(text)

#set variables to values from config file
MOBILE_MODE = bool(config.get('MOBILE','MOBILE_MODE')=='True')
if platform.system()=='Linux':
	MOBILE_MODE = True
DEBUG_MODE = bool(config.get('DEBUG', 'DEBUG_MODE')=='True')

SCREEN_HEIGHT = int(config.get('RENDERING','SCREEN_HEIGHT'))
SCREEN_WIDTH = int(config.get('RENDERING','SCREEN_WIDTH'))

WINDOW_HEIGHT = int(config.get('RENDERING','WINDOW_HEIGHT'))
WINDOW_WIDTH = int(config.get('RENDERING','WINDOW_WIDTH'))

def fill(surface, color):
#Fill all pixels of the surface with color, preserve transparency
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))

#color palette

def colorPalette():
	global BLACK
	global WHITE
	global RED
	global ORANGE
	global YELLOW
	global GREEN
	global CYAN
	global DCYAN
	global BLUE
	global PURPLE
	global DEBUG
	BLACK = (0, 0, 0, 255)
	WHITE = (255, 255, 255, 255)
	RED = (255, 0, 0, 255)
	ORANGE = (255, 127, 0, 255)
	YELLOW = (255, 255, 0, 255)
	GREEN = (0, 255, 0, 255)
	CYAN = (0, 255, 255, 255)
	DCYAN = (0, 170, 230, 255)
	BLUE = (0, 0, 255, 255)
	PURPLE = (255, 0, 255, 255)
	DEBUG = (200, 10, 200, 255)
colorPalette()

#create display window
pygame.init()
if MOBILE_MODE == False:
	screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
	win_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
else:
	screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
	win_screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h))
pygame.display.set_caption('F-16 Radar Simulation')
clock = pygame.time.Clock()
WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_surface().get_size()


arrow_img = pygame.image.load('img/arrow.png').convert_alpha()
cursor_img = pygame.image.load('img/cursor.png').convert_alpha()
button_img = pygame.image.load('img/btn_tmp.png').convert_alpha()
button_s_img = pygame.image.load('img/btn_tmp_s.png').convert_alpha()
arrow_small_img = pygame.image.load('img/ArrowS.png').convert_alpha()
sweep_img = pygame.image.load('img/sweep.png').convert_alpha()
sweep_img = pygame.transform.rotozoom(sweep_img, 0, 0.5)
bar_img = pygame.transform.rotozoom(sweep_img, 270, 1)
horizon_img = pygame.image.load('img/horizon.png').convert_alpha()

#-modify loaded images
fill(sweep_img, CYAN)
fill(bar_img, CYAN)
fill(horizon_img, DCYAN)

#cursor data
bigcursor_img = pygame.transform.rotozoom(cursor_img, 0, 2)
cursor = bigcursor_img.get_rect()
cursor.center = (32, 32)
cursor.update(512-32, 512-32, 64, 64)

pygame.key.set_repeat(100, 100)

#text setup

pygame.font.init()
dfont = pygame.font.Font('font/mfdfont.ttf', 46)

#radar settings variables
azimuth = 30
az_text = 'AX'
az_var = 2
radar_range = 80
bar_setting = 4

#object information
#--azimuth lines
az_pos_left = 0
az_pos_right = 0
upd_left_az = True
upd_right_az = True
#--sweep and bar
sweep_x = 512
dir = 1 # 1=right, 2=left
el_cursor = 496
px_per_bar = 21
bar = 1
el_pos = 0

#Buttons setup
#Setup font
pygame.font.init()
bfont = pygame.font.Font('font/mfdfont.ttf', 46)

#Button class
class Button():
	def __init__(self, x, y, image, scale = 1, rot = 0, text_in = '', color = 'WHITE', xoff = 0, yoff = 0):
		self.xoff = xoff
		self.yof = yoff
		self.x = x
		self.y = y
		self.scale = scale
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.rotozoom(image, rot, scale)
		self.text_in = text_in
		self.text = bfont.render(self.text_in, True, color)
		self.text_rect = self.text.get_rect(center=(self.x +width/(2/scale) + xoff, self.y + height/(2/scale) + yoff))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		scale_y = win_screen.get_height() / SCREEN_HEIGHT
		scale_x = (win_screen.get_height() / 2) / SCREEN_WIDTH
		pos = pygame.mouse.get_pos()
		posf = (int(pos[0] / scale_x), int(pos[1] / scale_y))
		#print(posf)
		#check mouseover and clicked conditions
		if self.rect.collidepoint(posf):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))
		surface.blit(self.text, self.text_rect)

		return action

#create button instances
#---screen buttons (non updating)
mode_button = Button(113, 0, button_img,1, 0, "CRM", WHITE, 0, -6)
scan_mode_button = Button(269, 0, button_img,1, 0, "RWS", WHITE, 0, -6)
exp_button = Button(440, 0, button_img,1, 0, "NORM", WHITE, 0, -6)
ovrd_button = Button(618, 0, button_img,1, 0, "OVRD", WHITE, 0, -6)
cntl_button = Button(791, 0, button_img,1, 0, "CNTL", WHITE, 0, -6)
range_up_btn = Button(0, 154, arrow_small_img, 0.3, 0)
range_down_btn = Button(-1, 310, arrow_small_img, 0.3, 180)
azimuth_btn = Button(0, 460, button_img, 0.9, 90)
elevation_btn = Button(0, 620, button_img, 0.9, 90)

def FillScreen():
	if DEBUG_MODE == False:
		screen.fill(BLACK)
		if MOBILE_MODE == False:
			win_screen.fill(BLACK)
	else:
		screen.fill(DEBUG)
		if MOBILE_MODE == False:
			win_screen.fill(DEBUG)
def WindowDim():
	#continuously get the window dimensions (windows)
	WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_surface().get_size()


#MENUS and menu related variables
drawRange = True
drawAzimuth = True
drawBars = True
modeMenuOpen = False

def Modes_Menu():
    global crm_btn
    global acm_btn
    crm_btn = Button(0, 154,button_img, 0.8, 0, "CRM",WHITE, 0, -6)
    acm_btn = Button(-1, 310,button_img, 0.8, 0, "ACM",WHITE, 0, -6)
Modes_Menu()
def MenuHandler():
	global modeMenuOpen, drawRange, drawAzimuth, drawBars
	if modeMenuOpen == True:
		#disable some other buttons drawing
		drawRange = False
		drawAzimuth = False
		drawBars = False
		#draw the menu specific buttons
		if crm_btn.draw(screen):
			modeMenuOpen = False
			drawRange = True
			drawAzimuth = True
			drawBars = True
			
			print('CRM Selected')
		if acm_btn.draw(screen):
			modeMenuOpen = False
			drawRange = True
			drawAzimuth = True
			drawBars = True
			print('ACM Selected')
		
	

#game loop
run = True
while run:
	
	#set framerate and init game
	dt = clock.tick(60)
	WindowDim()
	FillScreen()

	#radar variable handling
	#--azimuth lines
	if az_var != 3:
		if upd_left_az == True:
			az_pos_left = cursor.x - azimuth * 7.8
		if upd_right_az == True:
			az_pos_right = cursor.x + azimuth * 7.8 + 63
		if az_pos_left <= 3:
			az_pos_left = 3
			upd_right_az = False
		else:
			upd_right_az = True
		if az_pos_right >= 1021:
			az_pos_right = 1021
			upd_left_az = False
		else:
			upd_left_az = True
		if az_pos_left <= 3 and az_pos_right >=1021:
			az_pos_left = 3
			az_pos_right = 1021
			upd_left_az = False
			upd_right_az = False
		
	#--azimuth button stuff
	az_values = {
		1: ('1', 10),
		2: ('3', 30),
		3: ('6', 60)
	}
	
	try:
		az_text, azimuth = az_values[az_var]
	except KeyError:
		az_text = 'ERROR'
		
	#--sweep stuff
	if az_var < 3:
		if sweep_x >= az_pos_right:
			sweep_x = az_pos_right
			dir = 2
			#elevate
			if(bar < bar_setting):
				bar = bar + 1
			elif(bar >= bar_setting):
				bar = 1
		elif sweep_x <= az_pos_left:
			sweep_x = az_pos_left
			dir = 1
			#elevate
			if(bar < bar_setting):
				bar = bar + 1
			elif(bar >= bar_setting):
				bar = 1
	else:
		if sweep_x >= 992:
			dir = 2
			#elevate
			if(bar < bar_setting):
				bar = bar + 1
			elif(bar >= bar_setting):
				bar = 1
		elif sweep_x <= 32:
			dir = 1
			#elevate
			if(bar < bar_setting):
				bar = bar + 1
			elif(bar >= bar_setting):
				bar = 1
			
	if dir == 1:
		sweep_x = sweep_x + (0.5 * dt)
	elif dir == 2:
		sweep_x = sweep_x - (0.5 * dt)
	
	#--elevation stuff
	el_pos = el_cursor + (bar * px_per_bar) - ((bar_setting * px_per_bar)/2) - 10
	
	#draw things
	#--az lines
	if(az_var != 3):
		if upd_right_az == True:
			pygame.draw.line(screen, CYAN, (az_pos_left, 96), (az_pos_left, 914), width=5)
		if upd_left_az == True:
			pygame.draw.line(screen, CYAN, (az_pos_right, 96), (az_pos_right, 914), width=5)
	
	pygame.draw.rect(screen, WHITE, (0, 0, 1024, 1024), width=3) #frame
	if drawRange:
		pygame.draw.rect(screen, BLACK, (0, 230, 78, 80))
	
	screen.blit(sweep_img, (sweep_x - 16, 950))
	
	#--azimuth tape
	pygame.draw.line(screen, CYAN, (512, 900), (512,944), width=8)
	pygame.draw.line(screen, CYAN, (256, 910), (256,944), width=6)
	pygame.draw.line(screen, CYAN, (768, 910), (768,944), width=6)
	pygame.draw.line(screen, CYAN, (597, 910), (597,944), width=6)
	pygame.draw.line(screen, CYAN, (682, 910), (682,944), width=6)
	pygame.draw.line(screen, CYAN, (427, 910), (427,944), width=6)
	pygame.draw.line(screen, CYAN, (342, 910), (342,944), width=6)
	
	#--elevation tape
	pygame.draw.line(screen, CYAN, (100, 512), (144,512), width=8)
	pygame.draw.line(screen, CYAN, (100, 256), (134,256), width=6)
	pygame.draw.line(screen, CYAN, (100, 768), (134,768), width=6)
	pygame.draw.line(screen, CYAN, (100, 683), (134,683), width=6)
	pygame.draw.line(screen, CYAN, (100, 598), (134,598), width=6)
	pygame.draw.line(screen, CYAN, (100, 341), (134,341), width=6)
	pygame.draw.line(screen, CYAN, (100, 426), (134,426), width=6)
	
	#render things
	screen.blit(horizon_img, (256, 512-32))
	#screen buttons render/action
	if drawRange:
		if radar_range < 160:
			if range_up_btn.draw(screen):
				print("Range Up")
				radar_range = int(radar_range * 2)
		if radar_range > 5:
			if range_down_btn.draw(screen):
				print("Range Down")
				radar_range = int(radar_range / 2)
	if drawAzimuth:
		if azimuth_btn.draw(screen):
			print("Azimuth Change")
			if az_var <= 3 and az_var != 1:
				az_var = az_var - 1
			elif az_var == 1:
				az_var = 3
	if drawBars:
		if elevation_btn.draw(screen):
			if bar_setting < 4:
				bar_setting = bar_setting * 2
			else:
				bar_setting = 1
	if mode_button.draw(screen):
		modeMenuOpen = True
		print("Mode Page Open")
	if scan_mode_button.draw(screen):
		print("Scan Mode Change")
	if exp_button.draw(screen):
		print("Exp Mode Change")
	if ovrd_button.draw(screen):
		print("Radar Override")
	if cntl_button.draw(screen):
		print("Control Page Open")
	
	#temp
	screen.blit(bar_img, (62, el_pos))

	#menus handling
	MenuHandler()
	
	#screen controls
	uparrow = Button(128, 1128, arrow_img, 0.5, 0, "SLEW", WHITE, 0, 128)
	rightarrow = Button(256, 1256, arrow_img, 0.5, 270)
	downarrow = Button(128, 1384, arrow_img, 0.5, 180)
	leftarrow = Button(0, 1256, arrow_img, 0.5, 90)
	elev_up_btn = Button(420, 1120, arrow_small_img, 0.5, 0)
	elev_down_btn = Button(420, 1400, arrow_small_img, 0.5, 180)
 	
	if uparrow.draw(screen):
		print('UP')
		if cursor.y >= 8:
			cursor.move_ip(0, -0.5 * dt)
	if downarrow.draw(screen):
		print('DOWN')
		if cursor.y <= 948:
			cursor.move_ip(0, 0.5 * dt)
	if leftarrow.draw(screen):
		print('LEFT')
		if cursor.x >= 9:
			cursor.move_ip(-0.5 * dt, 0)
	if rightarrow.draw(screen):
		print('RIGHT')
		if cursor.x <= 947:
			cursor.move_ip(0.5 * dt, 0)
			
	if elev_up_btn.draw(screen):
		print('Elevation Up')
		el_cursor = el_cursor - (0.4* dt)
	if elev_down_btn.draw(screen):
		print('Elevation Down')
		el_cursor = el_cursor + (0.4* dt)
	
	#keyboard controls
	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_w]:
		print('up')
		if cursor.y >= 1:
			cursor.move_ip(0, -2 * dt)
	if pressed[pygame.K_s]:
		print('down')
		if cursor.y <= 959:
			cursor.move_ip(0, 2 * dt)
	if pressed[pygame.K_a]:
		print('left')
		if cursor.x >= 4:
			cursor.move_ip(-2 * dt, 0)
	if pressed[pygame.K_d]:
		print('right')
		if cursor.x <= 956:
			cursor.move_ip(2 * dt, 0)
		
	#render cursor
	screen.blit(bigcursor_img, cursor)
	
	#draw text
	if drawRange:
		range_text = dfont.render(str(radar_range), False, WHITE)
		screen.blit(range_text, (4, 230))
	if drawAzimuth:
		azimuth_text = dfont.render('A', False, WHITE)
		azimuth_number = dfont.render(az_text, False, WHITE)
		screen.blit(azimuth_text, (4, 457))
		screen.blit(azimuth_number, (4, 503))
	if drawBars:
		elevation_text = dfont.render('B', False, WHITE)
		elevation_number = dfont.render(str(bar_setting), False, WHITE)
		screen.blit(elevation_number, (4, 618))
		screen.blit(elevation_text, (4, 662))

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False

	if MOBILE_MODE == False:
		win_screen.blit(pygame.transform.scale(screen, (win_screen.get_height()/2, win_screen.get_height())), (0, 0))
	else:
		win_screen.blit(pygame.transform.scale(screen, (win_screen.get_width(), win_screen.get_height())), (0,0))
		
	pygame.display.update()
		
pygame.quit()