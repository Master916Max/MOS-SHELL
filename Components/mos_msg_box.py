#class MsgBox:
#   def __init__(self,title, ContentL1,ContentL2,Buttons, Type, root = None, Logo = None):
#        self.title = title
#        self.line1 = ContentL1
#        self.line2 = ContentL2
#        self.calc_dims()
#        self.Buttons = Buttons
#        self.Type = Type
#        if root is None:
#            raise Exception("No Root Surface given")
#        self.x = root.get_width()  // 2 - self.width  // 2
#        self.y = root.get_height() // 2 - self.height // 2
#        if root:
#            self.screen = root
#        else: self.screen = screen
#        self.logo = Logo
#        if Type == 1:
#            self.ok = ButtonField("OK", self.screen, self.x + self.width // 2 - 75, self.y + self.height , 150, 50, fgcolor=textcolor, bgcolor=syscolor)
#            self.height += 50
#
#    def calc_dims(self):
#        img = menuf.render(self.line1, True, textcolor)
#        line2 = menuf.render(self.line2, True, textcolor)
#        title = menuf.render(self.title,True,textcolor)
#        if img.get_width() + 60 > line2.get_width() + 60:
#            self.width = img.get_width() + 80
#        else:
#            self.width = line2.get_width() + 80
#        if title.get_width() + 90 > self.width:
#            self.width = title.get_width() + 90
#        self.height = img.get_height() + 40 + 10 + line2.get_height()
#        self.line1_height = img.get_height()
#
#    def update_x_y(self,rel, mousepos):
#        if pygame.Rect(self.x + rel[0],self.y + rel[1],self.width,70).collidepoint(mousepos):
#            self.x = self.x + rel[0]
#            if self.x < 0:
#                self.x = 0
#            if self.x + self.width > screen.get_width():
#                self.x = screen.get_width() - self.width
#            self.y = self.y + rel[1]
#            if self.y < 0:
#                self.y = 0
#            return True
#        return False
#
#    def in_window(self,x,y):
#        return pygame.Rect(self.x,self.y,self.width,self.height).collidepoint(x,y)
#    
#    def handel_input(self, type : str, dat):
#        global data
#        if type == "m":
#            if pygame.Rect(self.x + 5,self.y+30 ,self.width- 10,self.height- 35).collidepoint(dat[0], dat[1]): pass
#                #if self.func:
#                    #self.func(type,dat)
#            elif pygame.Rect(self.x,self.y,self.width,30).collidepoint(dat[0], dat[1]):
#                if _colide_in_cy(self.x + 15 , self.y+ 15, 10, dat[0], dat[1]):
#                    zlayer.remove(self)
#                self.offsetx = (self.x - dat[0])
#                self.offsety = (self.y - dat[1])
#        
#    def draw(self, sreen: pygame.Surface = None):
#        # if ms.index(self) != selected_window:
#        #     pygame.draw.rect(self.screen, (175,175,175), pygame.Rect(self.x,self.y,self.width,self.height))
#        # else:
#        pygame.draw.rect(  self.screen, (0,0,0), pygame.Rect(self.x-1,self.y-1,self.width+2,self.height+2))        
#        pygame.draw.rect(  self.screen, syscolor, pygame.Rect(self.x,self.y,self.width,self.height))
#        pygame.draw.rect(  self.screen, (255,255,255), pygame.Rect(self.x + 5,self.y+30 ,self.width- 10,self.height- 35))
#        pygame.draw.circle(screen,(255,0,0), (self.x + 15 , self.y+ 15),10)
#        #pygame.draw.circle(screen,(0,255,0), (self.x + 40 , self.y+ 15),10)
#       # pygame.draw.circle(screen,(0,0,255), (self.x + 65 , self.y+ 15),10)
#        _draw_text(self.title, menuf, textcolor, self.x + 30, self.y + 2.5)
#        if self.Type == 1:
#            pygame.draw.circle(screen, (0,0,255),    (self.x + 40,self.y +(self.line1_height)//2 + 50), 25)
#            pygame.draw.circle(screen, (255,255,255),(self.x + 40,self.y +(self.line1_height)//2 + 50), 22)
#            pygame.draw.circle(screen, (0,0,255),    (self.x + 40,self.y +(self.line1_height)//2 + 50), 20)
#            pygame.draw.circle(screen, (255,255,255),(self.x + 40,self.y +(self.line1_height)//2 + 60), 3)
#            pygame.draw.line(  screen, (255,255,255),(self.x + 39,self.y +(self.line1_height)//2 + 37),(self.x + 39,self.y +(self.line1_height)//2 + 52), 4)
#        _draw_text(self.line1, menuf, msgtextcolor, self.x + 75, self.y + 35)
#        _draw_text(self.line2, menuf, msgtextcolor, self.x + 75, self.y + 35 + self.line1_height + 5)
#        self.ok.draw(x=self.x + self.width // 2 - 75, y=self.y + self.height - 60)
#        return 0
#
#def create_msg_box(titel, content_l1, content_l2, buttons, type, root = None):
#    msg = MsgBox(titel, content_l1, content_l2, buttons, type, root)
#    zlayer.insert(0,msg)
#    return 0 , msg