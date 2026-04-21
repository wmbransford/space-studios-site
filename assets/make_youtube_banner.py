from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 2560, 1440
SAFE_W, SAFE_H = 1546, 423
SAFE_X = (W - SAFE_W) // 2
SAFE_Y = (H - SAFE_H) // 2

INK = (5, 7, 11)
INK_UP = (10, 14, 22)
ACCENT = (110, 231, 255)
ACCENT_SOFT = (168, 240, 255)
TEXT = (231, 234, 240)
TEXT_DIM = (231, 234, 240, 160)

FONTS = "/tmp/banner-fonts"
F_INTER_R = f"{FONTS}/inter/extras/otf/Inter-Regular.otf"
F_INTER_SB = f"{FONTS}/inter/extras/otf/Inter-SemiBold.otf"
F_SERIF = f"{FONTS}/InstrumentSerif-Regular.ttf"
F_SERIF_I = f"{FONTS}/InstrumentSerif-Italic.ttf"

img = Image.new("RGB", (W, H), INK)
draw = ImageDraw.Draw(img)

# Subtle vertical lift toward top (matches site's radial-glow-from-top)
for y in range(H):
    t = 1 - (y / H) * 0.8
    r = int(INK[0] + (INK_UP[0] - INK[0]) * t * 0.3)
    g = int(INK[1] + (INK_UP[1] - INK[1]) * t * 0.3)
    b = int(INK[2] + (INK_UP[2] - INK[2]) * t * 0.3)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Grid (56px, white at ~4% opacity) — site's .bg-grid
grid_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grid_layer)
for x in range(0, W, 56):
    gd.line([(x, 0), (x, H)], fill=(255, 255, 255, 10))
for y in range(0, H, 56):
    gd.line([(0, y), (W, y)], fill=(255, 255, 255, 10))
img = Image.alpha_composite(img.convert("RGBA"), grid_layer)

# Radial cyan glow from top-center (matches hero)
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
glow_cx, glow_cy = W // 2, -200
for r in range(1600, 0, -20):
    a = int(24 * (r / 1600) ** 0.5)
    gd.ellipse(
        [glow_cx - r, glow_cy - int(r * 0.75), glow_cx + r, glow_cy + int(r * 0.75)],
        fill=(110, 231, 255, max(0, 28 - r // 80)),
    )
glow = glow.filter(ImageFilter.GaussianBlur(radius=60))
img = Image.alpha_composite(img, glow)

draw = ImageDraw.Draw(img)

# Typography
tag_font = ImageFont.truetype(F_INTER_SB, 28)
headline_font = ImageFont.truetype(F_SERIF, 140)
headline_it_font = ImageFont.truetype(F_SERIF_I, 140)
pillar_font = ImageFont.truetype(F_INTER_R, 30)
cadence_font = ImageFont.truetype(F_INTER_R, 26)

# ── Tag pill ("● AI & automation studio") — top-left of safe zone
tag_x = SAFE_X
tag_y = SAFE_Y - 10
tag_text = "AI & automation studio"
bbox = draw.textbbox((0, 0), tag_text, font=tag_font)
tag_w = bbox[2] - bbox[0]
tag_h = bbox[3] - bbox[1]
pad_x, pad_y = 22, 12
dot_r = 6
pill_w = tag_w + pad_x * 2 + dot_r * 2 + 14
pill_h = tag_h + pad_y * 2 + 8

# Pill background
pill = Image.new("RGBA", (pill_w, pill_h), (0, 0, 0, 0))
pd = ImageDraw.Draw(pill)
pd.rounded_rectangle([0, 0, pill_w, pill_h], radius=pill_h // 2,
                     fill=(110, 231, 255, 20), outline=(110, 231, 255, 90), width=2)
img.paste(pill, (tag_x, tag_y), pill)

# Dot with glow
dot_cx = tag_x + pad_x + dot_r
dot_cy = tag_y + pill_h // 2
glow_dot = Image.new("RGBA", (80, 80), (0, 0, 0, 0))
gdd = ImageDraw.Draw(glow_dot)
gdd.ellipse([20, 20, 60, 60], fill=(110, 231, 255, 120))
glow_dot = glow_dot.filter(ImageFilter.GaussianBlur(radius=8))
img.paste(glow_dot, (dot_cx - 40, dot_cy - 40), glow_dot)
draw = ImageDraw.Draw(img)
draw.ellipse([dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r], fill=ACCENT)
# Tag text
draw.text((dot_cx + dot_r + 14, tag_y + pad_y + 2), tag_text, font=tag_font, fill=ACCENT_SOFT)

# ── Headline (Instrument Serif, w/ italic second half)
# "Building an AI-forward studio" + italic " in public."
h1_a = "Building an AI-forward"
h1_b = "studio "
h1_b_it = "in public."

hx = SAFE_X
hy = tag_y + pill_h + 36

# Line 1
draw.text((hx, hy), h1_a, font=headline_font, fill=TEXT)
# Line 2: straight "studio " then italic "in public."
line2_y = hy + 150
draw.text((hx, line2_y), h1_b, font=headline_font, fill=TEXT)
b_bbox = draw.textbbox((0, 0), h1_b, font=headline_font)
b_w = b_bbox[2] - b_bbox[0]
draw.text((hx + b_w, line2_y), h1_b_it, font=headline_it_font, fill=(231, 234, 240, 150))

# ── Right-side meta (pillars + cadence), bottom-right of safe zone
pillars = "Build logs · AI tool reviews · Tutorials"
cadence = "New videos most weeks"
p_bbox = draw.textbbox((0, 0), pillars, font=pillar_font)
p_w = p_bbox[2] - p_bbox[0]
right_x = SAFE_X + SAFE_W - p_w
py = SAFE_Y + SAFE_H - 80
draw.text((right_x, py), pillars, font=pillar_font, fill=(180, 195, 210))
c_bbox = draw.textbbox((0, 0), cadence, font=cadence_font)
c_w = c_bbox[2] - c_bbox[0]
draw.text((SAFE_X + SAFE_W - c_w, py + 42), cadence, font=cadence_font, fill=(130, 150, 170))

# Thin hairline separator above meta (matches site's border hairlines)
hair_y = py - 20
draw.line([(right_x, hair_y), (SAFE_X + SAFE_W, hair_y)], fill=(255, 255, 255, 25), width=1)

out = "/Users/william/Desktop/Williams Hub/space-studios-site/assets/youtube-banner.png"
img.convert("RGB").save(out, "PNG", optimize=True)
print(out)
