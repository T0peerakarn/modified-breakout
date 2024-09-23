import random, pygame, sys
from src.states.BaseState import BaseState
from src.constants import *
from src.Dependency import *
import src.CommonRender as CommonRender
import math

class PlayState(BaseState):
    def __init__(self):
        super(PlayState, self).__init__()
        self.paused = False

    def Enter(self, params):
        self.paddle = params['paddle']
        self.bricks = params['bricks']
        self.health = params['health']
        self.score = params['score']
        self.high_scores = params['high_scores']
        self.balls = params['balls']
        self.level = params['level']

        self.balls[0].dx = random.randint(-600, 600)  # -200 200
        self.balls[0].dy = random.randint(-180, -150)

        self.stuckBall = None
        self.stuckBallTimer = 250
        self.disperseItem = None

        self.initial_skin = params['initial_skin']
        self.ultimateTimer = 0

    def update(self,  dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                    gSounds['pause'].play()
                    #music_channel.play(sounds_list['pause'])
                if event.key == pygame.K_x and self.score >= 10000:
                    self.ultimateTimer = 150
                    self.score -= 10000
                    gSounds['ultimate'].play()

        if self.paused:
            return

        self.paddle.update(dt)
        
        for i, ball in enumerate(self.balls):

            ball.update(dt)

            if self.ultimateTimer > 0:
                ball.image = ball_image_list[random.randint(0, 6)]
            else:
                ball.image = ball_image_list[self.initial_skin]
               
            if self.stuckBall == None and math.fabs(ball.dy) <= 30:
                self.stuckBall = id(ball)
            
            if ball.Collides(self.paddle):
                # raise ball above paddle
                ####can be fixed to make it natural####
                ball.rect.y = self.paddle.rect.y - 24
                ball.dy = -ball.dy

                # half left hit while moving left (side attack) the more side, the faster
                if ball.rect.x + ball.rect.width < self.paddle.rect.x + (self.paddle.width / 2) and self.paddle.dx < 0:
                    ball.dx = -150 + -(8 * (self.paddle.rect.x + self.paddle.width / 2 - ball.rect.x))
                # right paddle and moving right (side attack)
                elif ball.rect.x > self.paddle.rect.x + (self.paddle.width / 2) and self.paddle.dx > 0:
                    ball.dx = 150 + (8 * abs(self.paddle.rect.x + self.paddle.width / 2 - ball.rect.x))
                gSounds['paddle-hit'].play()

            for k, brick in enumerate(self.bricks):

                if brick.alive and ball.Collides(brick):

                    if self.ultimateTimer > 0:
                        self.score += 2000
                        brick.Break()
                    else:
                        self.score = self.score + (brick.tier * 200 + brick.color * 25)
                        brick.Hit()

                        # hit brick from left while moving right -> x flip
                        if ball.rect.x + 6 < brick.rect.x and ball.dx > 0:
                            ball.dx = -ball.dx
                            ball.rect.x = brick.rect.x - 24

                        # hit brick from right while moving left -> x flip
                        elif ball.rect.x + 18 > brick.rect.x + brick.width and ball.dx < 0:
                            ball.dx = -ball.dx
                            ball.rect.x = brick.rect.x + 96

                        # hit from above -> y flip
                        elif ball.rect.y < brick.rect.y:
                            ball.dy = -ball.dy
                            ball.rect.y = brick.rect.y - 24

                        # hit from bottom -> y flip
                        else:
                            ball.dy = -ball.dy
                            ball.rect.y = brick.rect.y + 48

                    if self.CheckVictory():
                        gSounds['victory'].play()

                        g_state_manager.Change('victory', {
                            'level':self.level,
                            'paddle':self.paddle,
                            'health':self.health,
                            'score':self.score,
                            'high_scores':self.high_scores,
                        })

                    # whenever hit, speed is slightly increase, maximum is 450
                    if abs(ball.dy) < 450:
                        ball.dy = ball.dy * 1.02

                    break

            if ball.rect.y >= HEIGHT:
                self.balls.pop(i)

                if len(self.balls) == 0:
                    self.health -= 1
                    gSounds['hurt'].play()
                
                    if self.health == 0:
                        g_state_manager.Change('game-over', {
                            'score':self.score,
                            'high_scores': self.high_scores
                        })
                    else:
                        g_state_manager.Change('serve', {
                            'level': self.level,
                            'paddle': self.paddle,
                            'bricks': self.bricks,
                            'health': self.health,
                            'score': self.score,
                            'high_scores': self.high_scores,
                        })
        
        for brick in self.bricks:
            if not brick.alive and brick.reward != None:
                brick.reward.update(dt)

                if brick.reward.Collides(self.paddle):

                    if brick.reward.itemType == ITEM_MULTIPLE:
                        nBalls = len(self.balls)
                        for i in range(nBalls):

                            angle = random.randint(10, 30)

                            self.balls[i].speed_multiplier *= 1.5

                            self.balls.append(Ball(
                                self.balls[i].initial_skin,
                                self.balls[i].rect.x,
                                self.balls[i].rect.y,
                                self.balls[i].dx * math.cos(math.radians(angle)) - self.balls[i].dy * math.sin(math.radians(angle)),
                                self.balls[i].dx * math.sin(math.radians(angle)) + self.balls[i].dy * math.cos(math.radians(angle)),
                                self.balls[i].speed_multiplier,
                            ))
                            self.balls.append(Ball(
                                self.balls[i].initial_skin,
                                self.balls[i].rect.x,
                                self.balls[i].rect.y,
                                self.balls[i].dx * math.cos(math.radians(angle)) + self.balls[i].dy * math.sin(math.radians(angle)),
                                - self.balls[i].dx * math.sin(math.radians(angle)) + self.balls[i].dy * math.cos(math.radians(angle)),
                                self.balls[i].speed_multiplier,
                            ))
                        
                        gSounds['multiple'].play()

                    elif brick.reward.itemType == ITEM_HEART:
                        if self.health < 3:
                            self.health += 1

                        gSounds['recover'].play()

                    brick.reward = None
        
        if self.stuckBall:
            if self.stuckBallTimer != 0:
                self.stuckBallTimer -= 1
            elif self.disperseItem == None:
                for ball in self.balls:
                    if self.stuckBall == id(ball):
                        
                        t = 10

                        x = ball.x + t * ball.dx
                        while x < 0 or x > WIDTH:
                            if x < 0:
                                x = -x
                            if x > WIDTH:
                                x = 2 * WIDTH - x

                        self.disperseItem = Item(ITEM_DISPERSE, x, ball.y, 0)
            else:
                for ball in self.balls:
                    if ball.Collides(self.disperseItem):

                        self.stuckBall = None
                        self.stuckBallTimer = 250
                        self.disperseItem = None

                        for b in self.balls:
                            b.dx = random.randint(-600, 600)
                            b.dy = random.choice([1, -1]) * random.randint(-400, -300)
                            b.speed_multiplier *= 1.5

                        break
        
        if self.ultimateTimer > 0:
            self.ultimateTimer -= 1

    def Exit(self):
        pass

    def render(self, screen):
        for brick in self.bricks:
            brick.render(screen)

        self.paddle.render(screen)

        for ball in self.balls:
            ball.render(screen)

        if self.disperseItem:
            self.disperseItem.render(screen)
        
        CommonRender.RenderScore(screen, self.score)
        CommonRender.RenderHealth(screen, self.health)

        if self.paused:
            t_pause = gFonts['large'].render("PAUSED", False, (255, 255, 255))
            rect = t_pause.get_rect(center = (WIDTH/2, HEIGHT/2))
            screen.blit(t_pause, rect)


    def CheckVictory(self):
        for brick in self.bricks:
            if brick.alive:
                return False

        return True
