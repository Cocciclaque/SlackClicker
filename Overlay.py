# overlay.py

"""
Module: overlay

Provides a non-blocking, importable desktop overlay with multiple shader effects
around the active window’s frame+shadow, excluding the taskbar. Use Overlay.start(),
Overlay.switch_shader(name), and Overlay.stop().
Available shaders: "balatro", "crt", "shop", "postit".
"""
import ctypes
import win32gui, win32api, win32con
import glfw
import moderngl
import numpy as np
import threading
from time import time, sleep
from ctypes import wintypes
from PIL import Image, ImageDraw, ImageFont  # for text rendering
import random

# DWM constant for extended frame bounds (includes drop-shadow)
DWMWA_EXTENDED_FRAME_BOUNDS = 9

# ----------------------------------------------------------------------------
# Geometry & Window Helpers
# ----------------------------------------------------------------------------
def get_foreground_window():
    hwnd = win32gui.GetForegroundWindow()
    return hwnd if hwnd and win32gui.IsWindowVisible(hwnd) else None

def get_window_shadow_rect(hwnd):
    rect = wintypes.RECT()
    ctypes.windll.dwmapi.DwmGetWindowAttribute(
        hwnd,
        ctypes.c_uint(DWMWA_EXTENDED_FRAME_BOUNDS),
        ctypes.byref(rect),
        ctypes.sizeof(rect)
    )
    return rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top

def get_work_area(hwnd):
    hmon = win32api.MonitorFromWindow(hwnd, win32con.MONITOR_DEFAULTTONEAREST)
    work = win32api.GetMonitorInfo(hmon)['Work']
    x, y = work[0], work[1]
    return x, y, work[2] - x, work[3] - y

def build_outer_vertices(left, right, top, bottom):
    return np.array([
        -1,  1,   1,  1,  -1, top,
         1,  1,   1, top, -1, top,
        -1, bottom, 1, bottom, -1, -1,
         1, bottom, 1, -1,      -1, -1,
        -1, top,    left, top,   -1, bottom,
         left, top, left, bottom, -1, bottom,
         right, top, 1, top,      right, bottom,
         1, top,     1, bottom,   right, bottom,
    ], dtype='f4')

# ----------------------------------------------------------------------------
# Shader Sources (omitted BALATRO, CRT, SHOP for brevity)
# ----------------------------------------------------------------------------
VERT_SRC = """
#version 330
in vec2 in_pos;
void main() { gl_Position = vec4(in_pos, 0.0, 1.0); }
"""


# Full balatro fragment shader
BALATRO_FRAG = """
#version 330 core
uniform float time;
uniform vec2  resolution;
uniform float spin_speed;
uniform float move_speed;
uniform vec2  offset;
uniform vec4  colour1;
uniform vec4  colour2;
uniform vec4  colour3;
uniform float contrast;
uniform float lighting;
uniform float spin_amount;
uniform float pixel_filter;
uniform bool  is_rotating;
out vec4 f_color;

vec4 balatro_effect(vec2 fragCoord) {
    vec2 sz = resolution;
    float pixel_size = length(sz) / pixel_filter;
    vec2 uv = (floor(fragCoord * (1.0/pixel_size)) * pixel_size - 0.5*sz) / length(sz)
              - offset;
    float ul = length(uv);
    float speed = spin_speed * (is_rotating ? time : 1.0) * 0.2 + 302.2;
    float ang = atan(uv.y, uv.x)
              + speed
              - (spin_amount * ul + (1.0 - spin_amount)) * 20.0;
    vec2 mid = (sz/length(sz)) * 0.5;
    uv = vec2( ul*cos(ang) + mid.x, ul*sin(ang) + mid.y ) - mid;
    uv *= 30.0;
    speed = time * move_speed;
    vec2 uv2 = vec2(uv.x + uv.y, uv.x + uv.y);
    for(int i=0;i<5;i++){
        uv2 += sin(max(uv.x,uv.y)) + uv;
        uv  += 0.5 * vec2(
            cos(5.1123 + 0.353*uv2.y + speed*0.1311),
            sin(uv2.x - 0.113*speed)
        );
        uv  -= cos(uv.x + uv.y) - sin(uv.x*0.711 - uv.y);
    }
    float cm = (0.25*contrast + 0.5*spin_amount + 1.2);
    float pr = clamp(length(uv)*0.035*cm, 0.0, 2.0);
    float c1p = max(0.0, 1.0 - cm * abs(1.0 - pr));
    float c2p = max(0.0, 1.0 - cm * abs(pr));
    float c3p = 1.0 - min(1.0, c1p + c2p);
    float lig = (lighting - 0.2)*max(c1p*5.0 - 4.0,0.0)
              + lighting * max(c2p*5.0 - 4.0,0.0);
    vec4 col = (0.3/contrast)*colour1
             + (1.0 - 0.3/contrast)*(colour1*c1p + colour2*c2p
             + vec4(c3p*colour3.rgb, c3p*colour1.a))
             + lig;
    return col;
}

void main() {
    vec4 col = balatro_effect(gl_FragCoord.xy);
    f_color = vec4(col.rgb, 1.0);
}
"""

CRT_FRAG = """
#version 330 core
uniform vec2 resolution;
out vec4 f_color;
void main() {
    vec2 uv = gl_FragCoord.xy / resolution;
    float scan = sin(uv.y * resolution.y * 3.1415) * 0.05;
    float vig  = smoothstep(0.8, 0.5, length(uv - 0.5));
    f_color = vec4(vec3(0.9 - scan) * (1.0 - vig), 1.0);
}
"""

SHOP_FRAG = """
#version 330 core
uniform float time;
uniform vec2 resolution;
uniform float fillLevel;
uniform float opacity;
out vec4 f_color;
void main() {
    vec2 uv = gl_FragCoord.xy / resolution;
    vec4 coffee = vec4(0.6, 0.45, 0.3, opacity);
    vec4 dark   = vec4(0.0, 0.0, 0.0, opacity * 0.6);
    vec4 base = mix(coffee, dark, step(fillLevel, uv.y));
    float ripple = sin((uv.x * 20.0 + time * 3.0)) * 0.02;
    if (uv.y < fillLevel) base.rgb += ripple;
    f_color = base;
}
"""

NAN_FRAG = """
#version 330 core
void main(){
}
"""



POSTIT_FRAG = """
#version 330 core
uniform float time;
uniform vec2 holeCenter;
uniform vec2 holeSize;
uniform float opacity;
uniform sampler2D textTexs[8];
uniform vec2    stickySize;
out vec4 f_color;

vec2 rot(vec2 p, float a) {
    float c = cos(a), s = sin(a);
    return vec2(p.x*c - p.y*s, p.x*s + p.y*c);
}

float sdRoundedBox(vec2 p, vec2 b, float r) {
    vec2 d = abs(p) - b + vec2(r);
    return length(max(d,0.0)) - r;
}

float noise(vec2 uv) {
    return fract(sin(dot(uv, vec2(12.9898,78.233))) * 43758.5453);
}

void main() {
    vec2 frag = gl_FragCoord.xy;
    vec4 base = vec4(0,0,0, opacity*0.8);
    float g = noise(frag*0.5 + time*0.1);
    base.rgb *= mix(0.95,1.05, g*0.2);

    float rx = holeSize.x*0.9;
    float ry = holeSize.y*0.7;
    float border = 4.0, radius=8.0;

    for(int i=0;i<8;i++){
        float fi=float(i);
        float ang = fi*(6.2831853/8.0) + time*0.2;
        vec2 pos = holeCenter + vec2(cos(ang)*rx, sin(ang)*ry);
        vec2 p = frag - pos;
        p = rot(p,0.1*sin(time+fi));
        float d = sdRoundedBox(p, stickySize - vec2(border), radius);
        float inside = step(d,0.0);
        float edge = inside - step(d,-border);
        base = mix(base, vec4(1,1,0.3,opacity), inside);
        base = mix(base, vec4(0,0,0,opacity), edge);
        if(inside>0.5){
            vec2 uv = (p + stickySize)/(2.0*stickySize);
            uv.y = 1.0-uv.y;
            vec4 tx = texture(textTexs[i], uv);
            base = mix(base, tx, tx.a);
        }
    }
    f_color = base;
}
"""

class Overlay:
    def __init__(self):
        self._thread=None
        self._stop=threading.Event()
        self._shader_name='balatro'
        self._start_time=time()

    def start(self):
        if self._thread and self._thread.is_alive(): return
        self._stop.clear(); self._thread=threading.Thread(target=self._run,daemon=True); self._thread.start()

    def stop(self,timeout=None):
        self._stop.set();
        if self._thread: self._thread.join(timeout)

    def switch_shader(self,name):
        if name in('balatro','crt','shop','postit','nan'): self._shader_name=name

    def _run(self):
    
        if not glfw.init(): return
        for h,v in[(glfw.DECORATED,False),(glfw.FLOATING,True),(glfw.TRANSPARENT_FRAMEBUFFER,True),(glfw.RESIZABLE,False)]: glfw.window_hint(h,v)
        win=glfw.create_window(100,100,'',None,None)
        hwnd=glfw.get_win32_window(win)
        style=ctypes.windll.user32.GetWindowLongW(hwnd,-20)
        ctypes.windll.user32.SetWindowLongW(hwnd,-20,style|0x80000|0x20)
        glfw.make_context_current(win)
        ctx=moderngl.create_context(); ctx.enable(moderngl.BLEND); ctx.blend_func=(moderngl.SRC_ALPHA,moderngl.ONE_MINUS_SRC_ALPHA)

        sources={'balatro':(VERT_SRC,BALATRO_FRAG),'crt':(VERT_SRC,CRT_FRAG),'shop':(VERT_SRC,SHOP_FRAG),'postit':(VERT_SRC,POSTIT_FRAG)}
        if self._shader_name != 'nan':
            progs={k:ctx.program(vertex_shader=vs,fragment_shader=fs) for k,(vs,fs) in sources.items()}

        # texts for each note
        TEXTS=["Shop","Buy","Lunch\n@1","Boost","Read","Slack","Sleep","Zzz..."]
        HALF=75; size=(HALF*2,HALF*2)
        # prepare fonts
        try: font=ImageFont.truetype("segoescb.ttf",int(HALF*0.5))
        except: font=ImageFont.load_default()
        postit=progs['postit']
        for idx,text in enumerate(TEXTS):
            img=Image.new("RGBA",size,(0,0,0,0)); draw=ImageDraw.Draw(img)
            bb=draw.textbbox((0,0),text,font=font)
            w,h=bb[2]-bb[0],bb[3]-bb[1]
            draw.text(((size[0]-w)/2,(size[1]-h)/2),text,font=font,fill=(0,0,0,255))
            tex=ctx.texture(size,4,img.tobytes()); tex.build_mipmaps(); tex.use(location=idx)
        # bind array of texture units for textSamplers
        postit['textTexs'].value = tuple(range(len(TEXTS)))
        postit['stickySize']=(HALF,HALF)

        vbo=ctx.buffer(reserve=4*6*2*4)
        vaos={k:ctx.simple_vertex_array(p,vbo,'in_pos') for k,p in progs.items()}

        while not glfw.window_should_close(win) and not self._stop.is_set():
            fg=get_foreground_window()
            if fg and self._shader_name != "nan":
                fx,fy,fw,fh=get_window_shadow_rect(fg)
                wx,wy,ww,wh=get_work_area(fg)
                glfw.set_window_pos(win,wx,wy);glfw.set_window_size(win,ww,wh);ctx.viewport=(0,0,ww,wh)
                verts=build_outer_vertices((fx-wx)/ww*2-1,((fx+fw)-wx)/ww*2-1,1-(fy-wy)/wh*2,1-((fy+fh)-wy)/wh*2)
                vbo.orphan();vbo.write(verts.tobytes())
                prog=progs[self._shader_name]; vao=vaos[self._shader_name]
                t=time()-self._start_time
                if self._shader_name=='postit':
                    prog['time'].value=t
                    cx,cy=fx+fw*0.5-wx,fy+fh*0.5-wy
                    prog['holeCenter'].value=(cx,wh-cy);prog['holeSize'].value=(fw,fh);prog['opacity'].value=0.85
                elif self._shader_name=='shop':
                    prog['time'].value=t;prog['resolution'].value=(ww,wh);prog['fillLevel'].value=0.75;prog['opacity'].value=0.75
                elif self._shader_name=='crt': prog['resolution'].value=(ww,wh)
                elif self._shader_name=='balatro':
                    prog['time'].value=t;prog['resolution'].value=(ww,wh)
                ctx.clear(0,0,0,0);vao.render(moderngl.TRIANGLES)
            glfw.swap_buffers(win);glfw.poll_events();sleep(0.01)
        glfw.terminate()

if __name__=='__main__':
    ov=Overlay(); ov.start(); sleep(2); ov.switch_shader('postit')
    try: 
        while True: sleep(1)
    except KeyboardInterrupt: ov.stop()