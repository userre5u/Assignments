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
        self.window.bgcolor("white")
        self.window.tracer(0)


    @staticmethod
    def create_visual_object(turtle_visible=True, speed=0, color="black", shape="square", start_coordinates=(0, 0), penup=False, hideturtle=False, shape_size=None, format_msg=None):
        visual_obj = turtle.Turtle(visible=turtle_visible)
        visual_obj.speed(speed)
        visual_obj.shape(name=shape)
        visual_obj.color(color)
        if penup:
            visual_obj.penup()
        if hideturtle:    
            visual_obj.hideturtle()
        if shape_size:
            visual_obj.shapesize(shape_size[0], shape_size[1])
        visual_obj.goto(start_coordinates[0], start_coordinates[1])
        if format_msg:
            visual_obj.write(format_msg["msg"], align=format_msg["align"], font=format_msg["font"])
        return visual_obj

    
    @staticmethod
    def create_border(w, h):
        turtle_g = turtle.Turtle(visible=False)
        new_w, new_h = w+60, h+30
        offset = 5
        turtle_g.color("red", "black")
        turtle_g.goto(-new_w-offset, new_h+offset)
        turtle_g.begin_fill()
        turtle_g.forward(new_w*2)  
        turtle_g.right(90)
        turtle_g.forward(new_h*2)  
        turtle_g.right(90)
        turtle_g.forward(new_w*2)
        turtle_g.right(90)
        turtle_g.forward(new_h*2)
        turtle_g.right(90)
        turtle_g.end_fill()
        turtle_g.hideturtle()
        return new_w, new_h
   

    def game_lost(self):
        self.create_visual_object(turtle_visible=False, penup=True, hideturtle=True, format_msg={"msg": "You Lost :(", "align": "center", "font": ("Arial", 36, "normal")})


    def create_food(self):
        return self.create_visual_object(shape="circle", color="red", penup=True, shape_size=(0.50, 0.50))
    

    def score_update(self, score, high_score):
        self.score_window.speed(0)
        self.score_window.shape("square")
        self.score_window.color("white")
        self.score_window.penup()
        self.score_window.hideturtle()
        self.score_window.goto((-self.width)+20, self.height-20)
        self.score_window.clear()
        self.score_window.write(F"Score: {score} \t\t\t\t\tHigh Score: {high_score}", align="left", font=("Arial", 16, "normal"))



class Snake(Game):
    def __init__(self, color) -> None:
        super().__init__()
        self.color = color
        self.body = []


    def draw_items(self):
        self.score_window = turtle.Turtle()
        w, h = self.window.screensize()
        self.width, self.height = self.create_border(w, h)
        self.create_snake_head()


    def create_snake_head(self):
        self.head = self.create_visual_object(shape="triangle", color=self.color, penup=True, start_coordinates=(0, 100))
    

    def create_snake_body(self):
        single_square = self.create_visual_object(color="blue", penup=True)
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
        if self.head.xcor() > self.width or self.head.ycor() > self.height or self.head.xcor() < -self.width or self.head.ycor() < -self.height:
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


    def reset_game(self, score, high_score):
        self.clean_body()
        self.body = []
        self.score_update(score, high_score)
        self.window.reset()
        self.game_lost()
        time.sleep(2)
        self.window.reset()
        self.draw_items()


    def run(self):
        try:
            score = 0
            high_score = 0
            self.register_keys()
            self.window.listen()
            food = self.create_food()
            while True:    
                self.window.update()
                time.sleep(0.1)
                if self.head.distance(food) < 15:
                    random_x = random.randint(-(self.width-100), self.width-100)
                    random_y = random.randint(-(self.height-100), self.height-100)
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
                    self.reset_game(score, high_score)
                    food = self.create_food()
                    score = 0
                    
        except KeyboardInterrupt:
            print("\nUser aborted")
            return


def main():
    snake = Snake("green")
    snake.draw_items()
    snake.run()


if __name__ == "__main__":
    main()