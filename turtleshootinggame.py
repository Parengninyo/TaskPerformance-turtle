import turtle
import random
import time

# Setup screen
screen = turtle.Screen()
screen.title("Turtle Shooting Game")  # Changed title here
screen.bgcolor("black")
screen.setup(width=600, height=600)

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.goto(-300, 300)
border_pen.pendown()
for _ in range(4):
    border_pen.forward(600)
    border_pen.right(90)
border_pen.hideturtle()

# Setup player
player = turtle.Turtle()
player.shape("turtle")
player.color("blue")
player.penup()
player.speed(0)
player.goto(0, -250)
player.setheading(90)

# Bullet setup
bullets = []
bullet_speed = 20
max_bullets = 10
bullet_cooldown = 0.1
last_shot_time = time.time()

# Enemy setup
shapes = ["circle", "square", "triangle"]
enemies = []

def create_enemy():
    enemy = turtle.Turtle()
    enemy.shape(random.choice(shapes))
    enemy.color("red")
    enemy.penup()
    enemy.speed(0)
    enemy.goto(random.randint(-250, 250), random.randint(100, 250))
    return enemy

def setup_enemies(count):
    global enemies
    enemies.clear()
    for _ in range(count):
        enemies.append(create_enemy())

def start_new_level(level):
    global num_enemies, defeated_enemies, enemy_speed
    if level == 1:
        num_enemies = 5
    elif level == 2:
        num_enemies = 10
    elif level == 3:
        num_enemies = 20
    else:
        num_enemies = 20 + (level - 3) * 10
    
    defeated_enemies = 0
    enemy_speed = 5 + (level - 1) * 2
    setup_enemies(num_enemies)
    update_mission_text()

def move_left():
    x = player.xcor() - 15
    player.setx(max(x, -280))

def move_right():
    x = player.xcor() + 15
    player.setx(min(x, 280))

def create_bullet():
    bullet = turtle.Turtle()
    bullet.shape("square")
    bullet.color("yellow")
    bullet.penup()
    bullet.speed(0)
    bullet.shapesize(stretch_wid=0.2, stretch_len=1)
    return bullet

def fire_bullet():
    global last_shot_time
    current_time = time.time()
    if (current_time - last_shot_time) >= bullet_cooldown and len(bullets) < max_bullets:
        bullet = create_bullet()
        bullet.goto(player.xcor(), player.ycor() + 10)
        bullet.showturtle()
        bullets.append(bullet)
        last_shot_time = current_time

def is_collision(t1, t2):
    return t1.distance(t2) < 20

def update_mission_text():
    mission_text.clear()
    mission_text.write(f"Level {current_level}: Defeat {num_enemies - defeated_enemies} more enemies\nDefeated: {defeated_enemies}", align="left", font=("Arial", 16, "normal"))

def game_over(message):
    game_over_turtle = turtle.Turtle()
    game_over_turtle.hideturtle()
    game_over_turtle.color("white")
    game_over_turtle.penup()
    game_over_turtle.goto(-290, -250)
    game_over_turtle.write(message, align="left", font=("Arial", 24, "bold"))
    screen.update()
    time.sleep(2)
    turtle.bye()  # Close the window after showing the game over message

# Game initialization
current_level = 1
defeated_enemies = 0
num_enemies = 5

mission_text = turtle.Turtle()
mission_text.hideturtle()
mission_text.color("white")
mission_text.penup()
mission_text.goto(-290, 230)
update_mission_text()

start_new_level(current_level)

screen.listen()
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")
screen.onkey(fire_bullet, "space")

while True:
    screen.update()

    for enemy in enemies:
        x = enemy.xcor() + enemy_speed
        enemy.setx(x)

        if x > 280 or x < -280:
            for e in enemies:
                e.sety(e.ycor() - 40)
            enemy_speed *= -1

        if enemy.ycor() < -280:
            game_over("GAME OVER")
            break

        for bullet in bullets:
            if is_collision(bullet, enemy):
                bullet.hideturtle() 
                bullets.remove(bullet)
                enemy.hideturtle()
                enemies.remove(enemy)
                enemies.append(create_enemy())
                defeated_enemies += 1
                update_mission_text()
                if defeated_enemies >= num_enemies:
                    for e in enemies:
                        e.hideturtle()
                    enemies.clear()
                    current_level += 1
                    start_new_level(current_level)
                    break

    for bullet in bullets:
        bullet.sety(bullet.ycor() + bullet_speed)
        if bullet.ycor() > 275:
            bullet.hideturtle()
            bullets.remove(bullet)

    if defeated_enemies >= num_enemies:
        for e in enemies:
            e.hideturtle()
        enemies.clear()
        current_level += 1
        start_new_level(current_level)
