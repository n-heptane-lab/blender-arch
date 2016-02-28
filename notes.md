generating the arch is trickier than it seems at first. We need to create all the bars, all the physics objects that link them together, and get everything in the correct positions.

Each bar has three connecting points. Each end join has 4 connecting
points.

The end connection point for a bar is dependent on the width of the bar -- it is not exactly at the end.

We also need to figure out the initial configuration for generating the structure. Fully deployed seems sensible.

Do we generate the bar and then apply rotation? Or generate it already rotated?

The connector also has size to be accounted for.

