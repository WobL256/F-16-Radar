import pygame
import button

#define render dimensions
MOBILE_MODE = True

SCREEN_HEIGHT = 2048
SCREEN_WIDTH = 1024

WINDOW_HEIGHT = 1024
WINDOW_WIDTH = 512

def fill(surface, color):
#Fill all pixels of the surface with color, preserve transparency
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))

#color palette
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

#create display window
if MOBILE_MODE == False:
	screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
	win_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
else:
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('F-16 Radar Simulation')
clock = pygame.time.Clock()
WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_surface().get_size()

#load images
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
dfont = pygame.font.Font('mfdfont.ttf', 64)

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

#create button instances
#---screen buttons (non updating)
mode_button = button.Button(113, 0, button_img,1, 0, "CRM", WHITE, 0, -6)
scan_mode_button = button.Button(269, 0, button_img,1, 0, "RWS", WHITE, 0, -6)
exp_button = button.Button(440, 0, button_img,1, 0, "NORM", WHITE, 0, -6)
ovrd_button = button.Button(618, 0, button_img,1, 0, "OVRD", WHITE, 0, -6)
cntl_button = button.Button(791, 0, button_img,1, 0, "CNTL", WHITE, 0, -6)
range_up_btn = button.Button(0, 154, arrow_small_img, 0.3, 0)
range_down_btn = button.Button(-1, 310, arrow_small_img, 0.3, 180)
azimuth_btn = button.Button(0, 460, button_img, 0.9, 90)
elevation_btn = button.Button(0, 620, button_img, 0.9, 90)

#game loop
run = True
while run:
	
	#set framerate (30 best, 60 unstable)
	dt = clock.tick(30)
	
	#continuously get the window dimensions (windows)
	WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_surface().get_size()
	#print(WINDOW_HEIGHT, WINDOW_WIDTH)

	#background color
	screen.fill(BLACK)
	if MOBILE_MODE == False:
		win_screen.fill(BLACK)
	
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
			pygame.draw.line(screen, CYAN, (az_pos_left, 96), (az_pos_left, 928), width=5)
		if upd_left_az == True:
			pygame.draw.line(screen, CYAN, (az_pos_right, 96), (az_pos_right, 928), width=5)
	
	pygame.draw.rect(screen, WHITE, (0, 0, 1024, 1024), width=3) #frame
	pygame.draw.rect(screen, BLACK, (0, 230, 78, 80))
	
	screen.blit(sweep_img, (sweep_x - 16, 980))
	
	#--azimuth tape
	pygame.draw.line(screen, CYAN, (512, 930), (512,974), width=8)
	pygame.draw.line(screen, CYAN, (256, 940), (256,974), width=6)
	pygame.draw.line(screen, CYAN, (768, 940), (768,974), width=6)
	pygame.draw.line(screen, CYAN, (597, 940), (597,974), width=6)
	pygame.draw.line(screen, CYAN, (682, 940), (682,974), width=6)
	pygame.draw.line(screen, CYAN, (427, 940), (427,974), width=6)
	pygame.draw.line(screen, CYAN, (342, 940), (342,974), width=6)
	
	#--elevation tape
	pygame.draw.line(screen, CYAN, (80, 512), (124,512), width=8)
	pygame.draw.line(screen, CYAN, (80, 256), (114,256), width=6)
	pygame.draw.line(screen, CYAN, (80, 768), (114,768), width=6)
	pygame.draw.line(screen, CYAN, (80, 683), (114,683), width=6)
	pygame.draw.line(screen, CYAN, (80, 598), (114,598), width=6)
	pygame.draw.line(screen, CYAN, (80, 341), (114,341), width=6)
	pygame.draw.line(screen, CYAN, (80, 426), (114,426), width=6)
	
	#render things
	screen.blit(horizon_img, (256, 512-32))
	
	#screen buttons render/action
	if radar_range < 160:
		if range_up_btn.draw(screen):
			print("Range Up")
			radar_range = int(radar_range * 2)
	if radar_range > 5:
		if range_down_btn.draw(screen):
			print("Range Down")
			radar_range = int(radar_range / 2)
	if azimuth_btn.draw(screen):
		print("Azimuth Change")
		if az_var <= 3 and az_var != 1:
			az_var = az_var - 1
		elif az_var == 1:
			az_var = 3
	if elevation_btn.draw(screen):
		if bar_setting < 4:
			bar_setting = bar_setting * 2
		else:
			bar_setting = 1
	if mode_button.draw(screen):
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
	screen.blit(bar_img, (42, el_pos))
	
	#screen controls
	uparrow = button.Button(128, 1128, arrow_img, 0.5, 0, "slew", WHITE, 0, 128)
	rightarrow = button.Button(256, 1256, arrow_img, 0.5, 270)
	downarrow = button.Button(128, 1384, arrow_img, 0.5, 180)
	leftarrow = button.Button(0, 1256, arrow_img, 0.5, 90)
	elev_up_btn = button.Button(420, 1120, arrow_small_img, 0.5, 0)
	elev_down_btn = button.Button(420, 1400, arrow_small_img, 0.5, 180)
 	
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
			cursor.move(0, 2 * dt)
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
	range_text = dfont.render(str(radar_range), False, WHITE)
	screen.blit(range_text, (4, 230))
	azimuth_text = dfont.render('A', False, WHITE)
	azimuth_number = dfont.render(az_text, False, WHITE)
	screen.blit(azimuth_text, (4, 457))
	screen.blit(azimuth_number, (4, 503))
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
		win_screen.blit(pygame.transform.scale(screen, (WINDOW_HEIGHT/2, WINDOW_HEIGHT)), (0, 0))
	pygame.display.update()

pygame.quit()