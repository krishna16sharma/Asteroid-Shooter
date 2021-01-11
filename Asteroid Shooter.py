from vpython import *
#GlowScript 3.0 VPython

scene.range = 30
#scene.userspin = False
scene.userpan = False

earth = sphere(pos=vector(-235,-380,-350), radius=200, texture={'file':textures.earth,'bumpmap':bumpmaps.earth}, shininess = 0)
#moon = sphere(pos=vector(100,80,-350), radius=50, shininess = 0,  texture={'file':textures.rough,'bumpmap':bumpmaps.rock}, color = vector(1,1,0))

body = box(pos=vector(0,-25,0),size=vector(2,4,2), color = color.red)
shipbox = box(pos=vector(0,-25,-1),size=vector(1.75,3,1), color = color.red)
glass = ellipsoid(pos=vector(0,-25,0),size=vector(2,4,3), color = color.blue, opacity=0.6)
tip = pyramid(pos=vector(0,-23,0), size=vector(2,2,2), axis = vector(0,1,0), color=color.red)
exhaust = cylinder(pos=vector(0,-27.5,0), axis=vector(0,1,0), radius=0.5, make_trail=True, retain=5)
cannon1 = cylinder(pos=vector(0.275,-23.5,-1), axis=vector(0,1,0), radius=0.25)
cannon2 = cylinder(pos=vector(-0.275,-23.5,-1), axis=vector(0,1,0), radius=0.25)
ship = compound([body,shipbox,glass,tip,exhaust,cannon1,cannon2] , texture={'file':textures.metal,'bumpmap':bumpmaps.metal})


drag = False
s = ship
t = 0
dt = 0.02
bullet1 = None
bullet2 = None
score = 0
life = 3
mylabel = label(pos = vec(-40,25,0))

asteroids = []
        
def build_asteroids():
    global asteroids
    s1 = sphere(pos=vector(0,30,-1),radius=2)
    s2 = sphere(pos=vector(1.75,29.7,-1),radius=1.1)
    s3 = sphere(pos=vector(-1.75,29.7,-1),radius=1.3)
    asteroid1 = compound(([s1,s2]),  texture={'file':textures.rough,'bumpmap':bumpmaps.rock}, color= vector(0.64,0.59,0.57), shininess = 0, velocity=vector(0,-25*random()+0.2,0))
    asteroid1.pos = vector(60*random()-25*random(),30,-1)
    asteroids.append(asteroid1)
    asteroid2 = compound(([s1,s3]),  texture={'file':textures.rough,'bumpmap':bumpmaps.rock}, color= vector(0.64,0.59,0.6), shininess = 0, velocity=vector(0,-20*random()+0.2,0))
    asteroid2.pos = vector(-25*random()+30*random(),30,-1)
    asteroids.append(asteroid2)
    
def deploy_asteroids():
    global life
    for asteroid in asteroids:
        asteroid.pos +=(asteroid.velocity*dt)
        asteroid.rotate(angle=0.01, axis=vector(0,random(),1))
        
        
        if(asteroid.pos.y<=30 and asteroid.pos.y>-27.5):
            asteroid.visible = True
           # print(asteroid.pos,'Visible')
        if(asteroid.pos.y>30 or asteroid.pos.y<=-27.5):
           # print('invisible')
            asteroid.visible = False
            asteroid.pos.y = 30
            asteroid.pos.x = -25*random()+30*random()
            asteroid.velocity.y = -22*random()+0.5
            life-=1
            
        if(abs(s.pos.x - asteroid.pos.x)<=1.5 and abs(s.pos.y-asteroid.pos.y)<=2):
            s.visible = False
            print('HIT')
            sleep(0.5)
            life-=1
            s.visible = True 
            asteroid.visible = False
            asteroid.pos.y = 30
            asteroid.pos.x = -25*random()+30*random()
            asteroid.velocity.y = -22*random()+0.5
            
        '''if((abs(bullet1.pos.x -asteroid.pos.x)<1 and abs(bullet1.pos.y-asteroid.pos.y)<1)
            or(abs(bullet2.pos.x -asteroid.pos.x)<1 and abs(bullet2.pos.y-asteroid.pos.y)<1)):
                asteroid.visible = False
                asteroid.pos.y = 30
                asteroid.pos.x = -25*random()+30*random()
                asteroid.velocity.y = -22*random()+0.5'''
                
def showSphere(evt):
    bullet_t = 0
    global dt,score,life
    loc1 = ship.pos+ vector(0.275,2,-1)
    loc2 = ship.pos+vector(-0.275,2,-1)
    bullet1 = sphere(pos=loc1, radius=0.2, color=color.orange, velocity=vector(0,15,0))
    bullet2 = sphere(pos=loc2, radius=0.2, color=color.orange, velocity=vector(0,15,0))
    while(bullet_t>=0):
        rate(80)
        bullet_t+=dt
        bullet1.pos = loc1+(bullet1.velocity*bullet_t)
        bullet2.pos = loc2+(bullet2.velocity*bullet_t)
        #asteroid.pos = vector(0,30,-1)+(asteroid.velocity*t)
        #asteroid.rotate(angle=0.01, axis=vector(0,1,1))
        for asteroid in asteroids:
            if((abs(bullet1.pos.x -asteroid.pos.x)<2 and abs(bullet1.pos.y-asteroid.pos.y)<1)
                or(abs(bullet2.pos.x -asteroid.pos.x)<2 and abs(bullet2.pos.y-asteroid.pos.y)<1)):
                    score+=1
                    asteroid.visible = False
                    asteroid.pos.y = 30
                    asteroid.pos.x = -25*random()+30*random()
                    asteroid.velocity.y = -22*random()+0.5
                    

scene.bind('click', showSphere)

def down():
    global drag, s
    drag = True

def move():
    global drag, s
    if drag: # mouse button is down
        s.pos = scene.mouse.pos
        if(s.pos.y > -20):
            s.pos.y = -20
        if(s.pos.z !=0):
            s.pos.z = 0

def up():
    global drag
    drag = False
    
scene.bind("mousedown", down)
scene.bind("mousemove", move)
scene.bind("mouseup", up)

build_asteroids()
while (True):
    rate(80)
    earth.rotate(angle=0.001235, axis=vector(0.1,1,0))
    mylabel.text = 'life : ' + life + '\n' + 'score : ' + score
    
    if life==0:
        mylabel.text='GAME OVER'
        mylabel.pos = vector(0,0,0)
        break;
        
    t+=dt
    deploy_asteroids()
    
        



