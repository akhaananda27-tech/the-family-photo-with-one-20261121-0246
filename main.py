#!/usr/bin/env python3
"""Family photo with one machine member — make.fun bounty.

Draws a single 1024x1024 photograph-style image of a family at home with
one machine member, using Pillow only (no network). The scene is a warm
living-room/kitchen at golden hour: a parent reading on the sofa, a child
leaning on them, a younger child playing on the rug, and a domestic robot
mid-task handing a mug toward the kitchen counter. Specific observed
details: a dog bowl, laundry on the radiator, a half-peeled carrot on the
counter, mismatched chairs. No text or lettering anywhere in the frame.
"""
import os
from PIL import Image, ImageDraw, ImageFilter

W = H = 1024

# --- palette (warm golden-hour domestic) ---
WALL = (245, 226, 199)
WALL_SH = (232, 205, 172)
FLOOR = (176, 128, 84)
FLOOR_DK = (150, 105, 66)
FLOOR_LT = (196, 150, 104)
WINDOW_SKY = (255, 196, 120)
WINDOW_SKY2 = (255, 150, 90)
RUG = (178, 84, 66)
RUG2 = (205, 120, 88)
SOFA = (74, 116, 110)
SOFA_DK = (56, 92, 87)
WOOD = (122, 82, 52)
WOOD_DK = (96, 62, 38)
CREAM = (248, 240, 222)
ROBOT = (238, 238, 234)
ROBOT_SH = (200, 202, 198)
SCREEN = (126, 200, 227)
SCREEN_DK = (70, 150, 185)

img = Image.new("RGB", (W, H), WALL)
d = ImageDraw.Draw(img, "RGBA")


def rrect(draw, box, r, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def ell(draw, box, fill=None, outline=None, width=1):
    draw.ellipse(box, fill=fill, outline=outline, width=width)


def poly(draw, pts, fill=None):
    draw.polygon(pts, fill=fill)


def shadow_layer(draw_fn, blur=18, alpha=90):
    """Draw draw_fn onto a transparent layer, blur it, composite as shadow."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    draw_fn(ld)
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    # darken: keep only alpha, recolor to black with given alpha
    black = Image.new("RGBA", (W, H), (60, 40, 20, alpha))
    mask = layer.split()[3]
    img.paste(black, (0, 0), mask)
    return


# ================= BACKGROUND =================
# wall (top 62%) and floor (bottom 38%)
d.rectangle([0, 0, W, 640], fill=WALL)
d.rectangle([0, 640, W, H], fill=FLOOR)
# floor boards
for y in range(660, H, 46):
    d.line([(0, y), (W, y)], fill=FLOOR_DK, width=3)
for x in range(0, W, 210):
    d.line([(x, 640), (x - 40, H)], fill=FLOOR_DK, width=2)
# baseboard
d.rectangle([0, 628, W, 646], fill=(226, 200, 168))
# soft warm light wash from window (left)
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([-220, 60, 620, 700], fill=(255, 200, 110, 70))
glow = glow.filter(ImageFilter.GaussianBlur(90))
img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img, "RGBA")

# ---- window (left) with evening sky + curtain ----
d.rectangle([70, 90, 330, 470], fill=(210, 180, 140))  # frame outer
d.rectangle([86, 106, 314, 454], fill=WINDOW_SKY)
d.rectangle([86, 106, 314, 300], fill=WINDOW_SKY2)
# sun low
ell(d, [120, 330, 210, 420], fill=(255, 230, 150))
# distant rooftops
poly(d, [(86, 454), (150, 380), (210, 454)], fill=(150, 90, 70))
poly(d, [(180, 454), (250, 360), (314, 454)], fill=(120, 70, 55))
# window crossbars
d.rectangle([196, 106, 204, 454], fill=(210, 180, 140))
d.rectangle([86, 280, 314, 288], fill=(210, 180, 140))
# curtain (right side of window, slightly drawn)
poly(d, [(300, 80), (360, 80), (350, 480), (300, 480)], fill=(196, 110, 96))
poly(d, [(300, 80), (360, 80), (350, 480), (300, 480)], fill=(0, 0, 0, 0))
d.line([(318, 90), (312, 470)], fill=(150, 70, 60), width=3)
d.line([(340, 90), (334, 470)], fill=(150, 70, 60), width=3)
# window sill
d.rectangle([60, 470, 360, 486], fill=(226, 200, 168))

# ---- radiator under window, laundry draped on it ----
d.rectangle([80, 500, 330, 600], fill=(228, 222, 210))
for x in range(95, 325, 22):
    d.rectangle([x, 508, x + 10, 592], fill=(205, 198, 186))
d.rectangle([80, 500, 330, 512], fill=(240, 234, 222))
# laundry: a striped towel + a small shirt draped over the radiator top
poly(d, [(120, 496), (190, 496), (196, 560), (116, 560)], fill=(140, 170, 200))
d.line([(128, 500), (126, 556)], fill=(110, 140, 175), width=4)
d.line([(150, 500), (150, 558)], fill=(110, 140, 175), width=4)
d.line([(172, 500), (174, 558)], fill=(110, 140, 175), width=4)
poly(d, [(215, 498), (275, 498), (280, 545), (212, 545)], fill=(226, 150, 140))
d.line([(230, 500), (228, 542)], fill=(190, 110, 100), width=3)
d.line([(255, 500), (256, 543)], fill=(190, 110, 100), width=3)

# ---- wall art: two small framed prints ----
rrect(d, [420, 110, 520, 210], 4, fill=(250, 244, 230), outline=(150, 110, 70), width=5)
poly(d, [(440, 190), (470, 140), (500, 190)], fill=(90, 130, 110))
ell(d, [482, 128, 500, 146], fill=(255, 200, 110))
rrect(d, [545, 110, 645, 210], 4, fill=(250, 244, 230), outline=(150, 110, 70), width=5)
ell(d, [575, 140, 615, 180], fill=(205, 120, 88))
d.line([(560, 195), (630, 195)], fill=(90, 130, 110), width=4)

# ---- kitchen counter (right) with half-peeled carrot ----
d.rectangle([700, 540, 1024, 640], fill=WOOD)
d.rectangle([700, 540, 1024, 556], fill=WOOD_DK)
d.rectangle([700, 556, 1024, 564], fill=(150, 105, 66))
# cutting board + half-peeled carrot
poly(d, [(760, 500), (900, 500), (910, 538), (750, 538)], fill=(220, 190, 140))
# carrot body (orange, half peeled showing pale core)
poly(d, [(790, 512), (880, 512), (884, 528), (786, 528)], fill=(232, 120, 50))
poly(d, [(790, 512), (830, 512), (832, 528), (786, 528)], fill=(245, 200, 130))  # peeled pale strip
poly(d, [(884, 512), (900, 518), (884, 528)], fill=(200, 90, 30))  # tip
d.line([(800, 508), (806, 500)], fill=(90, 140, 80), width=4)  # leafy top
d.line([(810, 508), (818, 498)], fill=(90, 140, 80), width=4)
# peelings
poly(d, [(840, 530), (858, 530), (852, 540), (838, 540)], fill=(245, 200, 130))
poly(d, [(860, 532), (876, 532), (872, 540), (858, 540)], fill=(232, 120, 50))
# mug + bowl on counter
rrect(d, [930, 490, 985, 538], 8, fill=(140, 170, 200))
d.rectangle([985, 502, 1000, 522], fill=(140, 170, 200))
ell(d, [740, 522, 780, 538], fill=(250, 244, 230))

# ---- floor lamp (right of sofa) ----
d.rectangle([655, 300, 665, 640], fill=(90, 70, 50))
poly(d, [(610, 300), (710, 300), (690, 220), (630, 220)], fill=(255, 210, 140))
ell(d, [630, 220, 690, 260], fill=(255, 230, 170))
# warm lamp glow
glow2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd2 = ImageDraw.Draw(glow2)
gd2.ellipse([560, 180, 760, 420], fill=(255, 200, 110, 55))
glow2 = glow2.filter(ImageFilter.GaussianBlur(70))
img.paste(Image.alpha_composite(img.convert("RGBA"), glow2).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img, "RGBA")

# ---- rug (center) ----
poly(d, [(300, 640), (760, 640), (820, 900), (240, 900)], fill=RUG)
poly(d, [(340, 680), (720, 680), (770, 860), (290, 860)], fill=RUG2)
d.line([(320, 660), (740, 660)], fill=(230, 160, 120), width=4)
d.line([(270, 880), (790, 880)], fill=(230, 160, 120), width=4)

# ---- sofa (left-center) ----
# shadow under sofa
shadow_layer(lambda ld: ld.rounded_rectangle([180, 620, 620, 700], radius=18, fill=(0, 0, 0, 255)), blur=16, alpha=70)
rrect(d, [190, 520, 620, 660], 22, fill=SOFA)
rrect(d, [190, 520, 620, 590], 22, fill=SOFA_DK)
rrect(d, [200, 540, 330, 650], 14, fill=(84, 126, 120))  # left cushion
rrect(d, [340, 540, 470, 650], 14, fill=(84, 126, 120))  # mid cushion
rrect(d, [480, 540, 610, 650], 14, fill=(84, 126, 120))  # right cushion
rrect(d, [180, 600, 210, 680], 10, fill=SOFA_DK)  # left arm
rrect(d, [600, 600, 630, 680], 10, fill=SOFA_DK)  # right arm
# throw pillow
poly(d, [(500, 560), (580, 545), (595, 620), (515, 630)], fill=(226, 150, 90))
# throw blanket over left arm
poly(d, [(185, 600), (250, 600), (245, 700), (180, 700)], fill=(240, 220, 180))
d.line([(200, 610), (198, 695)], fill=(200, 170, 120), width=3)
d.line([(220, 610), (220, 695)], fill=(200, 170, 120), width=3)

# ---- small side table + mismatched chairs (right) ----
# round side table near sofa right
ell(d, [660, 640, 790, 670], fill=WOOD)
d.rectangle([718, 668, 732, 780], fill=WOOD_DK)
ell(d, [690, 776, 760, 790], fill=WOOD_DK)
# book + cup on side table
poly(d, [(680, 622), (740, 622), (736, 640), (684, 640)], fill=(90, 120, 150))
d.line([(686, 631), (734, 631)], fill=(250, 244, 230), width=2)
ell(d, [752, 624, 776, 642], fill=(250, 244, 230))
# mismatched chairs: one wooden, one painted blue, at a small table (far right)
# wooden chair
d.rectangle([860, 560, 872, 660], fill=WOOD_DK)
d.rectangle([930, 560, 942, 660], fill=WOOD_DK)
d.rectangle([855, 640, 947, 660], fill=WOOD)
d.rectangle([855, 560, 947, 575], fill=WOOD)
# blue chair (different shape, slightly turned)
poly(d, [(960, 570), (972, 570), (968, 660), (956, 660)], fill=(70, 120, 160))
poly(d, [(1010, 570), (1022, 570), (1024, 660), (1012, 660)], fill=(70, 120, 160))
poly(d, [(955, 640), (1024, 640), (1024, 658), (955, 658)], fill=(90, 140, 180))

# ---- plant (left corner) ----
import math
# terracotta pot (trapezoid, wider at top)
poly(d, [(62, 620), (148, 620), (138, 700), (72, 700)], fill=(170, 90, 70))
d.rectangle([58, 612, 152, 624], fill=(190, 105, 80))
# fuller arching leaves
for ang, ln, wd in [(15, 150, 10), (40, 175, 11), (65, 160, 10), (90, 190, 12), (115, 165, 10), (140, 150, 10), (165, 130, 9)]:
    x0, y0 = 105, 618
    x1 = x0 + int(ln * 0.6 * math.cos(math.radians(ang - 90)))
    y1 = y0 - int(ln * math.sin(math.radians(ang - 90 + 25)))
    d.line([(x0, y0), (x1, y1)], fill=(70, 120, 70), width=wd)
    # leaf tip
    ell(d, [x1 - 7, y1 - 8, x1 + 7, y1 + 8], fill=(85, 140, 80))

# ================= PEOPLE (at ease, not posed) =================
# --- adult on sofa, reading (left-center) ---
# body: relaxed lean, book open
poly(d, [(250, 560), (330, 560), (345, 660), (240, 660)], fill=(120, 90, 140))  # torso (mauve sweater)
ell(d, [262, 470, 322, 540], fill=(232, 190, 160))  # head
# hair (dark, tied back)
ell(d, [258, 462, 326, 510], fill=(60, 45, 40))
poly(d, [(258, 490), (270, 530), (258, 540)], fill=(60, 45, 40))
# arm holding book
poly(d, [(250, 580), (300, 620), (290, 640), (245, 605)], fill=(120, 90, 140))
# open book
poly(d, [(295, 610), (335, 600), (330, 640), (300, 646)], fill=(250, 244, 230))
poly(d, [(335, 600), (368, 612), (362, 648), (330, 640)], fill=(240, 230, 210))
d.line([(300, 616), (328, 610)], fill=(150, 150, 150), width=2)
d.line([(340, 612), (362, 620)], fill=(150, 150, 150), width=2)
# legs stretched along sofa (jeans)
poly(d, [(330, 640), (470, 640), (480, 668), (340, 668)], fill=(70, 90, 130))
ell(d, [470, 640, 500, 668], fill=(250, 244, 230))  # sock

# --- child leaning on adult (middle) ---
ell(d, [360, 520, 410, 572], fill=(240, 200, 170))  # head
poly(d, [(360, 540), (372, 520), (400, 518), (412, 540), (400, 560), (372, 560)], fill=(90, 70, 50))  # curly hair
poly(d, [(368, 570), (410, 570), (420, 660), (360, 660)], fill=(230, 170, 90))  # yellow top, leaning
poly(d, [(368, 600), (340, 640), (352, 652), (375, 618)], fill=(230, 170, 90))  # arm down
# child legs tucked
poly(d, [(380, 650), (430, 650), (435, 672), (385, 672)], fill=(90, 110, 150))

# --- younger child on rug, playing with blocks (center floor) ---
# sitting cross-legged, back to viewer slightly turned
poly(d, [(430, 760), (500, 760), (515, 860), (420, 860)], fill=(200, 90, 80))  # red dress/top
ell(d, [448, 700, 498, 755], fill=(240, 200, 170))  # head
ell(d, [448, 695, 498, 735], fill=(70, 55, 45))  # hair cap
poly(d, [(448, 720), (438, 760), (452, 760)], fill=(70, 55, 45))  # pigtail left
poly(d, [(498, 720), (508, 760), (494, 760)], fill=(70, 55, 45))  # pigtail right
# arms reaching to blocks
poly(d, [(435, 780), (400, 830), (412, 842), (445, 800)], fill=(200, 90, 80))
poly(d, [(495, 780), (530, 830), (518, 842), (485, 800)], fill=(200, 90, 80))
# legs crossed
poly(d, [(425, 850), (470, 850), (480, 880), (430, 880)], fill=(120, 80, 120))
poly(d, [(470, 850), (515, 850), (510, 880), (465, 880)], fill=(120, 80, 120))
# toy blocks on rug
rrect(d, [380, 840, 410, 868], 3, fill=(90, 140, 180))
rrect(d, [540, 838, 572, 866], 3, fill=(230, 170, 90))
poly(d, [(400, 860), (430, 860), (415, 838)], fill=(120, 170, 110))
ell(d, [560, 860, 590, 878], fill=(200, 90, 80))  # ball

# ================= THE MACHINE MEMBER =================
# A domestic robot: rounded white body, soft blue screen face with calm eyes,
# one arm extended mid-task holding a mug toward the counter. Slightly worn,
# warm light on its left side. It stands by the kitchen counter, part of the room.
# shadow
shadow_layer(lambda ld: ld.ellipse([700, 820, 850, 852], fill=(0, 0, 0, 255)), blur=14, alpha=80)
# body (rounded, slightly tapered)
rrect(d, [716, 660, 838, 828], 48, fill=ROBOT)
rrect(d, [716, 660, 838, 745], 48, fill=(244, 244, 240))
# belly panel seam
d.line([(724, 758), (830, 758)], fill=(210, 212, 208), width=3)
# small chest light
ell(d, [766, 776, 788, 798], fill=(126, 200, 227))
ell(d, [771, 781, 783, 793], fill=(200, 235, 245))
# head (rounded screen)
rrect(d, [726, 560, 828, 668], 44, fill=ROBOT)
rrect(d, [736, 572, 818, 656], 36, fill=SCREEN)
# calm eyes (two soft arcs) + small smile
ell(d, [754, 596, 774, 618], fill=(40, 60, 80))
ell(d, [790, 596, 810, 618], fill=(40, 60, 80))
d.arc([762, 622, 802, 644], start=20, end=160, fill=(40, 60, 80), width=4)
# warm light on robot's left edge (from window)
d.line([(720, 590), (720, 650)], fill=(255, 210, 140), width=5)
d.line([(724, 672), (724, 800)], fill=(255, 210, 140), width=4)
# neck
d.rectangle([764, 656, 790, 672], fill=ROBOT_SH)
# right arm extended toward counter, holding a mug (mid-task)
poly(d, [(832, 700), (896, 676), (902, 696), (838, 720)], fill=ROBOT)
ell(d, [890, 668, 912, 696], fill=ROBOT_SH)  # hand
# mug in hand
rrect(d, [894, 640, 932, 678], 6, fill=(200, 90, 80))
d.rectangle([932, 652, 942, 668], fill=(200, 90, 80))
# steam curls from mug
d.arc([902, 618, 920, 640], start=180, end=360, fill=(255, 255, 255), width=3)
d.arc([908, 604, 926, 626], start=180, end=360, fill=(255, 255, 255), width=3)
# left arm resting at side, slightly bent
poly(d, [(720, 708), (692, 756), (704, 768), (728, 724)], fill=ROBOT)
ell(d, [690, 752, 712, 774], fill=ROBOT_SH)
# wheels / base (low, domestic)
rrect(d, [728, 826, 826, 846], 10, fill=(120, 122, 118))
ell(d, [740, 840, 762, 856], fill=(60, 62, 60))
ell(d, [792, 840, 814, 856], fill=(60, 62, 60))
# a small scuff on the body (it lives here, slightly worn)
d.line([(736, 790), (752, 795)], fill=(190, 192, 188), width=3)
d.line([(800, 710), (812, 715)], fill=(190, 192, 188), width=3)

# ================= SPECIFIC DETAILS =================
# dog bowl on the floor by the wall (left of sofa)
ell(d, [150, 700, 220, 724], fill=(90, 120, 160))
ell(d, [160, 704, 210, 718], fill=(200, 220, 235))
ell(d, [170, 708, 195, 716], fill=(150, 110, 80))  # kibble
# slippers by the sofa
poly(d, [(560, 690), (600, 690), (606, 706), (566, 706)], fill=(180, 120, 90))
poly(d, [(610, 694), (650, 694), (656, 710), (616, 710)], fill=(160, 100, 80))
# picture frames on the wall (family photos, small)
rrect(d, [700, 130, 780, 210], 4, fill=(250, 244, 230), outline=(150, 110, 70), width=5)
ell(d, [722, 150, 748, 178], fill=(232, 190, 160))
ell(d, [738, 150, 758, 172], fill=(200, 170, 140))
poly(d, [(718, 180), (762, 180), (766, 205), (714, 205)], fill=(120, 90, 140))
rrect(d, [800, 130, 880, 210], 4, fill=(250, 244, 230), outline=(150, 110, 70), width=5)
ell(d, [822, 152, 844, 174], fill=(240, 200, 170))
ell(d, [842, 156, 858, 174], fill=(232, 190, 160))
poly(d, [(820, 180), (862, 180), (866, 205), (816, 205)], fill=(90, 130, 110))
# cat asleep on the rug edge (another lived-in detail)
ell(d, [600, 850, 680, 884], fill=(200, 170, 130))
ell(d, [600, 850, 640, 878], fill=(200, 170, 130))
poly(d, [(606, 852), (616, 836), (624, 852)], fill=(200, 170, 130))
poly(d, [(626, 850), (636, 834), (644, 850)], fill=(200, 170, 130))
d.line([(660, 868), (672, 868)], fill=(150, 110, 80), width=3)

# ================= PHOTOGRAPHIC FINISH =================
# gentle vignette (darker corners, keeps the centre warm)
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse([-180, -180, W + 180, H + 180], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(160))
dark = Image.new("RGB", (W, H), (40, 25, 10))
img = Image.composite(img, dark, vig.point(lambda p: 255 - int((255 - p) * 0.45)))
# slight warm grade + soft grain for a photographic feel
img = img.point(lambda p: min(255, int(p * 1.02 + 3)))
import random
random.seed(21)
grain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grain)
for _ in range(2600):
    x = random.randint(0, W - 1)
    y = random.randint(0, H - 1)
    v = random.randint(0, 255)
    gd.point((x, y), fill=(v, v, v, 14))
img = Image.alpha_composite(img.convert("RGBA"), grain).convert("RGB")

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
out = os.path.join(out_dir, "entry.png")
img.save(out, "PNG", optimize=True)
print(f"wrote {out} {img.size} {os.path.getsize(out)} bytes")
