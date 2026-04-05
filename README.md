Project Name: Run Kitty Run
Game Type: Runner

=========================================
IMPORTANT NOTE REGARDING PROJECT LIBRARIES
=========================================
Due to severe and persistent technical issues with my local development environment, the Pygame Zero (pgzrun) library completely failed to run on my machine despite extensive troubleshooting. 

Rather than failing to deliver, I chose to build the entire project using the standard Pygame library. I have strictly adhered to all other project requirements, including writing my own Object-Oriented classes, implementing sprite animations, adding audio, and creating a fully functional state machine. I poured a lot of effort into this and hope this workaround is acceptable to demonstrate my skills.

=========================================

Libraries Used:
- pygame
- time (built-in Python library)

How to run the project:
1. Ensure you have Python installed on your system.
2. Open your terminal or command prompt.
3. Install the Pygame library by running: 
   pip install pygame
4. Open the project folder in your terminal.
5. Run the game by executing the main file: 
   python main.py

How to Play:
- Movement: Use the LEFT and RIGHT arrow keys to run.
- Jump: Press the UP arrow key or SPACEBAR to jump.
- Enemies: The Snail and Ladybug will alternate between a "walking" state and a "resting" state every 3 seconds.
- Combat: You can only defeat an enemy by jumping and landing directly on top of them (Mario-style) WHILE they are in their "walking" state. If you touch them from the side, or touch them while they are resting, you will be poisoned!
- Win Condition: You cannot leave the screen right away. You must successfully stomp both enemies, turning them into trophies, and THEN run through the right border of the screen to escape.
