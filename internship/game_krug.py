import turtle

def prepare_fig(fig, x, y):
    fig.hideturtle()
    fig.penup()
    fig.setposition(x, y)
    fig.speed(500)

def draw_square(fig, color, side_length):
    fig.pendown()
    fig.fillcolor(color)
    fig.begin_fill()
    for i in range(4):
        fig.fd(side_length)
        fig.rt(90)
    fig.end_fill()

def message(text, color):
    global a
    circ.hideturtle()
    circ.goto(-50, 0)
    circ.color(color)
    sq.clear()
    sq2.clear()
    zvezda.hideturtle()
    if a==2:
        zvezda.penup()
        zvezda.goto(90, 30)
        zvezda.pendown()
        zvezda.showturtle()
    print(moves)
    circ.write(text, font=("Arial", 12, "bold"))

def win_or_die(moves):
    global a
    if -220 < circ.xcor() < -180 and 180 < circ.ycor() < 220:
        a+=1
        message(WIN_MSG + str(moves), 'green')
        
    if -310 < circ.xcor() < 290 and (230 < circ.ycor() < 310 or -310 < circ.ycor() < -230):
        message(GAME_OVER_MSG + str(moves), 'red')
    if (-310 < circ.xcor() < -230 or 230 < circ.xcor() < 310) and -310 < circ.ycor() < 310:
        message(GAME_OVER_MSG + str(moves), 'red')
    if (-130<circ.xcor()<-50 or 110<circ.xcor()<250) and 170<circ.ycor()<250:
        message(GAME_OVER_MSG + str(moves), 'red')
    if (-10<circ.xcor()<70 or 170<circ.xcor()<250) and 110<circ.ycor()<190:
        message(GAME_OVER_MSG + str(moves), 'red')
    if -250<circ.xcor()<130 and 50<circ.ycor()<130:
        message(GAME_OVER_MSG + str(moves), 'red')
    if 50<circ.xcor()<190 and -10<circ.ycor()<70:
        message(GAME_OVER_MSG + str(moves), 'red')
    if (-190<circ.xcor()<-50 or 50<circ.xcor()<190) and -70<circ.ycor()<10:
        message(GAME_OVER_MSG + str(moves), 'red')
    if -190<circ.xcor()<130 and -130<circ.ycor()<-50:
        message(GAME_OVER_MSG + str(moves), 'red')
    if (-130<circ.xcor()<10 or 170<circ.xcor()<250) and -190<circ.ycor()<-110:
        message(GAME_OVER_MSG + str(moves), 'red')
    if (-250<circ.xcor()<-170 or 50<circ.xcor()<130) and -250<circ.ycor()<-170:
        message(GAME_OVER_MSG + str(moves), 'red')

    if 200<circ.xcor()<220 and -220<circ.ycor()<-200:
        zvezda.hideturtle()
        a+=1
    
def movey(deltay):
    global moves
    y = circ.ycor() + deltay
    circ.sety(y)
    moves += 1
    win_or_die(moves)

def movex(deltax):
    global moves
    x = circ.xcor() + deltax
    circ.setx(x)
    moves += 1
    win_or_die(moves)

wndow = turtle.Screen()
wndow.title("Circle game")
wndow.setup(600, 600)

zvezda = turtle.Turtle()
zvezda.hideturtle()
zvezda.shape("turtle")
zvezda.color("green")
zvezda.penup()
zvezda.goto(210, -210)
zvezda.pendown()
zvezda.showturtle()

circ = turtle.Turtle()
circ.penup()
circ.shape("circle")
circ.color("orange")

sq = turtle.Turtle()
f = -240
for i in range(10):
    if -250<f<-180 or 0<f<70:
        prepare_fig(sq,  f, -180)
        draw_square(sq, 'red', 60)
    if -180<f<-50 or 170<f<240:
        prepare_fig(sq,  f, -120)
        draw_square(sq, 'red', 60)
    if -190<f<-60:
        prepare_fig(sq,  f, 0)
        draw_square(sq, 'red', 60)
    if -1<f<70:
        prepare_fig(sq,  120, f)
        draw_square(sq, 'red', 60)
    if 70>f>-70 :
        prepare_fig(sq,  60, f)
        draw_square(sq, 'red', 60)
    if -130<f<-60 or 110<f<190:
        prepare_fig(sq,  f, 240)
        draw_square(sq, 'red', 60)
    if -1<f<60 or 120<f<190:
        prepare_fig(sq,  f, 180)
        draw_square(sq, 'red', 60)
    if f<100:
        prepare_fig(sq,  f, 120)
        draw_square(sq, 'red', 60)
    if -190<f<1:
        prepare_fig(sq,  f, -60)
        draw_square(sq, 'red', 60)
    if f<360:
        prepare_fig(sq,  240, f)
        draw_square(sq, 'red', 60)
        prepare_fig(sq,  -300, f)
        draw_square(sq, 'red', 60)
    if f<300: 
        prepare_fig(sq,  f, 300)
        draw_square(sq, 'red', 60)
        prepare_fig(sq,  f, -240)
        draw_square(sq, 'red', 60)
        f+=60

sq2 = turtle.Turtle()
prepare_fig(sq2, -220, 220)
draw_square(sq2, 'green', 40)

moves = 0
a = 0
GAME_OVER_MSG = 'Game over!\nСделано шагов: '
WIN_MSG = 'Победа!\nСделано шагов: '
STEP = 10

turtle.listen()
turtle.onkeypress(lambda: movey(STEP), 'Up')
turtle.onkeypress(lambda: movey(-STEP), 'Down')
turtle.onkeypress(lambda: movex(STEP), 'Right')
turtle.onkeypress(lambda: movex(-STEP), 'Left')
turtle.done()
