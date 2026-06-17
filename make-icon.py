"""Genera un icono ORIGINAL de gatita kawaii en rosa (diseño propio).
Escribe los mipmaps de Android. Se ejecuta en el build."""
from PIL import Image, ImageDraw
import os

PINK_BG1=(244,114,182)   # rosa medio
PINK_BG2=(219,39,119)    # rosa fuerte
FACE=(255,251,253)       # casi blanco
EARIN=(249,168,212)      # rosa claro oreja
NOSE=(244,114,182)
BLUSH=(251,182,206)
DARK=(60,20,40)
HEART=(236,72,153)

def lerp(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))

def draw_icon(sz, adaptive=False):
    img=Image.new("RGBA",(sz,sz),(0,0,0,0))
    d=ImageDraw.Draw(img)
    if not adaptive:
        # fondo rosa con degradado vertical + esquinas redondeadas
        grad=Image.new("RGB",(sz,sz),PINK_BG1)
        gd=ImageDraw.Draw(grad)
        for y in range(sz):
            gd.line([(0,y),(sz,y)], fill=lerp(PINK_BG1,PINK_BG2,y/sz))
        mask=Image.new("L",(sz,sz),0)
        ImageDraw.Draw(mask).rounded_rectangle([0,0,sz,sz],radius=int(sz*0.22),fill=255)
        img.paste(grad,(0,0),mask)
        d=ImageDraw.Draw(img)
    # zona segura para adaptive (la cara va más chica y centrada)
    cx,cy=sz/2, sz*0.54
    r=sz*(0.26 if adaptive else 0.30)
    # orejas (triángulos)
    earw=r*0.95
    for sgn in (-1,1):
        ex=cx+sgn*r*0.72
        ey=cy-r*0.78
        d.polygon([(ex-earw*0.5,ey+earw*0.55),(ex+earw*0.5,ey+earw*0.55),(ex+sgn*earw*0.18,ey-earw*0.6)],fill=FACE)
        d.polygon([(ex-earw*0.26,ey+earw*0.42),(ex+earw*0.26,ey+earw*0.42),(ex+sgn*earw*0.10,ey-earw*0.18)],fill=EARIN)
    # cara (círculo)
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=FACE)
    # ojos
    eo=r*0.42; ey=cy-r*0.05; er=r*0.12
    for sgn in (-1,1):
        d.ellipse([cx+sgn*eo-er,ey-er*1.3,cx+sgn*eo+er,ey+er*1.3],fill=DARK)
        d.ellipse([cx+sgn*eo-er*0.35,ey-er*0.9,cx+sgn*eo+er*0.2,ey-er*0.2],fill=(255,255,255))
    # mejillas (blush)
    bo=r*0.62; by=cy+r*0.18; br=r*0.16
    for sgn in (-1,1):
        d.ellipse([cx+sgn*bo-br,by-br*0.7,cx+sgn*bo+br,by+br*0.7],fill=BLUSH)
    # nariz
    nr=r*0.09
    d.polygon([(cx-nr,cy+r*0.16),(cx+nr,cy+r*0.16),(cx,cy+r*0.28)],fill=NOSE)
    # bigotes
    lw=max(2,int(sz*0.012))
    for sgn in (-1,1):
        for k in (-1,0,1):
            y=cy+r*0.18+k*r*0.16
            d.line([(cx+sgn*r*0.5,y),(cx+sgn*r*1.15,y-k*r*0.06)],fill=(180,140,160),width=lw)
    # corazoncito arriba (acento original, en vez de moño)
    hs=r*0.34; hx=cx+r*0.72; hy=cy-r*1.02
    d.ellipse([hx-hs*0.5,hy-hs*0.35,hx,hy+hs*0.2],fill=HEART)
    d.ellipse([hx,hy-hs*0.35,hx+hs*0.5,hy+hs*0.2],fill=HEART)
    d.polygon([(hx-hs*0.48,hy),(hx+hs*0.48,hy),(hx,hy+hs*0.6)],fill=HEART)
    return img

base="android/app/src/main/res"
dens={"mdpi":48,"hdpi":72,"xhdpi":96,"xxhdpi":144,"xxxhdpi":192}
for name,s in dens.items():
    folder=f"{base}/mipmap-{name}"
    os.makedirs(folder,exist_ok=True)
    draw_icon(s).save(f"{folder}/ic_launcher.png")
    draw_icon(s).save(f"{folder}/ic_launcher_round.png")
    draw_icon(int(s*2.0),adaptive=True).save(f"{folder}/ic_launcher_foreground.png")

# fondo rosa del icono adaptable
os.makedirs(f"{base}/values",exist_ok=True)
open(f"{base}/values/ic_launcher_background.xml","w").write(
'<?xml version="1.0" encoding="utf-8"?>\n<resources>\n  <color name="ic_launcher_background">#DB2777</color>\n</resources>\n')
# quita el vector por defecto si existe
for p in [f"{base}/drawable-v24/ic_launcher_foreground.xml"]:
    if os.path.exists(p): os.remove(p)
print("icono gatita rosa generado")
