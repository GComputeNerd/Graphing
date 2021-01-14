![Sample Image](header.png)

# Graphing

This is a simple graphing calculator I made with PyCairo. I plan on making upgrades later. For now, it graphs functions of the form y=f(x) .

To graph functions. First make a CoordinateGrid object.

```
cg = cairofunctions.CoordinateGrid(cairo_context, image_width, image_height, tuple(ORIGIN), unit, pixel_unit)

# unit <- magnitude of 1 unit on X and Y axis
# pixel_unit <- How many pixels are 1 unit

cg.DrawAxes() # Draws axes
cg.DrawGridMarks() # Draws Grid Marks
cg.PlotFunc(lambda_function, xmin, xmax)
```

Very barebones at the moment.
