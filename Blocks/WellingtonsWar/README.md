# Description

The files here are for the game "Wellington's War" from Pacific Rim Publishing.

# BGG

For more information please see https://boardgamegeek.com/boardgame/28920/wellingtons-war-peninsular-campaign-1809-1814

# Naming Convention

Each file is given a unique name, typically by including a unit's designation (if any) and nationality (if appropriate). This is mostly done for the sake of Vassal, which requires unique filenames.

# Vassal and Batik

The Vassal application currently uses the Batik SVG rendering engine. While this mostly works, there are a few properties that it does not support. Namely, it does not support `dominant-baseline` or `alignment-baseline`. This effectively means that vertical alignment will have to be done manually via y-coordinates.

# Recreations vs Improvements

The images in the base directory are faithful recreations of the physical blocks. Unfortunately the layout of the blocks in the physical game are generally bland, especially the French. In addition, using black text for the French, British and Portuguese blocks was a mistake since it is quite difficult to read, both in real life and on a computer screen.

Consequently the blocks that I plan to use in the Vassal module include minor improvements, like white text instead of black for every side, except the Spanish, since the black contrasts nicely against the yellow background. In addition, I can see no benefit to including setup information on the blocks themselves (I'll create a separate player aid), and movement ratings will be given some color to distinguish them from other values.
