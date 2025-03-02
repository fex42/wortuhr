from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)
from build123d import *
from math import *
from RoundCornerCase import RoundCornerCase
from Foot import Foot

mt = 0.001
tol = 0.2
front_th = 1.2 # thickness without diffusor
diffusor_th = 0.2 # diffusor thickness (first two layers of print in white)
back_th = front_th + diffusor_th # thickness of back
wall_th = 1.0 # wall thickness

grid_height = 10.0 # grid height

led_dx = 16.6  # x distance between LEDs on stripe
led_dy = 18.94 # Y distance between stripes

cnt_x = 11 # number of letters in a row
cnt_y = 10 # number of letter rows

# X/Y corner LED distance
corner_dx = 17
corner_dy = 19
cled_dx = led_dx * cnt_x + corner_dx
cled_dy = led_dy * cnt_y + corner_dy
cled_offset_x = 5 # X offset of corner led to middle (LED, not hole)
cled_offset_y = 3 # Y offset of corner led to middle (LED, not hole)

class LetterGenerator:
    """A generator for the letters that respect the order of GridLocations"""

    letters_fr = [
        "ILNESTODEUX",
        "QUATRETROIS",
        "NEUFUNESEPT",
        "HUITSIXCINQ",
        "MIDIXMINUIT",
        "ONZERHEURES",
        "MOINSOLEDIX",
        "ETRQUARTPMD",
        "VINGT-CINQU",
        "ETSDEMIEPAM"
    ]

    letters_de_alt = [
        "ESKISTLFÜNF",
        "ZEHNZWANZIG",
        "DREIVIERTEL",
        "NACHAPPYVOR",
        "HALBIRTHDAY",
        "DRZWÖLFÜNFX",
        "ZEHNEUNDREI",
        "ZWEINSIEBEN",
        "ELFVIERACHT",
        "SECHSIUHRYE"
    ]

    letters_de = [
        "ESKISTRFÜNF",
        "ZEHNZWANZIG",
        "DREIVIERTEL",
        "TGNACHVORUM",
        "HALBGZWÖLFJ",
        "ZWEINSIEBEN",
        "KDREIRHFÜNF",
        "ELFNEUNVIER",
        "NACHTZEHNBX",
        "USECHSFUHRY"
    ]

    letters_en = [
        "ITLISASAMPM",
        "ACQUARTERDC",
        "TWENTYFIVEX",
        "HALFSTENFTO",
        "PASTERUNINE",
        "ONESIXTHREE",
        "FOURFIVETWO",
        "EIGHTELEVEN",
        "SEVENTWELVE",
        "TENSEOCLOCK"
    ]

    letters = letters_de

    _x = cnt_x
    _y = 1

    def next_char(self):
        c = self.letters[self._y-1][self._x-1]
#        print(f"next_char(x = {self._x}, y={self._y}) -> {c}")
        self._y += 1
        if self._y > cnt_y:
            self._y = 1
            self._x -= 1
        if self._x <= 0:
            self._x = cnt_x
        return c

gen = LetterGenerator()

corner_led_dia = 4.5 # diameter of corner/minute LED hole

# magnets joining back and front
mag_dia = 8.3 # diameter of magnet hole
mag_dep = 3.8 # depth of magnet hole

led_stripe_w = 10.2
led_stripe_h = 2.0

# font parameters for letters
font_size = 14.5
font="FreeSans"
font_style = FontStyle.BOLD

mnut_dia = 4.6
mnut_height = 4.2
mnut_screw_dia = 4.0

mn_hole_dx = 50
nm_hole_dy = (cnt_y-2) * led_dy

border = 0 # border size (including tolerance for back)

box_x = cnt_x * led_dx + 2 * corner_dx + wall_th
box_y = cnt_y * led_dy + 2 * corner_dy + wall_th

# X/Y size over all
size_x = 2*border + box_x
size_y = 2*border + box_y

screw_box_size = mnut_dia + 4.2
mag_dx = box_x - 2 * wall_th - screw_box_size
mag_dy = box_y - 2 * wall_th - screw_box_size

##########################################################
# Front
##########################################################

def magnetLocations():
    return Locations(
        (-mag_dx/2 , 0),
        (+mag_dx/2 , 0),
        (-70.0, -mag_dy/2),
        (-70.0, +mag_dy/2),
        (+70, -mag_dy/2),
        (+70, +mag_dy/2)
    )


def frontPanel():
    front = Box(size_x, size_y, front_th + diffusor_th,
                align=(Align.CENTER, Align.CENTER, Align.MAX))
    txt_pl = Plane(front.faces().sort_by(Axis.Z).last)

    # Sunken letters and holes

    # Letters
    letter_sk = Sketch() + [
        txt_pl * loc * Text(gen.next_char(), font_size, font=font, font_style=font_style, rotation=180)
        for loc in GridLocations(led_dx, led_dy, cnt_x, cnt_y)
    ]
    front -= extrude(letter_sk, -front_th)

    # Holes for corner LEDs
    holes_sk = Sketch() + [
        txt_pl * loc * Circle(corner_led_dia/2)
        for loc in GridLocations(cled_dx, cled_dy, 2, 2)
    ]
    front -= extrude(letter_sk + holes_sk, -front_th)

    front = front.mirror(Plane.ZX)

    # boxes for letters
    lboxes_sk = Rectangle(wall_th + cnt_x * led_dx, wall_th + cnt_y * led_dy,
                            align=(Align.CENTER, Align.CENTER, Align.MIN)) - [
        loc * Rectangle(led_dx - wall_th, led_dy - wall_th)
        for loc in GridLocations(led_dx, led_dy, cnt_x, cnt_y)
    ]
    front += extrude(lboxes_sk, grid_height-1)

    # boxes for corner LEDs
    corner_led_locations = GridLocations(cled_dx, cled_dy, 2, 2)
    cboxes_sk = Sketch() + [
        loc * Rectangle(corner_dx + wall_th, corner_dy + wall_th) 
        - loc * Rectangle(corner_dx - wall_th, corner_dy - wall_th)
        for loc in corner_led_locations
    ]
    front += extrude(cboxes_sk, grid_height - 2)


    # outer box wall
    outer_wall_sk = Rectangle(box_x, box_y) - Rectangle(box_x - 2 * wall_th, box_y - 2 * wall_th)
    front += extrude(outer_wall_sk, grid_height + mag_dep + back_th + 2)


    mag_sk = Sketch() + [
        loc * Rectangle(screw_box_size, screw_box_size)
        for loc in magnetLocations()
    ]
    front += extrude(mag_sk, grid_height)

    top_grid_pl = Plane.XY.offset(grid_height)
    mag_sk = Sketch() + [
        top_grid_pl * loc * Circle(mnut_dia/2)
        for loc in magnetLocations()
    ]
    front -= extrude(mag_sk, -mnut_height)

    # headroom for soldering stripes
    solder_sk = Sketch() + [
        top_grid_pl * loc * Rectangle(wall_th + cnt_x * led_dx, led_stripe_w)
        for loc in GridLocations(cnt_x * led_dx, led_dy, 1, cnt_y)
    ]
    front -= extrude(solder_sk, -1.5)

    return front



###########################################################
## Back
###########################################################
def meltNutLocations():
    x_top = mn_hole_dx/2
    x_btn = mn_hole_dx*1.6

    return Locations(
        (-x_top, nm_hole_dy/2),
        (+x_top, nm_hole_dy/2),
        (-x_btn, -nm_hole_dy/2),
        (x_btn, -nm_hole_dy/2),
    )

def backside():
    back_x = box_x - 2 * wall_th - tol
    back_y = box_y - 2 * wall_th - tol

    # back plane
    back = Box(back_x, back_y, back_th, 
            align=(Align.CENTER, Align.CENTER, Align.MAX))

    # magnet connectors
    mag_sk = Sketch() + [
        loc * Rectangle(screw_box_size - tol, screw_box_size - tol)
        for loc in magnetLocations()
    ]
    back += extrude(mag_sk, mag_dep + 1)

    back -= Plane.XY.offset(-back_th) * magnetLocations() * CounterBoreHole(radius= mnut_screw_dia/2,
        counter_bore_radius = 3.1, counter_bore_depth=2,
        depth = back_th + mag_dep + 2).mirror(Plane.XY)

    # letter LED stripes
    base_sk = Rectangle(cnt_x * led_dx, cnt_y * led_dy)
    back += extrude(base_sk, mag_dep)

    plane = Plane.XY.offset(mag_dep)

    stripes_sk = Sketch() + [
        plane * loc * Rectangle(cnt_x * led_dx, led_stripe_w)
        for loc in GridLocations(led_dx, led_dy, 1, cnt_y)
    ]
    back -= extrude(stripes_sk, -led_stripe_h/4)

    # corner LEDs
    c1_loc = Location(Vector((cled_dx-cled_offset_x)/2, (cled_dy-cled_offset_y)/2))

    ang = 45

    c1_sk = c1_loc * Rectangle(led_dx,led_stripe_w + 2).rotate(Axis.Z, -ang)
    c1_sk += c1_sk.mirror(Plane.XZ)
    c1_sk += c1_sk.mirror(Plane.YZ)

    c1g_sk = Plane.XY.offset(mag_dep) * c1_loc * Rectangle(led_dx,led_stripe_w).rotate(Axis.Z, -ang)
    c1g_sk += c1g_sk.mirror(Plane.XZ)
    c1g_sk += c1g_sk.mirror(Plane.YZ)

    back += extrude(c1_sk, mag_dep)
    back -= extrude(c1g_sk, -led_stripe_h/4)

    # melting nut holes
    #mn_locs = GridLocations(mn_hole_dx, nm_hole_dy, 4, 2)
    mn_locs = meltNutLocations()

    mn_sk = Sketch() + [
        plane * loc * Circle(mnut_dia/2)
        for loc in mn_locs
    ] 
    back -= extrude(mn_sk, -mnut_height)
    mn_sk = Sketch() + [
        plane * loc * Circle(mnut_screw_dia/2)
        for loc in mn_locs
    ] 
    back -= extrude(mn_sk, -mnut_height*2)

    # cable holes
    ch_loc = GridLocations(24, mag_dy - 24, 1, 2)
    cab_sk = Sketch() + [
        loc * Rectangle(6,4)
        for loc in ch_loc
    ]
    back -= extrude(cab_sk, -10)
    return back

###########################################################
## Controller case base
###########################################################


case_height = 28.0

# case outer size
case_x = mn_hole_dx + 20
case_y = nm_hole_dy/2 + 24.645
case_wall_th = 1.6
case_radius = case_wall_th + screw_box_size/2

def caseBox():
    case = RoundCornerCase(case_x, 
                        case_y, 
                        case_height,
                        case_radius,
                        case_wall_th,
                        screw_hole_dia=mnut_dia,
                        screw_hole_dep=mnut_height
                        ).base().move(Pos(0, case_y/2))

    plane = Plane.XY.offset(mag_dep)

    # mount holes for case
    mn_sk = Sketch() + [
        plane * loc * Circle(mnut_screw_dia/2)
        for loc in meltNutLocations()
    ] 
    case -= extrude(mn_sk, -10)

    # hole for cable to LEDs
    cab_sk = Sketch() + [
        plane * loc * Rectangle(6,4)
        for loc in GridLocations(24, mag_dy - 24, 1, 2)
    ]
    case -= extrude(cab_sk, -10)

    # USB-C Slot for power
    power_sk = Plane.XZ * Pos(0, case_height/2) * (RectangleRounded(width=14, height=5.4, radius=1.4))
    case -= extrude(power_sk, -case_wall_th) 
    return case

def caseCover():
    return RoundCornerCase(case_x, 
                        case_y, 
                        case_height,
                        case_radius,
                        case_wall_th,
                        screw_hole_dia=mnut_dia,
                        screw_hole_dep=mnut_height
                        ).cover()


print(f"size_x = {size_x}") 
print(f"size_y = {size_y}")
print(f"box_x = {box_x}") 
print(f"box_y = {box_y}")
print(f"mn_hole_dx = {mn_hole_dx}")
print(f"nm_hole_dy = {nm_hole_dy}")
print(f"mn_nut_height = {(nm_hole_dy-size_y)/2}")

def diffusor(dx, dy):
    _box = Box(
        dx - 2*wall_th - tol, 
        dy - 2*wall_th - tol, 
        grid_height - 8
        )
    _ce = _box.edges().filter_by(Axis.Z)
    _box = fillet(_ce, radius=1.0)
    _tf = _box.faces().sort_by(Axis.Z).last
    return offset(_box, openings = _tf, amount=0.4)

showFront = True
showBack = True
showCase = True
showCover = True
showFoot = True
showDiffusor = True

nix = Box(tol,tol,tol)

if showFront:
    front = frontPanel()
else:
    front = nix

if showBack:
    back = backside()
else:
    back = nix

if showCase:
    case = caseBox()
else:
    case = nix
if showCover:
    cover = caseCover()
else:
    cover = nix

if showFoot:
    foot = Foot().foot()
else:
    foot = nix

if showDiffusor:
    diffusor1 = diffusor(led_dx, led_dy)
    diffusor2 = diffusor(corner_dx, corner_dy)
else:
    diffusor1 = nix
    diffusor2 = nix

show(
     front.move(Pos(size_x + 20, size_y + 20)),
     back.move(Pos(size_x + 20, 0)),
     case,
     cover.move(Pos(0, -case_y/2-10)),
     foot.move(Pos(0, case_y*2-20)),
     diffusor1.move(Pos(80, 0)),
     diffusor2.move(Pos(80, 30))
     )

def export(filename, object):
    export_step(object, f"{filename}.step")
    export_stl(object, f"{filename}.stl")

export("wortuhr-front", front)
export("wortuhr-back", back)
export("wortuhr-case-usbc2", case)
export("wortuhr-cover", cover)
export("wortuhr-foot_x2", foot)
export("letter-diffusor_x110", diffusor1)
export("letter-diffusor_x4", diffusor1)
