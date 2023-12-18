import turtle
import random
import time
from enum import Enum


class DIRECTIONS(Enum):
    UP = 90
    DOWN = 270
    LEFT = 180
    RIGHT = 0


class Game:
    def __init__(self) -> None:
        self.window = turtle.Screen()
        self.window.title('Snake Game')
        self.window.bgcolor("black")
        self.window.tracer(0)
        self.score_window = turtle.Turtle()

   

    @staticmethod
    def game_lost():
        score_window = turtle.Turtle(visible=False)
        score_window.speed(0)
        score_window.shape("square")
        score_window.color("white")
        score_window.penup()
        score_window.hideturtle()
        score_window.goto(0, 0)
        score_window.write(F"You Lost :(", align="center", font=("Arial", 36, "normal"))

    

    def score_update(self, score, high_score):
        self.score_window.speed(0)
        self.score_window.shape("square")
        self.score_window.color("white")
        self.score_window.penup()
        self.score_window.hideturtle()
        self.score_window.goto(-380, 280)
        self.score_window.clear()
        self.score_window.write(F"Score: {score} \t\t\t\t\tHigh Score: {high_score}", align="left", font=("Arial", 16, "normal"))



class Food:
    @staticmethod
    def create_food():
        food = turtle.Turtle()
        food.speed(0)
        food.shape(name="circle")
        food.color("red")
        food.penup()
        food.shapesize(0.50, 0.50)
        food.goto(0, 0)
        return food



class Snake(Game):
    def __init__(self, color) -> None:
        super().__init__()
        self.color = color
        self.body = []


    def create_snake_head(self):
        self.head = turtle.Turtle()
        self.head.speed = 0
        self.head.shape(name="triangle")
        self.head.color(self.color)
        self.head.penup()
        self.head.goto(0, 100)
    

    def create_snake_body(self):
        single_square = turtle.Turtle()
        single_square.speed = 0
        single_square.shape(name="square")
        single_square.color("grey")
        single_square.penup()
        self.body.append(single_square)
    

    def go_right(self):
        if (self.head.heading()) != DIRECTIONS.LEFT.value:
            self.head.setheading(DIRECTIONS.RIGHT.value)
    

    def go_left(self):
        if (self.head.heading()) != DIRECTIONS.RIGHT.value:
            self.head.setheading(DIRECTIONS.LEFT.value)



    def go_up(self):
        if (self.head.heading()) != DIRECTIONS.DOWN.value:
            self.head.setheading(DIRECTIONS.UP.value)


    def go_down(self):
        if (self.head.heading()) != DIRECTIONS.UP.value:
            self.head.setheading(DIRECTIONS.DOWN.value)



    def move_body(self):
        for square in range(len(self.body)-1, 0, -1):
            new_x = self.body[square-1].xcor()
            new_y = self.body[square-1].ycor()
            self.body[square].goto(new_x, new_y)


    def register_keys(self):
        self.window.onkey(self.go_up, "Up")
        self.window.onkey(self.go_right, "Right")
        self.window.onkey(self.go_left, "Left")
        self.window.onkey(self.go_down, "Down")



    def move_head(self):
        if self.head.heading() == DIRECTIONS.RIGHT.value:
            x = self.head.xcor()
            self.head.setx(x + 20)

        elif self.head.heading() == DIRECTIONS.LEFT.value:
            x = self.head.xcor()
            self.head.setx(x - 20)

        elif self.head.heading() == DIRECTIONS.UP.value:
            y = self.head.ycor()
            self.head.sety(y + 20)

        elif self.head.heading() == DIRECTIONS.DOWN.value:
            y = self.head.ycor()
            self.head.sety(y - 20)
    

    def border_check(self):
        if self.head.xcor() > 400 or self.head.ycor() > 300 or self.head.xcor() < -400 or self.head.ycor() < -300:
            time.sleep(1)
            self.head.goto(0, 0)
            return True
        return False
    

    def snake_eat_itself(self):
        for square in self.body:
            if square.distance(self.head) < 20:
                time.sleep(1)
                self.head.goto(0, 0)
                return True
        return False

    def clean_body(self):
        for square in self.body:
            square.reset()



    def run(self):
        score = 0
        high_score = 0
        counter = 0
        self.register_keys()
        self.window.listen()
        food = Food().create_food()
        while True:    
            self.window.update()
            time.sleep(0.1)
            if self.head.distance(food) < 15:
                random_x = random.randint(-290, 290)
                random_y = random.randint(-290, 290)
                self.create_snake_body()
                score += 10
                if score > high_score:
                    high_score = score
                self.score_update(score, high_score)
                food.goto(random_x, random_y)
            self.move_body()
            if len(self.body) > 0:   
                square_before_head_x = self.head.xcor()
                square_before_head_y = self.head.ycor()
                self.body[0].goto(square_before_head_x, square_before_head_y)
            self.move_head()
            if self.border_check() or self.snake_eat_itself():
                self.clean_body()
                self.body = []
                score = 0
                self.score_update(score, high_score)
                counter += 1
                if counter == 3:
                    break
        self.window.reset()
        self.game_lost()
        self.window.exitonclick()


snake = Snake("green")
snake.create_snake_head()
snake.run()