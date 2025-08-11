
import ProductKeys as pk
import File as F
import time
import pyperclip
import pygame

warnings = []  # List to store warnings
selected = 1
local_data = {"page":0}  # Dictionary to store local data
current_page = 1  # Global variable to track the current page
key = ""

controll = False

# for i in range(32):
#     k = pk.create_product_key()
#     print(pk.validate_product_key(k), k)

def setup():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Installer")
    screen = pygame.display.set_mode((800, 600))
    return screen

def run(screen):
    handel_events(screen)
    draw(screen)
    pygame.display.flip()

def handel_events(screen):
    global current_page, selected, local_data, key  # Use the global variable to track the current page
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                print("Left mouse button clicked at", event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if current_page == 2 and local_data["page"] == 1:
                   key =f"{key}{pyperclip.paste()}"
            elif event.key == pygame.K_RETURN:
                if current_page == 2:
                    handle_p2(screen, event)
                else:
                    current_page +=1
            elif event.key == pygame.K_BACKSPACE:
                if current_page > 1:
                    if current_page == 2:
                        handle_p2(screen, event)
                    else:
                        current_page -= 1
                else:
                    warnings.append(["Cannot go back, already on the first page.", time.time() + 5])
                    print("Already on the first page, cannot go back.")
            elif event.key == pygame.K_UP and current_page == 2:
                selected = max(1, selected - 1)
            elif event.key == pygame.K_DOWN and current_page == 2:
                selected = min(3, selected + 1)
            else:
                if current_page == 2 and local_data["page"] == 1:
                    handle_p2(screen, event)

def draw(screen):
    global current_page, warnings # This can be changed to switch between pages
    if current_page == 1:
        _draw_Page1(screen)
    elif current_page == 2:
        _draw_Page2(screen)
    elif current_page == 3:
        _draw_Page3(screen)
    elif current_page == 4:
        _draw_Page4(screen)
    elif current_page == 5:
        _draw_finish(screen)
    if current_page > 5:
        exit()  # Exit if the current page exceeds the last page
    
    for warning in warnings:
        font = pygame.font.Font(None, 24)
        text = font.render(warning[0], True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 20))
        pygame.draw.rect(screen, (255, 235, 235), text_rect.inflate(20, 10))  # Draw a background for the warning
        screen.blit(text, text_rect)  # Draw the warning text
        if time.time() > warning[1]:
            warnings.remove(warning)

def _draw_Page1(screen: pygame.Surface):
    screen.fill((235, 235, 255))  # Fill the screen with white
    font = pygame.font.Font(None, 36)
    textl1 = font.render("Step 1: Welcome to the Installer", True, (0, 0, 0))
    textl2 = font.render("Press Enter to continue", True, (0, 0, 0))
    text_rect = textl1.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2- textl1.get_height()+ 75))
    text_rect2 = textl2.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + textl2.get_height()+75))
    screen.blit(textl1, text_rect)  # Draw the page title
    screen.blit(textl2, text_rect2)  # Draw the instruction text
    # Drawing the Logo

    logo = pygame.Surface((200,200), pygame.SRCALPHA)
    pygame.draw.rect(logo, (255,0,0), (0,0, 100,100))
    pygame.draw.rect(logo, (255,255,0), (100,0, 100,100))
    pygame.draw.rect(logo, (0,0,255), (0,100, 100,100))
    pygame.draw.rect(logo, (0,255,255), (100,100, 100,100))
    d_logo = pygame.transform.rotate(logo,45)
    screen.blit(d_logo,(screen.get_width()//2-125,25))


    # Additional drawing logic for Page 1 can be added here

def _draw_Page2(screen):
    
    screen.fill((255, 255, 255))  # Fill the screen with white
    font = pygame.font.Font(None, 36)
    text = font.render("Step 2: Installation Options", True, (0, 0, 0))
    text_rect = text.get_rect(topleft=(screen.get_width() // 3,0))
    if local_data["page"] == 0:
        f1 = font.render("Feature 1: Basic Installation", True, (0, 0, 0))
        f2 = font.render("Feature 2: Advanced Installation", True, (0, 0, 0))
        f3 = font.render("Feature 3: Custom Installation", True, (0, 0, 0))
        f1_rect = f1.get_rect(topleft=(screen.get_width() // 2.5, 100))
        f2_rect = f2.get_rect(topleft=(screen.get_width() // 2.5, 150))
        f3_rect = f3.get_rect(topleft=(screen.get_width() // 2.5, 200))
        pygame.draw.rect(screen, (100, 100, 155) if selected == 1 else (200, 200, 255), f1_rect.inflate(10, 10))  # Draw a background for Feature 1
        pygame.draw.rect(screen, (100, 100, 155) if selected == 2 else (200, 200, 255), f2_rect.inflate(10, 10))  # Draw a background for Feature 2
        pygame.draw.rect(screen, (100, 100, 155) if selected == 3 else (200, 200, 255), f3_rect.inflate(10, 10))  # Draw a background for Feature 3
        screen.blit(f1, f1_rect)  # Draw Feature 1
        screen.blit(f2, f2_rect)  # Draw Feature 2
        screen.blit(f3, f3_rect)  # Draw Feature 3
    if local_data["page"] == 1:
        f1 = font.render("Please Enter your Product Key:", True, (0, 0, 0))
        f2 = font.render(key, True, (0, 0, 0))  # Display the entered product key
        f1_rect = f1.get_rect(topleft=(screen.get_width() // 2.5, 100))
        text_rect1 = f1.get_rect(topleft=(screen.get_width() // 2.5, 100)).move(0,f1_rect.height + 50)
        pygame.draw.rect(screen, (200, 200, 255), f1_rect.inflate(10, 10))  # Draw a background for Feature 1

        pygame.draw.rect(screen, (100, 100, 155), f1_rect.inflate(10, 10).move(0,f1_rect.height + 50))  # Highlight the selected feature

        screen.blit(f1, f1_rect)
        screen.blit(f2, text_rect1)  # Draw the entered product key

    screen.blit(text, text_rect)  # Draw the page title
    # Additional drawing logic for Page 2 can be added here
    _draw_left_side(screen, "select")  # Draw the left side of the screen

def handle_p2(screen, event: pygame.event.Event):
    global selected, current_page, key, local_data  # Use the global variable to track the current page

    if local_data["page"] == 1:
        if event.key == pygame.K_RETURN:
            if len(key) == 16 and pk.validate_product_key(key):
                local_data["page"] = 1
                current_page += 1
            else:
                warnings.append(["Invalid Product Key. Please enter a valid key.", time.time() + 5])
                print("Invalid Product Key. Please enter a valid key.")
            return
        if event.key == pygame.K_LEFT:
            local_data["page"] = 0
            return
        if event.unicode.isalnum() or event.unicode in "-_":
            key += event.unicode
        elif event.key == pygame.K_BACKSPACE:
            key = key[:-1]
    if local_data["page"] == 0 or local_data["page"] == 2:
        if event.key == pygame.K_BACKSPACE:
            current_page -= 1
            return
        
    if selected == 1 and local_data["page"] == 0:
        local_data["inst_type"] = "Basic Installation"
        local_data["page"] = 1
        
    elif selected == 2:
        local_data["inst_type"] = "Advanced Installation"
        local_data["page"] = 1

    elif selected == 3:
        local_data["inst_type"] = "Custom Installation"
        local_data["page"] = 1


def _draw_Page3(screen):
    
    screen.fill((255, 255, 255))  # Fill the screen with white
    font = pygame.font.Font(None, 36)
    text = font.render("Step 3: Copying Files", True, (0, 0, 0))
    text_rect = text.get_rect(topleft=(screen.get_width() // 3,0))
    screen.blit(text, text_rect)  # Draw the page title
    # Additional drawing logic for Page 2 can be added here
    _draw_left_side(screen, "copy")  # Draw the left side of the screen

def _draw_Page4(screen):
    
    screen.fill((255, 255, 255))  # Fill the screen with white
    font = pygame.font.Font(None, 36)
    text = font.render("Step 4: Setting Up the System", True, (0, 0, 0))
    text_rect = text.get_rect(topleft=(screen.get_width() // 3,0))
    screen.blit(text, text_rect)  # Draw the page title
    # Additional drawing logic for Page 2 can be added here
    _draw_left_side(screen, "setting")  # Draw the left side of the screen

def _draw_finish(screen):
    screen.fill((200, 255, 200))  # Fill the screen with light green
    font = pygame.font.Font(None, 36)
    textl1 = font.render("Installation Complete!", True, (0, 0, 0))
    textl2 = font.render("Press Enter to Close the Installer", True, (0, 0, 0))
    text_rect = textl1.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2- textl1.get_height()))
    text_rect2 = textl2.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + textl2.get_height()))
    screen.blit(textl1, text_rect)  # Draw the page title
    screen.blit(textl2, text_rect2)  # Draw the instruction text
    # Additional drawing logic for the finish page can be added here

def _draw_left_side(screen: pygame.Surface, state):
    font1 = pygame.font.Font(None,36)
    font = pygame.font.Font(None,34)
    if state == "select":
        left_side_rect = pygame.Rect(0, 0, screen.get_width() // 3, screen.get_height())
        pygame.draw.rect(screen, (57, 57, 114), left_side_rect)  # Fill the left side with light blue
        l1=font1.render("Sequence:", False,(0,0,0))
        l2=font.render("-Selecting Features",False,(0,0,0))
        l3=font.render("-Copying Files",False,(0,0,0))
        l4=font.render("-Setting Up the System",False,(0,0,0))
        l5=font.render("-Starting the System",False,(0,0,0))

        screen.blit(l1,(screen.get_width()//6 - l1.get_width()//2, 5))
        off = 5 + l1.get_height()
        screen.blit(l2,(5, 10+off))

        #pygame.draw.line(screen,(0,0,0),(5,10+off),(5+l2.get_width(),10+off))

        off += 10 + l2.get_height()
        pygame.draw.line(screen,(0,100,100),(5,off),(5+l2.get_width(),off), 5)
        screen.blit(l3,(5, 10+off))
        off += 10 + l2.get_height()
        screen.blit(l4,(5, 10+off))
        off += 10 + l2.get_height()
        screen.blit(l5,(5, 10+off))

    elif state == "copy":
        left_side_rect = pygame.Rect(0, 0, screen.get_width() // 3, screen.get_height())
        pygame.draw.rect(screen, (57, 114, 114), left_side_rect)
        l1=font1.render("Sequence:", False,(0,0,0))
        l2=font.render("-Selecting Features",False,(0,0,0))
        l3=font.render("-Copying Files",False,(0,0,0))
        l4=font.render("-Setting Up the System",False,(0,0,0))
        l5=font.render("-Starting the System",False,(0,0,0))

        screen.blit(l1,(screen.get_width()//6 - l1.get_width()//2, 5))
        off = 5 + l1.get_height()
        screen.blit(l2,(5, 10+off))
        off += 10 + l2.get_height()
        screen.blit(l3,(5, 10+off))
        off += 10 + l3.get_height()
        pygame.draw.line(screen,(0,100,100),(5,off),(5+l3.get_width(),off), 5)
        screen.blit(l4,(5, 10+off))
        off += 10 + l4.get_height()
        screen.blit(l5,(5, 10+off))
    elif state == "setting":
        left_side_rect = pygame.Rect(0, 0, screen.get_width() // 3, screen.get_height())
        pygame.draw.rect(screen, (57, 114, 57), left_side_rect)
        l1=font1.render("Sequence:", False,(0,0,0))
        l2=font.render("-Selecting Features",False,(0,0,0))
        l3=font.render("-Copying Files",False,(0,0,0))
        l4=font.render("-Setting Up the System",False,(0,0,0))
        l5=font.render("-Starting the System",False,(0,0,0))

        screen.blit(l1,(screen.get_width()//6 - l1.get_width()//2, 5))
        off = 5 + l1.get_height()
        screen.blit(l2,(5, 10+off))
        off += 10 + l2.get_height()
        screen.blit(l3,(5, 10+off))
        off += 10 + l3.get_height()
        screen.blit(l4,(5, 10+off))
        off += 10 + l4.get_height()
        pygame.draw.line(screen,(0,100,100),(5,off),(5+l4.get_width(),off), 5)
        screen.blit(l5,(5, 10+off))
    pass
    # Draw the left side of the screen with a specific color
      # Light blue color
    # Additional drawing logic for the left side can be added here

def main():
    screen = setup()
    while True:
        run(screen)

def install():
    """
    Main function to run the installer.
    This function initializes the pygame window and starts the event loop.
    """
    main()

if __name__ == "__main__":
    install()