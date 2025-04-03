from cmu_graphics import *
import random 
import math

# HELPER FUNCTIONS
#__________________________________FIND_NEIGHBORS_______________________________
def neighbors(curBoid, otherBoids, visualRange):
    boidNeighbors = []
    # loop by exluding the boid itself and collect the neighbors
    for boid in otherBoids:
        if (boid != curBoid and 
            distance(curBoid.x, curBoid.y, boid.x, boid.y) < visualRange):
            boidNeighbors.append(boid)
    return boidNeighbors 
#_______________________________APPLY_BOID_RULES________________________________
# apply rule of cohesion
def cohesion(boid, neighbors):
    if len(neighbors) == 0: # if there are no neighbors
        return (0, 0) # no change in velocity
    allX = []
    allY = []
    for neighbor in neighbors:
        allX.append(neighbor.x)
        allY.append(neighbor.y)
    avgX = sum(allX)/len(neighbors)
    avgY = sum(allY)/len(neighbors)
    changeDifference = (avgX - boid.x, avgY - boid.y)
    return changeDifference

# apply rule of alignment      
def alignment(boid, neighbors):
    if len(neighbors) == 0: 
        return (0, 0)
    allvx = []
    allvy = []
    for neighbor in neighbors:
        allvx.append(neighbor.vx)
        allvy.append(neighbor.vy)
    avgVx = sum(allvx)/len(neighbors)
    avgVy = sum(allvy)/len(neighbors)
    changeDifference = (avgVx - boid.vx, avgVy - boid.vy)
    return changeDifference

 # apply rule of seperation
def separation(boid, neighbors, minDist):
    if len(neighbors) == 0:
        return (0, 0) 

    sepVector = [0, 0] 
    for neighbor in neighbors:
        dist = distance(boid.x, boid.y, neighbor.x, neighbor.y)
        if 0 < dist < minDist:  # Ensure it's within range
            sepVector[0] += (boid.x - neighbor.x) / dist  # Normalize
            sepVector[1] += (boid.y - neighbor.y) / dist  

    magnitude = (sepVector[0]**2 + sepVector[1]**2)**0.5
    if magnitude > 0:
        sepVector[0] /= magnitude
        sepVector[1] /= magnitude
        
    return sepVector
#_______________________________BOTTON_HELPERS__________________________________
# helper functions for telling if mouse coordinates are in Bottons
# returns True if Mouse is in cohesion botton
def cohesionBotton(app, x, y):
    if (x > app.cohesionX and x < app.cohesionX + app.bottonWidth
        and y > app.bottonY and y < app.bottonY + app.bottonHeight):
        return True

# returns True if Mouse is in alignment botton    
def alignmentBotton(app, x, y):
    if (x > app.alignmentX and x < app.alignmentX + app.bottonWidth
        and y > app.bottonY and y < app.bottonY + app.bottonHeight):
        return True

# returns True if Mouse is in separation botton   
def separationBotton(app, x, y):
    if (x > app.separationX and x < app.separationX + app.bottonWidth
        and y > app.bottonY and y < app.bottonY + app.bottonHeight):
        return True


#______________________________CLASS_BOIDS______________________________________
class Boids:
    
       # Initializes a boid with a position (x, y) and a velocity (vx, vy).
       # The velocity determines the direction and speed of movement.
    
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y 
        self.vx = vx 
        self.vy = vy 
        
    # Updates the boid's position by adding its velocity   
    
    def moveBoid(self, allBoids, visualRange, rule1, rule2, rule3):
        allNeighbors = neighbors(self, allBoids, visualRange)
        
        # apply the rules of cohesion
        if rule1: 
            cohesionImpact = cohesion(self, allNeighbors)
            self.vx += cohesionImpact[0] * 0.1
            self.vy += cohesionImpact[1] * 0.1
        
        # apply rules of alignment 
        if rule2:
            alignmentImpact = alignment(self, allNeighbors)
            self.vx += alignmentImpact[0] * 0.5
            self.vy += alignmentImpact[1] * 0.5
        
        # apply rules for separation
        if rule3:
            separationImpact = separation(self, allNeighbors, minDist = 30)
            self.vx += separationImpact[0] * 1.1
            self.vy += separationImpact[1] * 1.1
        
        # limit the speed 
        maxSpeed = 15
        speed = (self.vx**2 + self.vy**2) ** 0.5 # calculate speed

        # If the boid's speed exceeds maxSpeed, scale velocity down 
        if speed > maxSpeed:
                # Normalize vx while maintaining direction
                self.vx = (self.vx / speed) * maxSpeed  
                # Normalize vy while maintaining direction
                self.vy = (self.vy / speed) * maxSpeed  
            
        self.x += self.vx
        self.y += self.vy 
        
    # each boid should avoid dissapearing from the canvas
    def avoidEdges(self, width, height):
        margin = 150 # margin by which boid starts to avoid
        turnFactor = 1 # factor by which boid makes the turn 
        if self.x < margin:
            self.vx += turnFactor
        if self.x > width - margin:
            self.vx -= turnFactor
        if self.y < margin:
            self.vy += turnFactor
        if self.y > height - margin:
            self.vy -= turnFactor
 #______________________________________________________________________________
 #____________________________onAppStart________________________________________    
def onAppStart(app):
    app.background = "black"
    app.width = 1200
    app.height = 800
    
    # Boid rules 
    app.cohesion = True
    app.alignment = True 
    app.separation = True 
    
    # Boid's parameters
    app.boidNumber = 100  
    app.boidSize = 6
    app.visualRange = 30 
    app.centeringStep = 0.005 # adjust velocity by this %
    """
    use the class Boids and create boidNumber of boids at random positions
    with initial velocity set between -2 to 2 so they go right/left/up/down
    """
    app.boids = []
    for boid in range(app.boidNumber):
        x = random.randint(0, app.width)
        y = random.randint(0, app.height)
        vx = random.uniform(-2, 2)
        vy = random.uniform(-2, 2)
        app.boids.append(Boids(x, y, vx, vy))
    
    # Botton coordinates 
    app.bottonY = app.height*0.9
    app.bottonWidth = app.width * 0.1
    app.bottonHeight = app.height * 0.05
    app.cohesionX = app.width * 0.1
    app.alignmentX = app.width * 0.3
    app.separationX = app.width * 0.5
    
    # Predator Parameters
    app.predator = True
      
def onStep(app):
    # get the boids moving randomly
    for boid in app.boids:
        boid.moveBoid(app.boids, app.visualRange, 
                      app.cohesion, app.alignment, app.separation)
        boid.avoidEdges(app.width, app.height)
        
def onMousePress(app, x, y):
    # turn on/off the 3 rules of boids
    if cohesionBotton(app, x, y):
        app.cohesion = not app.cohesion
    if alignmentBotton(app, x, y):
        app.alignment = not app.alignment
    if separationBotton(app, x, y):
        app.separation = not app.separation

    # One mouse press boid generation
    if app.predator:
        app.boids.append(Boids(x, y, random.uniform(-2, 2), random.uniform(-2, 2)))
    
    
    

def redrawAll(app):
    
    #  Loop through all boids and draw them as triangles 
    for boid in app.boids:
        # Calculate rotation angle based on velocity
        """
        atan2(y, x) is used to calculate the angle of a vector (x, y) relative 
        to the x-axis, ensuring correct direction handling in all quadrants.
        It avoids division by zero and provides a full -180° to 180° range for 
        accurate boid rotation.
        """
        angle = math.degrees(math.atan2(boid.vy, boid.vx))
        # Define three points for the bird triangular shape
        tip_x = boid.x + app.boidSize * 1.2 # Pointy front x
        tip_y = boid.y  # Pointy front y
        left_x = boid.x - app.boidSize # Back left x
        left_y = boid.y - app.boidSize / 1.5 # Back left y
        right_x = boid.x - app.boidSize # Back right x
        right_y = boid.y + app.boidSize / 1.5  # Back right y
        drawPolygon(
            tip_x, tip_y,  # Tip of the triangle 
            left_x, left_y,  # Back left wing
            right_x, right_y,  # Back right wing
            fill = 'pink', rotateAngle = angle)
        
    if app.cohesion:
        drawRect(app.cohesionX,  app.bottonY, 
                app.bottonWidth,  app.bottonHeight,  border="green")
    else:
         drawRect(app.cohesionX,  app.bottonY, 
                app.bottonWidth,  app.bottonHeight,  border="red")
    drawLabel("Cohesion", app.cohesionX + app.bottonWidth / 2, 
              app.bottonY + app.bottonHeight / 2, fill = "white")
        
    if app.alignment:
        drawRect(app.alignmentX,  app.bottonY, 
                app.bottonWidth,  app.bottonHeight,  border="green")
    else:
        drawRect(app.alignmentX,  app.bottonY, 
                app.bottonWidth,  app.bottonHeight,  border="red")
    drawLabel("Alignment", app.alignmentX + app.bottonWidth / 2, 
              app.bottonY + app.bottonHeight / 2, fill = "white")
       
    if app.separation:
        drawRect(app.separationX,  app.bottonY, 
                app.bottonWidth,  app.bottonHeight,  border="green")
    else:
        drawRect(app.separationX,  app.bottonY, 
                app.bottonWidth,  app.bottonHeight,  border="red")
    drawLabel("Separation", app.separationX + app.bottonWidth / 2, 
              app.bottonY + app.bottonHeight / 2, fill = "white")   

    drawRect(app.width * 0.7,  app.bottonY, 
             app.bottonWidth,  app.bottonHeight,  border="green")
    
    
    
runApp()                
