# Landing Camp grid v0.3 — connectivity-checked engineering draft

**Not approved as final tilemap or implemented in engine.** Approved: visual v2 and broad layout v1. This is a proposed 48x40 metatile navigation sketch, with doors and major exits now marked.

```text
00 TTTTTTTTTTTTTTTTTTTT...5....TTT.TTT.TTTTTTTTTTTT
01 TTTTTTTTTTTTTTTTTTTT........TTT.TTT.TTTTTTTTTTTT
02 TTTTTTTTTTTTTTTTTTTT........TTT.TTT.TTTTTTTTTTT^
03 TTTTTTTTTTTTTTTTTTTT............TTT.^TTTTTTTTTT^
04 TTTTTTTTTTTTTTTTTTTT...========4TTT.^^TTTTTTT^^^
05 TTTTTTTTTTTTTTTTTTTT...==...........^^^^^TTT^^^^
06 TTTTTTTTT..............==HHHHHHHHH..^^^^^^^^^^^^
07 TTTTTTTTTTTT..LLLLLLLL.==HHHHHHHHH..^^^~~^CCCCC^
08 TTTTTTTTTTTT..LLLLLLLL.==HHHHHHHHH..^^~~~^CCCCC^
09 TTTTTTTTTTTT..LLLLLLLL.==HHHHHHHHH..^^~~~^CCCCC^
10 TTTTTTTTTTTT..LLLLLLLL.==HHH+HHHHH..^^^~~===3CC^
11 TTTTTTTTTTTT..LLLL+LLL.==..==.......^^^^^=====^^
12 TTTTTTTT========================SSSS=^^^^==^^^^^
13 ........========================SSSS=^^^^==^^^^^
14 ~~~~~~~~~~~............==..==...SS+S=^^^^==^^^^^
15 ~~~~~~~~~~~......MMM...==.============~~~===....
16 ~~~~~~~~~~~......MMM...==.=====....===~~~====...
17 ~~~~~~D~~~~......M+M...=====F===...==..~~.......
18 ~~DDDDDDDDDDD~....=============....==...~.......
19 ~~DDDDDDDDDDD~===========.=====....==...........
20 ~~DDDDDDDDDDD============..============.........
21 ~~~~~~~~~~~~~============..==......==...........
22 ~~~~~~~~~~~.=========================QQQ........
23 ~~~~~~~~~~~.A========================Q+Q.=......
24 ~~~~~~~~~~~............==...============........
25 ~~~~~~~~~~~............==..........==...........
26 ~~~~~~~~~~~~...........==..........==...........
27 ~~~~~~~~~~~~...........==..........==...........
28 ~~~~~~~~~~~~~..........======================...
29 ~~~~~~~~~~~~~..........=====================2...
30 ~~~~~~~~~~~~~..........==.............TTTTTTTTTT
31 ~~~~~~~~~~~~...........==.............TTTTTTTTTT
32 ~~~~~~~~~~~~...........==.............TTTTTTTTTT
33 ~~~~~~~~~~~...TTTTTTT..==.............TTTTTTTTTT
34 ~~~~~~~~~~~...TTTTTTT..==.............TTTTTTTTTT
35 ~~~~~~~~~~....TTTTTTT..==.............TTTTTTTTTT
36 ~~~~~~~~~~....TTTTTTT..==.............TTTTTTTTTT
37 ~~~~~~~~~~....TTTTTTT..==.............TTTTTTTTTT
38 ~~~~~~~~~~~...TTTTTTT..==.............TTTTTTTTTT
39 ~~~~~~~~~~~...TTTTTTT..1=.............TTTTTTTTTT
```

## Legend and coordinate contract
Coordinates zero-based (x,y), x across 0..47, y down 0..39. Each row has 48 cells.
- Walkable planning cells: `.` ground, `=` dirt road, `D` dock, `+` door, `A` arrival, `F` campfire, `1`–`5` exits/gates.
- Blocked planning cells: `M` medical, `L` lab, `H` HQ, `S` supply, `Q` quarters, `R` ruins, `C` cave, `T` forest, `^` cliff, `~` water.
- Door coordinates: medical (18,17), lab (18,11), HQ (28,10), supply (34,14), quarters (38,23).
- Arrival (12,23); campfire (28,17); main forest exit (23,39); coast (44,29); cave (44,10); northern trail to the ruins (31,4); north trail (23,0).

## Automated abstract connectivity validation
A four-neighbor flood fill from arrival (12,23) treating ground, road, dock, doors, and marked gates as walkable reached **all 10 listed entrances/exits**: (18,17), (18,11), (28,10), (34,14), (38,23), (23,39), (44,29), (44,10), (31,4), (23,0). This is a test of the **text sketch only**, not GBA tile collision or warp behavior.

## Remaining engineering and approval requirements
1. Convert rough rectangular building footprints into actual tilesets, doors, ramps, coast and cliffs.
2. Validate elevations, metatile behavior, collision and warp destinations in-game; gated exits must not be freely traversable before story unlock.
3. Design actual neighboring maps for the forest/coast/cave/north/ruins connections.
4. Present a visually legible accurate map for the user's explicit exact-layout approval; the schematic alone is not a final approval request.
5. Settlement phase 1/2/3 transformations remain separately approval-gated.

## Implemented settlement arrangement update
The lab is north of medical, both west of HQ. The fire clearing faces HQ; supply and living quarters form the eastern cluster. These coordinates drive the native art, collision export and paired warps. The whole camp composition and waterfront still require reconstruction against the approved artwork.
