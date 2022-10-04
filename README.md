<h1>Install package dependencies</h1>

<p>Make sure that you have installed Pip on your machine.</p>
<p>Run this command on your bash to install all dependencies: <b>pip install -r requirements.txt</b></p>

<h1>Purpose</h1>
<p>Display a demo insometric map on the screen</p>

<h1>Module explanation</h1>

<h2>1. Entry file main.py</h2>
<p>Define a principle logic flow of project</p>

<h2>2. module game/game.py</h2>
<p>game.py create a game loop function that be called in main.py: Draw -> Event handling -> Update State (ex: update state of the building burned down or not)</p>

<h2>3. module world.py</h2>
<p><b>Role</b>: Export class World that be used in module game.py</p>

<h3>Function in module world.py</h3>

<h4>3.1 create_cartesian_world</h4>
<p>Return a 2 dim array in which each cell contains 4 cartesian coordinations (x, y) pairs of 4 vertices of a square cell of size TILE_SIZE x TILE_SIZE (TILE_SIZE defined in setting.py module)</p>

<h4>3.2 cartesian_cell</h4>
<p>Return an array of 4 cartesian coordinations pair of 4 vertices of a square cell. This function is used in create_cartesian_world</p>

<p><b>Note</b>: to print the square cell on a screen we just have to have one cartesian coordination pair of the first vertice. But to draw a Polygone in our case is Rhombus we must have 4 coordinations. Refer this docs -> https://www.pygame.org/docs/ref/draw.html#pygame.draw.polygon </p>

<h4>3.3 isometric_cell</h4>
<p>Return a dictionary that contains an array of 4 cartesian coordinations pair of 4 vertices of a rhombus and a position of the point where we the image be filled in. This function is used in create_isometric_world</p>

<h4>3.4 create_isometric_world</h4>
<p>Return a 2 dim array in which each cell contains 4 cartesian coordinations (x, y) pairs of 4 vertices of a rhombus of size 2xTILE_SIZE x TILE_SIZE (TILE_SIZE defined in setting.py module)</p>

<h4>3.5 load_images</h4>
<p>Return an image loaded from assets/graphics directory</p>





