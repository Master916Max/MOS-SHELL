
# Colors (RGB tuples)
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
RED        = (255,   0,   0)
GREEN      = (  0, 255,   0)
BLUE       = (  0,   0, 255)
YELLOW     = (255, 255,   0)
CYAN       = (  0, 255, 255)
MAGENTA    = (255,   0, 255)
GRAY       = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
DARK_GRAY  = ( 64,  64,  64)
ORANGE     = (255, 165,   0)
PURPLE     = (128,   0, 128)
BROWN      = (165,  42,  42)
PINK       = (255, 192, 203)
NAVY       = (  0,   0, 128)
TEAL       = (  0, 128, 128)
OLIVE      = (128, 128,   0)
MAROON     = (128,   0,   0)
LIME       = (191, 255,   0)
GOLD       = (255, 215,   0)
SILVER     = (192, 192, 192)

# Window Message Types (Win32 style)
WM_PAINT        = 0x000F
WM_DESTROY      = 0x0002
WM_CLOSE        = 0x0010
WM_CREATE       = 0x0001
WM_QUIT         = 0x0012
WM_SIZE         = 0x0005
WM_MOVE         = 0x0003
WM_KEYDOWN      = 0x0100
WM_KEYUP        = 0x0101
WM_CHAR         = 0x0102
WM_MOUSEMOVE    = 0x0200
WM_LBUTTONDOWN  = 0x0201
WM_LBUTTONUP    = 0x0202
WM_RBUTTONDOWN  = 0x0204
WM_RBUTTONUP    = 0x0205
WM_MBUTTONDOWN  = 0x0207
WM_MBUTTONUP    = 0x0208
WM_MOUSEWHEEL   = 0x020A
WM_COMMAND      = 0x0111
WM_TIMER        = 0x0113
WM_HOTKEY       = 0x0312

# DefaultHandlers
def DefaultWMHandler(event,**kwargs): pass
