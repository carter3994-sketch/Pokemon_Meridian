"""Compose seamless animated water from the Landing Camp source art."""

from PIL import Image, ImageDraw


FRAME_COUNT = 8
FRAMES_PER_STEP = 8
SWELL = (0, 1, 2, 3, 3, 2, 1, 0)


def metatile(image, x, y):
    return image.crop((x*16, y*16, x*16+16, y*16+16))


# A shared palette for water, wet stone and the cascade. The open sea
# uses the darker blue ramp, leaving white and mint for breaking foam.
WATER_COLORS = (
    (0,0,0), (232,247,244), (150,163,104), (155,221,228),
    (83,182,202), (119,115,110), (66,153,199), (53,133,184),
    (71,72,88), (43,116,175), (36,104,168), (32,98,161),
    (54,146,178), (30,93,157), (28,89,151), (24,75,135),
)
SHORE_STEPS = (0,0,1,1,2,2,1,0)
BANKS = ((0,-1),(1,0),(0,1),(-1,0))


def ocean_frame(step):
    """Draw broad, low-contrast swells with short traveling crests."""
    frame = Image.new("P",(32,32),11)
    frame.putpalette([channel for rgb in WATER_COLORS for channel in rgb])
    for y in range(32):
        for x in range(32):
            band = (y + (x//4) + step) % 8
            if band < 2:
                frame.putpixel((x,y),13)
            elif band == 2:
                frame.putpixel((x,y),10)
    for i,(x,y,width) in enumerate(((1,4,7),(18,2,6),(9,13,8),(25,20,6),(3,24,6),(18,28,9))):
        phase = (step+i*3)%FRAME_COUNT
        left = x + SWELL[phase]
        height = y + (2 <= phase <= 5)
        for offset in range(width):
            px = (left+offset)%32
            py = (height + (offset < 2) - (offset == width-1))%32
            color = 9 if offset in (0,width-1) else 7
            if 2 <= phase <= 5 and width//2-1 <= offset <= width//2:
                color = 6
            frame.putpixel((px,py),color)
    return frame


def shore_frame(ocean, banks, corners, rock, step):
    """Join all bank edges around a water cell, including diagonal corners."""
    frame = ocean.copy()
    for y in range(16):
        for x in range(16):
            edges = (y,15-x,15-y,x)
            axes = (x,y,x,y)
            distance = min((edges[i] - (axes[i] in (5,6,12,13)) for i in banks),
                           default=16)
            for i in corners:
                distance = min(distance,edges[i]+edges[(i+1)%4]+2)
            if distance >= 9:
                continue
            sweep = (x*3+y*5)%9
            foam = (4 if rock else 2) + SHORE_STEPS[(step+sweep//3)%8]
            if rock and distance <= 3:
                color = 2 if distance <= 0 and sweep < 6 else (8 if distance == 3 or sweep < 3 else 5)
            elif distance == foam and sweep != 4:
                color = 1 if rock and sweep < 4 else 3
            elif distance <= foam:
                color = 4
            else:
                color = 12 if distance < 8 else 9
            frame.putpixel((x,y),color)
    return frame


def waterfall_frame(source, step):
    """Send narrow light bands down the stream and outward in the splash."""
    frame = source.copy()
    lighter = {3:1, 4:3, 6:4, 7:6, 9:7, 10:7, 11:9, 12:9, 13:10, 14:10}
    for y in range(source.height):
        for x in range(source.width):
            pixel = source.getpixel((x,y))
            if pixel not in lighter and pixel != 1:
                continue
            if y < 47:
                phase = (y - 3*step + (x//3)*5) % 24
                active = phase < 7
                receding = phase >= 19
            else:
                phase = (abs(x-16) + abs(y-50) - 2*step) % 16
                active = phase < 4
                receding = phase >= 12
            if active:
                frame.putpixel((x,y),lighter.get(pixel,pixel))
            elif receding and pixel in (1,3):
                frame.putpixel((x,y),3 if pixel == 1 else 4)
    return frame


def reef_foam(frame, step):
    """Pull the foam line out from the rock as the swell crests."""
    frame = frame.copy()
    draw = ImageDraw.Draw(frame)
    inset = (0,0,1,1,1,0,0,0)[step]
    draw.arc((1+inset,5+inset,15-inset,15),15,165,fill=3)
    draw.point((4+inset,14),fill=1 if step < 5 else 3)
    draw.point((12-inset,14),fill=1 if step < 5 else 3)
    return frame


def build_water_frames(assets, reefs, rows):
    """Return animated source metatiles, including the water beneath the pier."""
    falls = Image.open(assets/"env_waterfall.png")
    falls.putpalette([channel for rgb in WATER_COLORS for channel in rgb])
    frames = {}
    oceans = [ocean_frame(i) for i in range(FRAME_COUNT)]
    for phase in range(4):
        frames[f"env_ocean_{phase}"] = [metatile(frame,phase%2,phase//2) for frame in oceans]
    for name,x,y in reefs:
        phase = x%2+2*(y%2)
        frames[f"{name}_foam"] = [
            reef_foam(frame,i) for i,frame in enumerate(frames[f"env_ocean_{phase}"])
        ]

    width,height = len(rows[0]),len(rows)
    shore_names = {}
    def land(x,y):
        return 0 <= x < width and 0 <= y < height and rows[y][x] not in "~D"

    for y,row in enumerate(rows):
        for x,cell in enumerate(row):
            if cell != "~":
                continue
            banks = tuple(i for i,(dx,dy) in enumerate(BANKS) if land(x+dx,y+dy))
            corners = []
            for i,(dx,dy) in enumerate(BANKS):
                j = (i+1)%4
                sx,sy = BANKS[j]
                if i not in banks and j not in banks and land(x+dx+sx,y+dy+sy):
                    corners.append(i)
            if not banks and not corners:
                continue
            rock = x < 20
            phase = x%2+2*(y%2)
            name = f"env_waterbank_{int(rock)}_{phase}_{''.join(map(str,banks))}_{''.join(map(str,corners))}"
            if name not in frames:
                frames[name] = [shore_frame(frame,banks,corners,rock,i)
                                for i,frame in enumerate(frames[f"env_ocean_{phase}"])]
            shore_names[x,y] = name

    waterfall = [waterfall_frame(falls,i) for i in range(FRAME_COUNT)]
    for y in range(falls.height//16):
        for x in range(falls.width//16):
            frames[f"env_waterfall_{x}_{y}"] = [metatile(frame,x,y) for frame in waterfall]
    return frames,shore_names
