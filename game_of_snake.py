from sense_hat import SenseHat
from time import sleep
from random import randint

sense = SenseHat()

x = 0
y = 0
length = 4
tail = [(0,0)]

def set_all(r, g, b):
    for i in range(0,8):
        for j in range(0,8):
            sense.set_pixel(i, j, r, g, b)


def restart():
    global x, y, length, tail
    x, y = 0, 0
    length = 4
    tail = [(0,0)]
    sense.set_pixel(x, y, 255, 0, 0)  # snake starts in the top left corner
    a_wild_pixel_appears()  # pixel to eat


def fail_animation():
    for i in range(0, 10):
        set_all(0, 0, 255)
        sleep(0.1)
        sense.clear()
        sleep(0.1)


def a_wild_pixel_appears():
    x_wild = randint(0,7)
    y_wild = randint(0,7)
    # we need to exclude pixel locations that are already occupied, in a general way...

    sense.set_pixel(x_wild, y_wild, 0, 255, 0)

sense.clear()
restart()

board_state = sense.get_pixels()
print(board_state)


while True:
    event = sense.stick.wait_for_event()  #take joystick input

    # modulus allows wrap around if fall off edge of 8*8 board
    if event.direction == "right":
        x = (x+1) % 8
    elif event.direction == "left":
        x = (x+7) % 8
    elif event.direction == "down":
        y = (y+1) % 8
    elif event.direction == "up":
        y = (y+7) % 8

    tail.append((x,y))
    if len(tail) > length:
        end = tail.pop(0)
        sense.set_pixel(end[0], end[1], 0, 0, 0)

    index_eaten = y*8 + x
    eaten_pixel = sense.get_pixels()[index_eaten]
    if eaten_pixel[1] != 0:
        length +=1
        sense.set_pixel(randint(0, 7), randint(0, 7), 0, 255, 0) # new pixel to eat
        # of course there's an interesting bug here: what if it's in our tail?
    elif eaten_pixel[0] != 0:
        fail_animation()
        restart()
        continue
    
    sense.set_pixel(x, y, 255, 0, 0)

    
    


    
