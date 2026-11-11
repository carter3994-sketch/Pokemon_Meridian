"""Assemble GBA ground from the approved Landing Camp material swatches."""

from itertools import product

from PIL import Image, ImageDraw


PATH_CELLS = frozenset("=+A12345F")
TRAIL_JOIN_CELLS = PATH_CELLS | {"D"}


def apply_camp_terrain(art, grid, rows, materials):
    """Lay out walkable ground and return a lookup for the shared meadow tiles."""
    assert materials.mode == "P" and materials.size == (96, 32)
    width, height = len(rows[0]), len(rows)

    def texture_seed(x, y):
        return ((x+3)*73856093) ^ ((y+11)*19349663) ^ ((x+1)*(y+1)*83492791)

    def swatch(offset, x, y):
        left = offset + (x % 2) * 16
        top = (y % 2) * 16
        return materials.crop((left, top, left + 16, top + 16))

    for variant, y, x in product(range(2), repeat=3):
        name = f"meadow_{variant}{x}{y}"
        art[name] = swatch(variant*32, x, y)
        art[f"{name}_flowers"] = art[name].copy()
        draw = ImageDraw.Draw(art[f"{name}_flowers"])
        for px, py in ((5, 7), (8, 4), (11, 9)):
            draw.line((px - 2, py + 4, px, py), fill=1)
            draw.point((px - 1, py), fill=14)
            draw.point((px, py - 1), fill=15)
            draw.point((px + 1, py), fill=14)
            draw.point((px, py), fill=5)

    def meadow(x, y):
        seed = texture_seed(x, y)
        parity = (x+y) % 2
        # Favor shorter grass, with irregular pockets of full meadow clumps.
        variant = int((seed >> 9) % 7 < 5)
        name = f"meadow_{variant}{(seed >> 5) % 2}{parity}"
        if variant and (seed >> 13) % 37 == 0:
            name += "_flowers"
        return name

    def is_path(x, y):
        return 0 <= x < width and 0 <= y < height and rows[y][x] in TRAIL_JOIN_CELLS

    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            if cell in ".THMLSQR":
                grid[y][x] = meadow(x, y)
            if cell not in PATH_CELLS:
                continue

            # One rule per 8x8 quadrant. Diagonals distinguish an inside
            # bend from a filled intersection. Cardinal joins keep the
            # trail connected across each 16x16 metatile boundary.
            quarters = []
            for qy, qx in product(range(2), repeat=2):
                dx, dy = 2*qx-1, 2*qy-1
                vertical = is_path(x, y+dy)
                horizontal = is_path(x+dx, y)
                inside_bend = vertical and horizontal and not is_path(x+dx, y+dy)
                quarters.append((vertical, horizontal, inside_bend))

            phase = (texture_seed(x, y) >> 7) % 2, (x+y) % 2
            bits = "".join(str(int(value)) for quarter in quarters for value in quarter)
            name = f"trail_{phase[0]}{phase[1]}_{bits}"
            if name not in art:
                dirt = swatch(64, *phase)
                grass = swatch(32, *phase)
                rim = (2, 2, 3, 3, 3, 3, 2, 2) if phase[0] else (2, 3, 3, 4, 4, 3, 3, 2)
                for i, (vertical, horizontal, inside_bend) in enumerate(quarters):
                    qx, qy = i % 2, i // 2
                    for py, px in product(range(8), repeat=2):
                        # a and b increase from the outer corner inwards.
                        a = px if qx == 0 else 7-px
                        b = py if qy == 0 else 7-py
                        distance = 8
                        if not horizontal:
                            distance = min(distance, a-rim[b])
                        if not vertical:
                            distance = min(distance, b-rim[a])
                        if not vertical and not horizontal:
                            distance = min(distance, a+b-8)
                        if inside_bend:
                            distance = min(distance, a+b-4)

                        pos = qx*8+px, qy*8+py
                        if distance < 0:
                            green = grass.getpixel(pos)
                            dirt.putpixel(pos, 9 if distance == -1 and green != 1 else green)
                        elif distance == 0:
                            dirt.putpixel(pos, 11)
                        elif distance == 1 and (a+b) % 3 != 0:
                            dirt.putpixel(pos, 8)
                art[name] = dirt
            grid[y][x] = name
    return meadow
