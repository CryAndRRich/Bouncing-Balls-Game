# Bouncing Balls Game
This is a Python code for bouncing balls with an arc-shaped boundary
# Code Structure
The code is organized into three main parts:
* `Ball()` **class**:
This class represents a bouncing ball within the simulation
The constructor initializes a `Ball` object with the following attributes:
  + `pos`: The ball's position as a NumPy array (for efficient vector calculations)
  + `rad`: The ball's radius, a random value between 4.5 and 5.5
  + `vel`: The ball's velocity as a NumPy array, representing its direction and speed
  + `elastic`: The ball's elasticity (bounciness), a random value between 0.7 and 1 (higher values make the ball bounce more)
  + `mass`: The ball's mass, calculated based on its radius (larger radius implies higher mass)
  + `col`: The ball's color, a random triple of RGB values
  + `inside`: A boolean flag indicating whether the ball is currently inside the arc's boundary
* `gamePlay()` **class**:
This class manages the overall game logic and simulation aspects
  + initializes a `gamePlay` object with the following attributes:
  `circle_center`,`circle_radius`,`gravity`,`spinning_speed`,`arc_mass`,`arc_deg`,`start_angle`,`end_angle`,`ball_velocity`
  + `draw` **function**:
  Draws the arc boundary and balls onto the game window surface
    - Calculates arc endpoints based on `arc_deg`
    - Uses `pygame.draw.polygon()` to draw the arc in black
    - Iterates through `balls` and draws each one using `pygame.draw.circle()`
  + `check_inside` **function**:
  Checks if a ball's position is inside the arc's boundary
    - Calculates the angle corresponding to the ball's position
    - Compares this angle with the arc's start and end angles
    - Returns `True` if the ball's angle falls within the arc's range
  + `check_ball_collides_arc` **function**:
  Handles ball-arc collisions. Iterates through each ball:
    - Checks if the ball goes out of bounds and removes it if needed
    - Creates a new ball with random properties at the starting position
    - Updates ball's velocity with gravity
    - Calculates distance between ball and arc center
    - If the ball is outside the arc but was previously inside (based on `inside` flag), a collision is detected
    - Calculates the normal vector at the collision point if inside the arc
    - Updates `ball.pos` to the arc's edge
    - Calculates a new velocity considering the `arc_mass` and `spinning speed`
    - Applies `ball.elastic` to the new velocity
  + `check_ball_collides_ball`:
  Handles ball-ball collisions. Uses nested loops to compare each pair of balls:
    - Calculates the distance between ball centers
    - If the distance is less than the sum of their rads, a collision occurs
    - Calculates the normal vector at the collision point
    - Calculates the relative velocity of the balls along the normal vector
    - Applies the concept of `restitution` (bounciness) to update the `ball.vel` after the collision
    - Applies `ball.elastic` to the new velocities
* `Bouncing_Balls()` **class**:
  + Creates a `gamePlay` object to manage the simulation
  + Implements the main game loop:
    - Handles user events (like closing the window)
    - Updates the arc's starting and ending angles for rotation
    - Calls `check_collisions()` to handle collisions
    - Fills the background with black
    - Draws the arc using `pygame.draw.circle()`
    - Calls `draw()` to draw the balls
    - Updates the display and maintains the desired frame rate using `fpsClock.tick(FPS)`
# Potential Enhancements
If you want to create your own Bouncing Balls Game, try adding:
* **More Ball Types**: Introduce balls with varying sizes, masses, or shapes
* **Friction**: Implement friction to simulate energy loss and gradual slowing down
* **Multiple Arcs**: Create more complex boundaries with multiple arcs having different properties
* **User Interaction**: Allow users to control the simulation by adding/removing balls, changing gravity
* **Balls Sound**: Create a sound whenever collision occurs
