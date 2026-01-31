import pygame
import math

def draw_line_aa(surface: pygame.Surface, 
                 color, points, 
                 width: int = 6, 
                 ss: int = 4, 
                 step: float = 0.5):
    """
    Tegner jevn tykk linje uten hakk ved å stempling (circles) langs path + supersampling.
    step: hvor tett vi sampler i forhold til radius (lavere = glattere, tregere)
    """
    if len(points) < 2:
        return

    # Normaliser input
    pts = []
    for p in points:
        if isinstance(p, pygame.Vector2):
            pts.append((p.x, p.y))
        else:
            pts.append((float(p[0]), float(p[1])))

    r = width / 2.0
    pad = width + 4

    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    minx = math.floor(min(xs) - pad)
    miny = math.floor(min(ys) - pad)
    maxx = math.ceil(max(xs) + pad)
    maxy = math.ceil(max(ys) + pad)

    W = max(1, int((maxx - minx) * ss))
    H = max(1, int((maxy - miny) * ss))

    tmp = pygame.Surface((W, H), pygame.SRCALPHA)
    tmp.fill((0, 0, 0, 0))

    rr = max(1, int(round(r * ss)))
    stamp_step = max(1, int(round(rr * step)))  # hvor mange px mellom stamps (i upscaled)

    def up(p):
        return ((p[0] - minx) * ss, (p[1] - miny) * ss)

    # Stemple sirkler langs hvert segment
    for i in range(len(pts) - 1):
        x1, y1 = up(pts[i])
        x2, y2 = up(pts[i + 1])

        dx = x2 - x1
        dy = y2 - y1
        dist = math.hypot(dx, dy)
        if dist < 1e-6:
            continue

        steps = max(1, int(dist / stamp_step))
        for s in range(steps + 1):
            t = s / steps
            x = x1 + dx * t
            y = y1 + dy * t
            pygame.draw.circle(tmp, color, (int(x), int(y)), rr)

    # Nedskaler med AA
    down = pygame.transform.smoothscale(tmp, (max(1, W // ss), max(1, H // ss)))
    surface.blit(down, (minx, miny), special_flags=pygame.BLEND_RGBA_MAX)


def draw_polyline_aa(surface: pygame.Surface,
                             color,
                             points,
                             width: int = 6,
                             ss: int = 4,
                             overlap_px: int = 1):
    """
    Tykk polyline som polygon (quad per segment) + supersampling.
    - Flate ender (butt caps)
    - 1 px overlap mellom segmenter for å unngå sprekker
    """
    if len(points) < 2:
        return

    # Normaliser input til Vector2
    pts = []
    for p in points:
        if isinstance(p, pygame.Vector2):
            pts.append(p)
        else:
            pts.append(pygame.Vector2(float(p[0]), float(p[1])))

    r = width / 2.0
    pad = width + 4

    xs = [p.x for p in pts]
    ys = [p.y for p in pts]
    minx = math.floor(min(xs) - pad)
    miny = math.floor(min(ys) - pad)
    maxx = math.ceil(max(xs) + pad)
    maxy = math.ceil(max(ys) + pad)

    W = max(1, int((maxx - minx) * ss))
    H = max(1, int((maxy - miny) * ss))

    tmp = pygame.Surface((W, H), pygame.SRCALPHA)
    tmp.fill((0, 0, 0, 0))

    rr = r * ss
    ov = overlap_px * ss  # overlap i oppskalert space

    def up(v: pygame.Vector2) -> pygame.Vector2:
        return pygame.Vector2((v.x - minx) * ss, (v.y - miny) * ss)

    last_seg = len(pts) - 2

    for i in range(len(pts) - 1):
        a = up(pts[i])
        b = up(pts[i + 1])
        d = b - a
        if d.length_squared() < 1e-8:
            continue

        n = d.normalize()  # segmentretning

        # Overlap kun inn mot nabosegmenter:
        # - ikke forleng før aller første punkt
        # - ikke forleng etter aller siste punkt
        start_ext = ov if i > 0 else 0
        end_ext   = ov if i < last_seg else 0

        a2 = a - n * start_ext
        b2 = b + n * end_ext

        perp = pygame.Vector2(-n.y, n.x) * rr

        p1 = a2 + perp
        p2 = a2 - perp
        p3 = b2 - perp
        p4 = b2 + perp

        pygame.draw.polygon(
            tmp,
            color,
            [(p1.x, p1.y), (p2.x, p2.y), (p3.x, p3.y), (p4.x, p4.y)]
        )

    down = pygame.transform.smoothscale(tmp, (max(1, W // ss), max(1, H // ss)))
    surface.blit(down, (minx, miny), special_flags=pygame.BLEND_RGBA_MAX)
