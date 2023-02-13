import pygame

pygame.font.init()
dfont = pygame.font.Font('font/mfdfont.ttf', 64)

#button class   button(x, y, image, scale, rot, text_in, color, xoff, yoff)
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
		self.text = dfont.render(self.text_in, True, color)
		self.text_rect = self.text.get_rect(center=(self.x +width/(2/scale) + xoff, self.y + height/(2/scale) + yoff))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))
		surface.blit(self.text, self.text_rect)

		return action