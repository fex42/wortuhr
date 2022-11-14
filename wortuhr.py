import cadquery as cq

front_th = 2.0
diffusor_th = 0.4 #- 0.4

led_dx = 16.6
led_dy = 18.94

cnt_x = 11
cnt_y = 10

size_x = 240 # 2*border + (cnt_x - 1) * led_dx
size_y = 240 # 2*border + (cnt_y - 1) * led_dy

wall_th = 1.2

letters = iter(list(
    "ESKISTAFÜNF" + 
    "ZEHNZWANZIG" + 
    "DREIVIERTEL" + 
    "VORFUNKNACH" + 
    "HALBAELFÜNF" + 
    "EINSDCWZWEI" + 
    "DREIAUJVIER" + 
    "SECHSNLACHT" + 
    "SIEBENZWÖLF" + 
    "ZEHNEUNKUHR" ))

front = (cq.Workplane("XY")
          .box(size_y, size_x, front_th + diffusor_th)
          .faces(">Z").workplane()
          .rarray(led_dy, led_dx, cnt_y, cnt_x)
    .eachpoint(lambda loc: (cq.Workplane().workplane(offset=-diffusor_th)
                 .text(next(letters), 10, -front_th)
                 .rotate((0, 0, 1),(0, 0, 2), 90)
                 .val().moved(loc)), combine='s')
    )

result = (front.faces("<Z").workplane()
          .rect(wall_th + cnt_y * led_dy, wall_th + cnt_x * led_dx)
          .rarray(led_dy, led_dx, cnt_y, cnt_x)
          .rect(led_dy - wall_th, led_dx - wall_th).extrude(10.0)
)

log(f"size_x = {size_x}")
log(f"size_y = {size_y}")

show_object(result)