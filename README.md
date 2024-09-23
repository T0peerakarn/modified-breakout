# Modified Breakout

## Overview

A Breakout game developed in Pygame. Players control a paddle to bounce a ball and break bricks, but now they have access to power-ups and an ultimate mode that elevates the experience.

## Items

### Multiple Item

A **Multiple Item** multiplies the number of balls by 3, so that for each ball, two additional balls come out at random angles relative to the original one.

The speed of the new ball can be calculated by the following formula:

$$
\begin{bmatrix}
dx' & dy'
\end{bmatrix}
\=
\begin{bmatrix}
dx & dy
\end{bmatrix}
\begin{bmatrix}
\cos(\theta) & -\sin(\theta) \\
\sin(\theta) & \cos(\theta)
\end{bmatrix}
$$

where

- $\theta$ be the angle of the new balls with respect to the original one.
- $dx$ be the speed in x-axis of the original ball
- $dy$ be the speed in y-axis of the original ball
- $dx'$ be the speed in x-axis of the new ball
- $dy'$ be the speed in y-axis of the new ball

Moreover, after the Multiplier Item is used, the speed of the ball slightly increases and gradually decelerates to the normal speed to enhance the user experience.

### Disperse Item

Unfortunately, there is a chance that after the new balls emerge from the Multiplier Item, their speed on the y-axis will be very low, causing the balls to move horizontally indefinitely and preventing the game from continuing. To address this situation, logic has been implemented to generate a **Disperse Item** in front of the stuck ball, which will assign random speeds to both the x-axis and y-axis for all balls.

### Heart Item

The player has a maximum of 3 health points, which decrease when all the balls fall. The only way to increase health is by collecting the **Heart Item**, which will restore 1 health point to the player.

## Ultimate Mode

By pressing **'X'** on the keyboard, every ball will turn into ultimate mode, transforming into a flashing color ball that can break any brick in one hit, earning 2000 points for each brick. However, there is a very limited time for which ultimate mode is active, and the player must pay 10,000 points to activate it.

## Tools

- **Python**: The programming language used to implement the system.
- **Pygame**: A Python library used for creating the game
