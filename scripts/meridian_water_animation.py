"""Compose seamless animated water from the Landing Camp source art."""

from PIL import Image, ImageDraw


FRAME_COUNT = 8
FRAMES_PER_STEP = 8
SWELL = (0, 1, 2, 3, 3, 2, 1, 0)


def metatile(image, x, y):
    return image.crop((x*16, y*16, x*16+16, y*16+16))


def ocean_frame(source, step):
    """Move sparse curved wavelets over the deep blue water texture."""
    frame = source.copy()
    crests = ((2,5,5), (19,1,5), (11,14,7), (27,19,5), (3,24,6), (22,29,7))
    for i, (x, y, width) in enumerate(crests):
        phase = (step + i*3) % FRAME_COUNT
        left = x + SWELL[phase]
        height = y + (1 if 2 <= phase <= 5 else 0)
        for offset in range(width):
            px = (left+offset) % source.width
            py = (height + (offset in (0,width-1))) % source.height
            light = 6 if 2 <= phase <= 5 and 1 <= offset < width-1 else 7
            if light == 6 and offset == width//2 and phase in (3,4):
                light = 4
            frame.putpixel((px,py),light)
            if light == 6 and offset == width//2:
                frame.putpixel((px,(py+1) % source.height),7)
    return frame


def shore_frame(source, step):
    """Slide the existing foam along the shore and let the wash recede."""
    frame = source.copy()
    water = {1,3,4,6,7,9,10,11,12,13,14}
    for y in range(8,source.height):
        for x in range(source.width):
            old = source.getpixel((x,y))
            if old not in water:
                continue
            sample_y = y
            if y >= 11 and 2 <= step <= 5:
                sample_y = y-1
            color = source.getpixel(((x+SWELL[step]) % source.width,sample_y))
            if color in water:
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


def build_water_frames(assets, reefs):
    """Return animated source metatiles, including the water beneath the pier."""
    ocean = Image.open(assets/"env_ocean.png")
    shore = Image.open(assets/"env_shore.png")
    falls = Image.open(assets/"env_waterfall.png")
    # The environment sprite's index zero is the opaque backing color.
    for image in (shore, falls):
        image.putdata([15 if value == 0 else value for value in image.getdata()])
    frames = {}
    oceans = [ocean_frame(ocean,i) for i in range(FRAME_COUNT)]
    for phase in range(4):
        frames[f"env_ocean_{phase}"] = [metatile(frame,phase%2,phase//2) for frame in oceans]
    for name, x, y in reefs:
        phase = x%2+2*(y%2)
        frames[f"{name}_foam"] = [
            reef_foam(frame,i) for i,frame in enumerate(frames[f"env_ocean_{phase}"])
        ]

    shores = [shore_frame(shore,i) for i in range(FRAME_COUNT)]
    directions = (
        ("north",None,Image.Transpose.FLIP_LEFT_RIGHT),
        ("south",Image.Transpose.ROTATE_180,Image.Transpose.FLIP_LEFT_RIGHT),
        ("east",Image.Transpose.ROTATE_270,Image.Transpose.FLIP_TOP_BOTTOM),
        ("west",Image.Transpose.ROTATE_90,Image.Transpose.FLIP_TOP_BOTTOM),
    )
    for direction, rotation, flip in directions:
        name = f"env_shore_{direction}"
        frames[name] = [frame if rotation is None else frame.transpose(rotation) for frame in shores]
        frames[name+"_alt"] = [frame.transpose(flip) for frame in frames[name]]

    waterfall = [waterfall_frame(falls,i) for i in range(FRAME_COUNT)]
    for y in range(falls.height//16):
        for x in range(falls.width//16):
            frames[f"env_waterfall_{x}_{y}"] = [metatile(frame,x,y) for frame in waterfall]
    return frames
