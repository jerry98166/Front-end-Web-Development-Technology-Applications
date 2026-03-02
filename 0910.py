import turtle

wn = turtle.Screen()
alex = turtle.Turtle()
# 畫圓形螺旋
for i in range(200):
    alex.circle(i)   # 每次畫一個越來越大的圓
    alex.right(20)

wn.exitonclick()