# overlay.py

"""
Module: warp_overlay

Provides a non-blocking, importable desktop-wide "warp drive" shader overlay
that stretches your screen outward uniformly, simulating extreme forward acceleration.
It runs once for `duration` seconds, then does a quick unfade and stops.
"""
import threading
import time
import sys
import glfw
import moderngl
import numpy as np
from PIL import ImageGrab, Image

class WarpOverlay:
    def __init__(self, max_intensity=5.0, duration=6.0, fps=60):
        self.max_intensity = max_intensity  # final stretch multiplier
        self.duration = duration            # total warp duration
        self.fps = fps
        self._stop_event = threading.Event()
        self._thread = None
        self._start_time = None
        self.finished = False

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self, timeout=None):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout)
    def get_finished(self):
        return self.finished

    def _run(self):
        if not glfw.init():
            return
        # Create fullscreen, transparent window
        glfw.window_hint(glfw.DECORATED, False)
        glfw.window_hint(glfw.FLOATING, True)
        glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, False)
        monitor = glfw.get_primary_monitor()
        mode = glfw.get_video_mode(monitor)
        width, height = mode.size.width, mode.size.height
        window = glfw.create_window(width, height, "", None, None)
        glfw.make_context_current(window)

        # ModernGL context
        ctx = moderngl.create_context()
        ctx.enable(moderngl.BLEND)
        ctx.blend_func = (moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA)

        # Fullscreen quad
        quad = np.array([-1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0], dtype='f4')
        vbo = ctx.buffer(quad.tobytes())
        prog = ctx.program(
            vertex_shader="""
                #version 330
                in vec2 in_pos;
                out vec2 v_uv;
                void main() {
                    v_uv = in_pos * 0.5 + 0.5;
                    gl_Position = vec4(in_pos, 0.0, 1.0);
                }
            """,
            fragment_shader="""
                #version 330 core
                uniform sampler2D screenTex;
                uniform float elapsed;
                uniform float duration;
                uniform float maxIntensity;
                in vec2 v_uv;
                out vec4 f_color;

                void main() {
                    float unfadeDuration = 0.2;
                    float warpEnd = duration;
                    float totalTime = duration + unfadeDuration;
                    float p = clamp(elapsed / duration, 0.0, 1.0);
                    float intensity = pow(p, 2.0) * maxIntensity;

                    vec4 color;
                    if (elapsed < warpEnd) {
                        vec2 coord = v_uv - vec2(0.5);
                        float dist = length(coord);
                        float stretch = 1.0 + intensity * (1.0 - dist * 2.0);
                        vec2 sample_uv = coord * stretch + vec2(0.5);
                        if(sample_uv.x < 0.0 || sample_uv.x > 1.0 || sample_uv.y < 0.0 || sample_uv.y > 1.0) {
                            color = vec4(0.0);
                        } else {
                            color = texture(screenTex, sample_uv);
                        }
                        color = mix(color, vec4(0.0), p);
                    } else {
                        // unfade: revert from white back to screen
                        float unfadeP = clamp((elapsed - warpEnd) / unfadeDuration, 0.0, 1.0);
                        vec4 texColor = texture(screenTex, v_uv);
                        color = mix(vec4(1.0), texColor, unfadeP);
                    }
                    f_color = color;
                }
            """
        )
        vao = ctx.simple_vertex_array(prog, vbo, 'in_pos')

        # Dynamic screen texture
        texture = ctx.texture((width, height), 4)
        texture.filter = (moderngl.LINEAR, moderngl.LINEAR)

        self._start_time = time.time()
        interval = 1.0 / self.fps
        last_frame = None

        while not glfw.window_should_close(window) and not self._stop_event.is_set():
            elapsed = time.time() - self._start_time
            if elapsed > self.duration + 0.2:
                break
            img = ImageGrab.grab()
            img = img.resize((width, height))
            img = img.transpose(method=Image.FLIP_TOP_BOTTOM)
            last_frame = img.convert('RGBA').tobytes()
            texture.write(last_frame)
            ctx.viewport = (0, 0, width, height)
            prog['elapsed'].value = elapsed
            prog['duration'].value = self.duration
            prog['maxIntensity'].value = self.max_intensity
            texture.use(location=0)
            prog['screenTex'].value = 0
            ctx.clear(0.0, 0.0, 0.0, 0.0)
            vao.render(mode=moderngl.TRIANGLE_STRIP)
            glfw.swap_buffers(window)
            glfw.poll_events()
            time.sleep(interval)

        # Final frame with last screen image to avoid black flash
        if last_frame:
            texture.write(last_frame)
            ctx.viewport = (0, 0, width, height)
            prog['elapsed'].value = self.duration + 0.2
            prog['duration'].value = self.duration
            prog['maxIntensity'].value = self.max_intensity
            texture.use(location=0)
            prog['screenTex'].value = 0
            ctx.clear(0.0, 0.0, 0.0, 0.0)
            vao.render(mode=moderngl.TRIANGLE_STRIP)
            self.finished = True
            glfw.swap_buffers(window)
            time.sleep(0.05)  # allow one more frame before close

        glfw.terminate()

# Example usage
if __name__ == '__main__':
    overlay = WarpOverlay(max_intensity=5.0, duration=6.0, fps=60)
    overlay.start()
    try:
        while overlay._thread.is_alive():
            time.sleep(0.1)
    except KeyboardInterrupt:
        overlay.stop()
