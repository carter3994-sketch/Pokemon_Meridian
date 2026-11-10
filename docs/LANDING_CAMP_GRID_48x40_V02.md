# Landing Camp exact-grid candidate v0.2 (48x40)

**UNAPPROVED ENGINEERING SKETCH.** Every character is a proposed metatile classification, not final game tiles, collision or actual asset art. Visual v2 and broad layout v1 are approved. No playable map is built yet.

Coordinates: x=0..47 left-to-right, y=0..39 top-to-bottom. Rows are numbered; each row contains 48 characters.

```text
   000000000011111111112222222222333333333344444444
   012345678901234567890123456789012345678901234567
00 TTTTTTTTTTTTTTTTTTTTT.............^^^^^^^^^^^^^^
01 TTTTTTTTTTTTTTTTTTTTT...5.........^^^^^^^^^^^^^^
02 TTTTTTTTTTTTTTTTTTTTT........RRRRR^^^^^^^^^^^^^^
03 TTTTTTTTTTTTTTTTTTTTT........RR4RR^^^^^^^^^^^^^^
04 TTTTTTTTTTTTTTTTTTTTT........RRRRR^^^^^^^^^^^^^^
05 TTTTTTTTTTTTTTTTTTTTT.HHHHHHHRRRRR^^^^^^^^^^^^^^
06 TTTTTTTTT.............HHHHHHHHHH..^^^^^^^^^^^^^^
07 TTTTMMMMMMMM.LLLLLLLL.HHHHHHHHHH..^^^^^^^^^^^^^^
08 TTTTMMMMMMMM.LLLLLLLL.HHHHHHHHHH......^^^^CCCCC^
09 TTTTMMMMMMMM.LLLLLLLL.HHHHHHHHHH......^^^^CCCCC^
10 ....MMMMMMMM.LLLLLLLL.HHHHHHHHHH......^^^^CCC3C^
11 ....MMMMMMMM.LLLLLLLL..==.............^^^^CCCCC^
12 ....MMMMMMMM.LLLLLLLL..================^^^^^^^^^
13 .......................================^^^^^^^^^
14 ~~~~~~~~~~~............==..........==.^^^^^^^^^^
15 ~~~~~~~~~~~............==..........==.^^^^^^^^^^
16 ~~~~~~~~~~~............==..........==.^^^^^^^^^^
17 ~~~~~~~~~~~:::.........==..........==...........
18 ~~DDDDDDDDDDD:...PPPPPP==.........SSSSSSSSSS....
19 ~~DDDDDDDDDDD:...PPPPPP==.........SSSSSSSSSS....
20 ~~DDDDDDDDDDD:...PPPPPPF=.........SSSSSSSSSS....
21 ~~~~~~~~~~~:::...PPPPPP==.........SSSSSSSSSS....
22 ~~~~~~~~~~~:=============.........SSSSSSSSSS....
23 ~~~~~~~~~~~:A========================...........
24 ~~~~~~~~~~~:::======================QQQQQQQQQ...
25 ~~~~~~~~~~~:::===......==..........=QQQQQQQQQ...
26 ~~~~~~~~~~~:::.........==..........=QQQQQQQQQ...
27 ~~~~~~~~~~~:::.........==..........=QQQQQQQQQ...
28 ~~~~~~~~~~~:::.........==...........QQQQQQQQQ...
29 ~~~~~~~~~~~............=====================....
30 ~~~~~~~~~~~~~~.........=====================TTTT
31 ~~~~~~~~~~~~~~.........==............TTTTTTTTTTT
32 ~~~~~~~~~~~~~~.........==............TTTTTTTTTTT
33 ~~~~~~~~~~~~~~.........==............TTTTTTTTTTT
34 ~~~~~~~~~~~~~~.........==............TTTTTTTT2TT
35 ~~~~~~~~~~~~~~.........==............TTTTTTTTTTT
36 ~~~~~~~~~~~~~~.........==............TTTTTTTTTTT
37 ~~~~~~~~~~~~~~.........==............TTTTTTTTTTT
38 ~~~~~~~~~~~~~~.......................TTTTTTTTTTT
39 ~~~~~~~~~~~~~~.........1.............TTTTTTTTTTT
```

## Legend
- `.` proposed walkable natural terrain; `=` two-tile-wide or wider dirt roads; `T` forest; `~` water; `:` shore; `^` cliffs.
- `D` dock, `M` medical, `L` lab, `H` HQ, `S` supply, `Q` quarters, `R` ruins, `C` cave, `P` central plaza.
- `F` campfire landmark; `A` arrival point; `1` main forest exit, `2` coastal exit, `3` cave entrance, `4` ruins approach, `5` northern trail.
- Buildings currently occupy rough rectangular footprints; **doors, walls, shoreline collision, cliffs, height, and warp activation cells are not yet drawn**. Their absence is intentional, not a claim that this grid is playable.

## Issues to resolve before approval and implementation
1. The proposed dock at x2..12 y18..20 currently crosses water/shore; refine pier shape and elevation to ensure valid access.
2. Exact building door cells and approaches require GBA tileset review.
3. The forest exit at (23,39) and coastal exit at (45,34) need compatible neighboring route maps.
4. Ruins/cave restrictions must be represented as event gates, not unexplainable impassable terrain.
5. Verify all major roads and optional loops remain connected once solid building collisions are placed.
6. Present revised actual art and precise collision/warp plan to the user for approval. Do not implement final map visuals prematurely.

## Time progression
The map is the Arrival phase only. Later growth phases require separately approved changed map visuals and consistent save flags.
