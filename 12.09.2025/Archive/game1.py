import pygame
import sys
import math
import json
import random
import source as src

# --- Pencere ve yerleşim ---
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 740
TOP_HEIGHT = 540
MENU_WIDTH = 360
WORLD_WIDTH = WINDOW_WIDTH - MENU_WIDTH
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sierra Engine - 1D Playground")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 16)
small_font = pygame.font.SysFont("consolas", 13)

# --- Arka plan ---
BLOCK_SIZE = 32
background_tile = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
background_tile.fill((28, 30, 34))
pygame.draw.rect(background_tile, (40, 40, 45), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 1)

# --- Oyuncu placeholder ---
PLAYER_START_X = 120
PLAYER_START_Y = TOP_HEIGHT - 64 - 10
try:
    player = src.create_character("TESTSUBJECT01", PLAYER_START_X, PLAYER_START_Y, src.CHARACTER_TYPES)
    player_is_engine = True
except Exception:
    size = src.CHARACTER_TYPES.get("TESTSUBJECT01", {}).get('size', 48)
    player = {"type": "TESTSUBJECT01", "x": PLAYER_START_X, "y": PLAYER_START_Y, "size": size, "walk_frames": []}
    player_is_engine = False

# --- Material properties ---
MATERIALS = {
    'metal': {
        'restitution': 0.65,
        'fragility': 0.05,  # low fragility
        'frag_range': (0, 1),
        'density': 0.9,
        'color_tint': (200,200,200)
    },
    'glass': {
        'restitution': 0.45,
        'fragility': 1.0,  # fragile
        'frag_range': (6, 12),
        'density': 0.6,
        'color_tint': (180,220,255)
    },
    'wood': {
        'restitution': 0.55,
        'fragility': 0.5,
        'frag_range': (2,5),
        'density': 0.7,
        'color_tint': (200,170,120)
    },
    'rubber': {
        'restitution': 0.9,
        'fragility': 0.02,
        'frag_range': (0,1),
        'density': 1.1,
        'color_tint': (170,80,200)
    }
}
material_keys = list(MATERIALS.keys())

# --- Objeler ve tipler (her tipin default materyali) ---
OBJECT_TYPES = [
    {"id": "ball_s", "name": "Small Ball",  "radius": 10, "mass": 1.0, "color": (200,80,80),  'material': 'rubber'},
    {"id": "ball_m", "name": "Medium Ball", "radius": 18, "mass": 2.5, "color": (80,200,120), 'material': 'wood'},
    {"id": "ball_l", "name": "Large Ball",  "radius": 28, "mass": 5.0, "color": (80,140,220), 'material': 'metal'},
    {"id": "block",  "name": "Block",       "radius": 24, "mass": 8.0, "color": (200,200,80), 'material': 'wood'}
]
selected_type_idx = 0
objects = []  # each: {x, vx, radius, mass, color, id, uid, material}
next_uid = 1

# --- Particles for visual effects ---
particles = []  # each: {x, y, vx, life, size, color, alpha}

# --- Simülasyon ayarları ---
playing = True
debug = False
base_friction = 0.6
surface_keys = list(src.SURFACE_TYPES.keys()) if hasattr(src, 'SURFACE_TYPES') else ['DEFAULT']
selected_surface_idx = 0
fragmentation_global_threshold = 12.0
min_mass_for_fragment = 0.4

SAVE_PATH = '/mnt/data/1d_playground_save.json'

# --- Helpers ---

def world_to_screen(x):
    return int(x)


def new_uid():
    global next_uid
    uid = next_uid
    next_uid += 1
    return uid


def spawn_particles(x, count, color, speed=2.0, size=3):
    y = TOP_HEIGHT // 2
    for i in range(count):
        ang = random.uniform(-math.pi/2 - 0.4, -math.pi/2 + 0.4)
        vx = math.cos(ang) * random.uniform(-speed, speed)
        vy = math.sin(ang) * random.uniform(0.5, speed)
        particles.append({
            'x': x + random.uniform(-6,6),
            'y': y + random.uniform(-6,6),
            'vx': vx,
            'vy': -vy,
            'life': random.uniform(0.5, 1.2),
            'size': random.uniform(max(1, size*0.6), size*1.4),
            'color': color,
            'alpha': 1.0
        })

# --- Draw helpers ---

def draw_background():
    for y in range(0, TOP_HEIGHT, BLOCK_SIZE):
        for x in range(0, WORLD_WIDTH, BLOCK_SIZE):
            screen.blit(background_tile, (x, y))


def draw_particles(dt):
    # draw and update particles
    to_remove = []
    surf = pygame.Surface((WINDOW_WIDTH, TOP_HEIGHT), pygame.SRCALPHA)
    for p in particles:
        p['x'] += p['vx'] * dt * 60
        p['y'] += p['vy'] * dt * 60
        p['vy'] += 9.8 * dt * 30  # gravity effect for particles
        p['life'] -= dt
        p['alpha'] = max(0.0, p['life'] / 1.2)
        if p['life'] <= 0:
            to_remove.append(p)
        else:
            c = p['color']
            a = int(255 * p['alpha'])
            pygame.draw.circle(surf, (c[0], c[1], c[2], a), (int(p['x']), int(p['y'])), max(1, int(p['size'])))
    for r in to_remove:
        particles.remove(r)
    screen.blit(surf, (0,0))


def draw_objects():
    y = TOP_HEIGHT // 2
    for obj in objects:
        sx = world_to_screen(obj['x'])
        # tint color by material
        mat = MATERIALS.get(obj.get('material', 'metal'), None)
        color = obj['color']
        if mat:
            tint = mat['color_tint']
            color = (min(255, int((color[0]+tint[0])/2)), min(255, int((color[1]+tint[1])/2)), min(255, int((color[2]+tint[2])/2)))
        pygame.draw.circle(screen, color, (sx, y), int(max(1, obj['radius'])))
        if abs(obj['vx']) > 0.1:
            endx = int(sx + max(-80, min(80, obj['vx'] * 8)))
            pygame.draw.line(screen, (255,255,255), (sx, y), (endx, y), 2)
        label = f"#{obj['uid']} {obj['material']} m:{obj['mass']:.2f} v:{obj['vx']:.2f}"
        s = small_font.render(label, True, (220,220,220))
        screen.blit(s, (sx - s.get_width()//2, y + obj['radius'] + 6))


def draw_player_custom():
    if player_is_engine:
        try:
            src.draw_player(screen, player, 0)
            return
        except Exception:
            pass
    size = player.get('size', 48)
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.rect(surf, (180,200,255), (0,0,size,size))
    screen.blit(surf, (player['x'] - size//2, player['y'] - size//2))

# --- Menu and controls UI ---

def draw_menu(mouse_pos=None):
    menu_x = WORLD_WIDTH
    pygame.draw.rect(screen, (18,18,22), (menu_x, 0, MENU_WIDTH, TOP_HEIGHT))
    x = menu_x + 12
    y = 12
    title = font.render('Objects (Materials & Fragments)', True, (230,230,230))
    screen.blit(title, (x, y))
    y += 32

    # surface selection
    surf_label = small_font.render('Surface: ' + surface_keys[selected_surface_idx], True, (200,200,200))
    screen.blit(surf_label, (x, y))
    y += 18
    prev_rect = pygame.Rect(x, y, 28, 20)
    next_rect = pygame.Rect(x + 200, y, 28, 20)
    pygame.draw.rect(screen, (40,40,50), prev_rect)
    pygame.draw.rect(screen, (40,40,50), next_rect)
    screen.blit(small_font.render('<', True, (220,220,220)), (prev_rect.x+8, prev_rect.y+2))
    screen.blit(small_font.render('>', True, (220,220,220)), (next_rect.x+8, next_rect.y+2))
    y += 32

    # object palette
    pal_top = y
    for i, t in enumerate(OBJECT_TYPES):
        rect = pygame.Rect(x, y, MENU_WIDTH - 24, 48)
        pygame.draw.rect(screen, (30,30,36), rect)
        if i == selected_type_idx:
            pygame.draw.rect(screen, (60,60,80), rect, 2)
        cx = rect.x + 28
        cy = rect.y + rect.h//2
        pygame.draw.circle(screen, t['color'], (cx, cy), int(t['radius']/1.5))
        name_s = small_font.render(t['name'], True, (230,230,230))
        screen.blit(name_s, (rect.x + 64, rect.y + 14))
        # material label for each
        mat = t.get('material', 'metal')
        m_s = small_font.render(mat, True, (160,160,160))
        screen.blit(m_s, (rect.x + rect.w - 64, rect.y + 14))
        y += 56

    # material adjust for selected type
    y += 6
    sel_t = OBJECT_TYPES[selected_type_idx]
    screen.blit(small_font.render('Material for selected type:', True, (200,200,200)), (x, y))
    y += 18
    mprev = pygame.Rect(x, y, 28, 20)
    mnext = pygame.Rect(x + 200, y, 28, 20)
    pygame.draw.rect(screen, (40,40,50), mprev)
    pygame.draw.rect(screen, (40,40,50), mnext)
    screen.blit(small_font.render('<', True, (220,220,220)), (mprev.x+8, mprev.y+2))
    screen.blit(small_font.render('>', True, (220,220,220)), (mnext.x+8, mnext.y+2))
    screen.blit(small_font.render(sel_t.get('material','metal'), True, (230,230,230)), (x+44, y+2))
    y += 36

    # fragmentation control
    frag_label = small_font.render(f'Frag threshold: {fragmentation_global_threshold:.1f}', True, (220,220,220))
    screen.blit(frag_label, (x, y))
    frag_minus = pygame.Rect(x, y+22, 28, 20)
    frag_plus = pygame.Rect(x+120, y+22, 28, 20)
    pygame.draw.rect(screen, (40,40,50), frag_minus)
    pygame.draw.rect(screen, (40,40,50), frag_plus)
    screen.blit(small_font.render('-', True, (220,220,220)), (frag_minus.x+10, frag_minus.y+2))
    screen.blit(small_font.render('+', True, (220,220,220)), (frag_plus.x+10, frag_plus.y+2))
    y += 56

    # Play/Pause/Step/Save/Load/Clear
    btns = [ ('Play' if not playing else 'Pause'), ('Step'), ('Save'), ('Load'), ('Clear') ]
    btn_rects = []
    for b in btns:
        r = pygame.Rect(x, y, MENU_WIDTH-24, 36)
        pygame.draw.rect(screen, (40,40,48), r)
        screen.blit(small_font.render(b, True, (230,230,230)), (r.x+8, r.y+8))
        btn_rects.append((b,r))
        y += 44

    # Selected object info
    y += 6
    info_title = small_font.render('Selected object:', True, (200,200,200))
    screen.blit(info_title, (x, y))
    y += 20
    sel = get_selected_object_index(mouse_pos)
    if sel is not None:
        o = objects[sel]
        lines = [f'uid: {o["uid"]}', f'material: {o["material"]}', f'mass: {o["mass"]:.2f}', f'vx: {o["vx"]:.2f}', f'x: {o["x"]:.1f}']
        for ln in lines:
            screen.blit(small_font.render(ln, True, (220,220,220)), (x, y))
            y += 16
    else:
        screen.blit(small_font.render('None', True, (160,160,160)), (x, y))

    rect_map = {
        'surface_prev': prev_rect,
        'surface_next': next_rect,
        'frag_minus': frag_minus,
        'frag_plus': frag_plus,
        'buttons': btn_rects,
        'palette_top': (pal_top, y)
    }
    # also include material prev/next rects
    rect_map['mat_prev'] = mprev
    rect_map['mat_next'] = mnext
    return rect_map

# Helper: find object under mouse

def get_selected_object_index(mouse_pos):
    if mouse_pos is None:
        return None
    mx,my = mouse_pos
    if not (0 <= mx < WORLD_WIDTH and 0 <= my < TOP_HEIGHT):
        return None
    for i in range(len(objects)-1, -1, -1):
        o = objects[i]
        if abs(o['x'] - mx) <= o['radius']:
            return i
    return None

# --- Physics ---

def resolve_collisions(dt):
    global objects
    n = len(objects)
    # naive O(n^2)
    for i in range(n):
        for j in range(i+1, n):
            a = objects[i]
            b = objects[j]
            dist = abs(a['x'] - b['x'])
            min_dist = a['radius'] + b['radius']
            if dist < min_dist and dist > 0:
                overlap = min_dist - dist
                total_mass = a['mass'] + b['mass']
                sign = 1 if a['x'] < b['x'] else -1
                a['x'] -= sign * (overlap * (b['mass'] / total_mass))
                b['x'] += sign * (overlap * (a['mass'] / total_mass))

                u1 = a['vx']
                u2 = b['vx']
                m1 = a['mass']
                m2 = b['mass']

                # restitution from materials (mass-weighted average)
                e1 = MATERIALS.get(a.get('material','metal'), {}).get('restitution', 0.8)
                e2 = MATERIALS.get(b.get('material','metal'), {}).get('restitution', 0.8)
                restitution = (e1*m1 + e2*m2) / (m1 + m2)

                v1 = (u1*(m1 - m2) + 2*m2*u2) / (m1 + m2)
                v2 = (u2*(m2 - m1) + 2*m1*u1) / (m1 + m2)

                rel_speed = abs(u1 - u2)

                # fragmentation check influenced by material fragility
                frag_chance = 0.0
                frag_a = MATERIALS.get(a.get('material','metal'), {}).get('fragility', 0.0)
                frag_b = MATERIALS.get(b.get('material','metal'), {}).get('fragility', 0.0)
                # choose the more fragile one as candidate
                candidate_idx = i if frag_a >= frag_b else j
                candidate = objects[candidate_idx]
                candidate_fragility = max(frag_a, frag_b)

                if rel_speed >= fragmentation_global_threshold * candidate_fragility and candidate['mass'] > min_mass_for_fragment:
                    # perform fragmentation on candidate
                    mat = MATERIALS.get(candidate.get('material','glass'), {})
                    frag_min, frag_max = mat.get('frag_range', (2,3))
                    count = random.randint(max(1, int(frag_min)), max(1, int(frag_max)))
                    # ensure not too many fragments
                    count = min(count, 12)
                    # split mass
                    total_mass = candidate['mass']
                    pieces = []
                    for k in range(count):
                        if k == count - 1:
                            m_frag = total_mass - sum([p['mass'] for p in pieces])
                        else:
                            remaining = total_mass - sum([p['mass'] for p in pieces])
                            # random split but avoid extremely tiny
                            m_frag = max(0.05, remaining * random.uniform(0.15, 0.5))
                        pieces.append({'mass': m_frag})
                    # compute density from original radius: density = mass / (radius^2)
                    density = candidate['mass'] / max(1.0, (candidate['radius']**2))
                    # create fragments around candidate position
                    cx = candidate['x']
                    base_v = candidate['vx']
                    # remove candidate
                    objects.pop(candidate_idx)
                    for p in pieces:
                        r_frag = math.sqrt(max(0.5, p['mass'] / density))
                        angle = random.uniform(-0.8, 0.8)
                        vx = base_v + random.uniform(-3, 3)
                        frag_obj = {
                            'x': cx + random.uniform(-candidate['radius']*0.3, candidate['radius']*0.3),
                            'vx': vx,
                            'radius': max(2, r_frag),
                            'mass': p['mass'],
                            'color': candidate['color'],
                            'id': candidate['id'] + '_frag',
                            'uid': new_uid(),
                            'material': candidate.get('material', 'glass')
                        }
                        objects.append(frag_obj)
                    # spawn particles visual
                    spawn_particles(cx, max(6, count*3), candidate['color'], speed=3.0, size=3)
                    return

                # otherwise assign velocities with restitution
                a['vx'] = v1 * restitution
                b['vx'] = v2 * restitution


def physics_update(dt):
    # friction from chosen surface
    surface_key = surface_keys[selected_surface_idx] if surface_keys else None
    surface_friction = 1.0
    if hasattr(src, 'SURFACE_TYPES') and surface_key in getattr(src, 'SURFACE_TYPES', {}):
        surface_friction = src.SURFACE_TYPES[surface_key].get('friction', 1.0)
    combined_friction = base_friction * surface_friction

    for obj in objects:
        obj['vx'] *= max(0.0, 1.0 - combined_friction * dt * 0.02)
        obj['x'] += obj['vx'] * dt
        # world bounds
        if obj['x'] - obj['radius'] < 0:
            obj['x'] = obj['radius']
            obj['vx'] = -obj['vx'] * 0.6
        if obj['x'] + obj['radius'] > WORLD_WIDTH:
            obj['x'] = WORLD_WIDTH - obj['radius']
            obj['vx'] = -obj['vx'] * 0.6
    resolve_collisions(dt)

    # update particles
    dt_s = dt / 60.0
    to_remove = []
    for p in particles:
        p['life'] -= dt_s
        if p['life'] <= 0:
            to_remove.append(p)
    for r in to_remove:
        if r in particles:
            particles.remove(r)

# --- IO ---

def save_state(path=SAVE_PATH):
    try:
        dump = {'objects': objects, 'next_uid': next_uid, 'surface_idx': selected_surface_idx}
        with open(path, 'w') as f:
            json.dump(dump, f)
        print('Saved to', path)
    except Exception as e:
        print('Save failed:', e)


def load_state(path=SAVE_PATH):
    global objects, next_uid, selected_surface_idx
    try:
        with open(path, 'r') as f:
            dump = json.load(f)
        objects = dump.get('objects', [])
        next_uid = dump.get('next_uid', max([o.get('uid',0) for o in objects], default=0) + 1)
        selected_surface_idx = dump.get('surface_idx', 0)
        print('Loaded from', path)
    except Exception as e:
        print('Load failed:', e)

# --- Input state ---
placing = False
place_start_x = 0
dragging_idx = None

# --- Main loop ---
running = True
step_once = False

while running:
    dt = clock.tick(FPS) / 1.0
    mouse_pos = pygame.mouse.get_pos()
    mx, my = mouse_pos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_d:
                debug = not debug
            if event.key == pygame.K_SPACE:
                playing = not playing
            if event.key == pygame.K_n:
                step_once = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left
                if mx >= WORLD_WIDTH:
                    rects = draw_menu(mouse_pos)
                    if rects['surface_prev'].collidepoint(mouse_pos):
                        selected_surface_idx = (selected_surface_idx - 1) % len(surface_keys)
                    elif rects['surface_next'].collidepoint(mouse_pos):
                        selected_surface_idx = (selected_surface_idx + 1) % len(surface_keys)
                    elif rects['frag_minus'].collidepoint(mouse_pos):
                        fragmentation_global_threshold = max(0.5, fragmentation_global_threshold - 1.0)
                    elif rects['frag_plus'].collidepoint(mouse_pos):
                        fragmentation_global_threshold += 1.0
                    elif rects['mat_prev'].collidepoint(mouse_pos):
                        # cycle material for selected type
                        cur = OBJECT_TYPES[selected_type_idx]['material']
                        i = material_keys.index(cur)
                        OBJECT_TYPES[selected_type_idx]['material'] = material_keys[(i-1) % len(material_keys)]
                    elif rects['mat_next'].collidepoint(mouse_pos):
                        cur = OBJECT_TYPES[selected_type_idx]['material']
                        i = material_keys.index(cur)
                        OBJECT_TYPES[selected_type_idx]['material'] = material_keys[(i+1) % len(material_keys)]
                    else:
                        for name, r in rects['buttons']:
                            if r.collidepoint(mouse_pos):
                                if name == 'Play':
                                    playing = True
                                elif name == 'Pause':
                                    playing = False
                                elif name == 'Step':
                                    step_once = True
                                elif name == 'Save':
                                    save_state()
                                elif name == 'Load':
                                    load_state()
                                elif name == 'Clear':
                                    objects = []
                    # palette selection
                    pal_top, pal_bottom = rects['palette_top']
                    if my >= pal_top and my < pal_top + len(OBJECT_TYPES)*56:
                        idx = (my - pal_top) // 56
                        if 0 <= idx < len(OBJECT_TYPES):
                            selected_type_idx = int(idx)
                else:
                    sel = get_selected_object_index(mouse_pos)
                    if sel is not None:
                        dragging_idx = sel
                        placing = False
                    else:
                        placing = True
                        place_start_x = mx
                        dragging_idx = None
            elif event.button == 3:  # right click -> delete
                if mx < WORLD_WIDTH:
                    sel = get_selected_object_index(mouse_pos)
                    if sel is not None:
                        objects.pop(sel)
            elif event.button == 2:  # middle click -> impulse
                sel = get_selected_object_index(mouse_pos)
                if sel is not None:
                    obj = objects[sel]
                    obj['vx'] += (mx - obj['x']) * 0.08
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if placing and 0 <= mx < WORLD_WIDTH and 0 <= my < TOP_HEIGHT:
                    dx = mx - place_start_x
                    speed = dx * 0.12
                    t = OBJECT_TYPES[selected_type_idx]
                    new_obj = {
                        'x': float(place_start_x),
                        'vx': float(speed),
                        'radius': float(t['radius']),
                        'mass': float(t['mass']),
                        'color': t['color'],
                        'id': t['id'],
                        'uid': new_uid(),
                        'material': t.get('material','metal')
                    }
                    objects.append(new_obj)
                placing = False
                dragging_idx = None
        elif event.type == pygame.MOUSEMOTION:
            if dragging_idx is not None and 0 <= mx < WORLD_WIDTH:
                obj = objects[dragging_idx]
                obj['x'] = float(mx)
                obj['vx'] = 0.0

    # update
    if playing or step_once:
        physics_update(dt / 16.0)
        step_once = False

    # draw
    screen.fill((18,20,24))
    draw_background()
    draw_objects()
    draw_particles(dt/60.0)
    draw_player_custom()
    rects = draw_menu(mouse_pos)

    # bottom panel
    info_panel = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT - TOP_HEIGHT))
    info_panel.fill((10,10,10))
    screen.blit(info_panel, (0, TOP_HEIGHT))
    info_text = f"Objects: {len(objects)}  | Selected: {OBJECT_TYPES[selected_type_idx]['name']} ({OBJECT_TYPES[selected_type_idx]['material']})  | Playing: {playing}  | Surface: {surface_keys[selected_surface_idx]}"
    t = font.render(info_text, True, (220,220,220))
    screen.blit(t, (12, TOP_HEIGHT + 12))
    if debug:
        dbg = font.render(f"FPS: {int(clock.get_fps())}", True, (200,200,200))
        screen.blit(dbg, (12, TOP_HEIGHT + 36))

    # placing preview
    if placing:
        px = place_start_x
        mx, my = pygame.mouse.get_pos()
        t = OBJECT_TYPES[selected_type_idx]
        pygame.draw.circle(screen, t['color'], (px, TOP_HEIGHT//2), int(t['radius']), 2)
        pygame.draw.line(screen, (220,220,220), (px, TOP_HEIGHT//2), (mx, TOP_HEIGHT//2), 2)

    pygame.display.flip()

pygame.quit()
sys.exit()
