# Landing Camp grid v0.3 — connectivity-checked engineering draft

**Not approved as final tilemap or implemented in engine.** Approved: visual v2 and broad layout v1. This is a proposed 48x40 metatile navigation sketch, with doors and major exits now marked.

```text
00 TTTTTTTTTTTTTTTTTTTT...5.....RRRRRR.^^^^^^^^^^^^
01 TTTTTTTTTTTTTTTTTTTT.........RRRRRR.^^^^^^^^^^^^
02 TTTTTTTTTTTTTTTTTTTT.........RRRRRR.^^^^^^^^^^^^
03 TTTTTTTTTTTTTTTTTTTT.........RRRRRR.^^^^^^^^^^^^
04 TTTTTTTTTTTTTTTTTTTT...========4RRR.^^^^^^^^^^^^
05 TTTTTTTTTTTTTTTTTTTT...==...........^^^^^^^^^^^^
06 TTTTTTTTT..............==HHHHHHHHH..^^^^^^^^^^^^
07 TTTTMMMMMMMM..LLLLLLLL.==HHHHHHHHH..^^^^^^CCCCC^
08 TTTTMMMMMMMM..LLLLLLLL.==HHHHHHHHH..^^^^^^CCCCC^
09 TTTTMMMMMMMM..LLLLLLLL.==HHHHHHHHH..^^^^^^CCCCC^
10 TTTTMMMMMMMM..LLLLLLLL.==HHH+HHHHH..^^^^^===3CC^
11 TTTTMMMM+MMM..LLLL+LLL.==...=.......^^^^^===CCC^
12 TTTTTTTT=============================^^^^=^^^^^^
13 ........=============================^^^^=^^^^^^
14 ~~~~~~~~~~~............==..........==^^^^=^^^^^^
15 ~~~~~~~~~~~............==..........=======......
16 ~~~~~~~~~~~............==..........=======......
17 ~~~~~~~~~~~............==..........==...........
18 ~~DDDDDDDDDDD~.........==..........==.SSSSSSSS..
19 ~~DDDDDDDDDDD~...========..........==.SSSSSSSS..
20 ~~DDDDDDDDDDD======F=====..........==.SSSSSSSS..
21 ~~~~~~~~~~~~~============..........==.SSSSSSSS..
22 ~~~~~~~~~~~.=========================.SSS+SSSS..
23 ~~~~~~~~~~~.A========================....=......
24 ~~~~~~~~~~~............==..........==.QQQQQQQQ..
25 ~~~~~~~~~~~............==..........==.QQQQQQQQ..
26 ~~~~~~~~~~~............==..........==.QQQQQQQQ..
27 ~~~~~~~~~~~............==..........==.QQQ+QQQQ..
28 ~~~~~~~~~~~............======================...
29 ~~~~~~~~~~~............=====================2...
30 ~~~~~~~~~~~............==.............TTTTTTTTTT
31 ~~~~~~~~~~~............==.............TTTTTTTTTT
32 ~~~~~~~~~~~............==.............TTTTTTTTTT
33 ~~~~~~~~~~~...TTTTTTT..==.............TTTTTTTTTT
34 ~~~~~~~~~~~...TTTTTTT..==.............TTTTTTTTTT
35 ~~~~~~~~~~~...TTTTTTT..==.............TTTTTTTTTT
36 ~~~~~~~~~~~...TTTTTTT..==.............TTTTTTTTTT
37 ~~~~~~~~~~~...TTTTTTT..==.............TTTTTTTTTT
38 ~~~~~~~~~~~...TTTTTTT..==.............TTTTTTTTTT
39 ~~~~~~~~~~~...TTTTTTT..1=.............TTTTTTTTTT
```

## Legend and coordinate contract
Coordinates zero-based (x,y), x across 0..47, y down 0..39. Each row has 48 cells.
- Walkable planning cells: `.` ground, `=` dirt road, `D` dock, `+` door, `A` arrival, `F` campfire, `1`–`5` exits/gates.
- Blocked planning cells: `M` medical, `L` lab, `H` HQ, `S` supply, `Q` quarters, `R` ruins, `C` cave, `T` forest, `^` cliff, `~` water.
- Door coordinates: medical (8,11), lab (18,11), HQ (28,10), supply (41,22), quarters (41,27).
- Arrival (12,23); campfire (19,20); main forest exit (23,39); coast (44,29); cave (44,10); ruins gate (31,4); north trail (23,0).

## Automated abstract connectivity validation
A four-neighbor flood fill from arrival (12,23) treating ground, road, dock, doors, and marked gates as walkable reached **all 10 listed entrances/exits**: (8,11), (18,11), (28,10), (41,22), (41,27), (23,39), (44,29), (44,10), (31,4), (23,0). This is a test of the **text sketch only**, not GBA tile collision or warp behavior.

## Remaining engineering and approval requirements
1. Convert rough rectangular building footprints into actual tilesets, doors, ramps, coast and cliffs.
2. Validate elevations, metatile behavior, collision and warp destinations in-game; gated exits must not be freely traversable before story unlock.
3. Design actual neighboring maps for the forest/coast/cave/north/ruins connections.
4. Present a visually legible accurate map for the user's explicit exact-layout approval; the schematic alone is not a final approval request.
5. Settlement phase 1/2/3 transformations remain separately approval-gated.
