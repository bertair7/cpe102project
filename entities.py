import point
import worldmodel

class Background:
   def __init__(self, name, imgs):
      self.name = name
      self.imgs = imgs
      self.current_img = 0
   def get_images(self):
      return self.imgs
   def get_name(self):
      return self.name

class MinerNotFull:
   def __init__(self, name, resource_limit, position, rate, imgs,
      animation_rate):
      self.name = name
      self.position = position
      self.rate = rate
      self.imgs = imgs
      self.current_img = 0
      self.resource_limit = resource_limit
      self.resource_count = 0
      self.animation_rate = animation_rate
      self.pending_actions = []
   def next_position(self, world, dest_pt):
      horiz = sign(dest_pt.x - self.position.x)
      new_pt = point.Point(self.position.x + horiz, self.position.y)

      if horiz == 0 or worldmodel.is_occupied(world, new_pt):
         vert = sign(dest_pt.y - self.position.y)
         new_pt = point.Point(self.position.x, self.position.y + vert)

         if vert == 0 or worldmodel.is_occupied(world, new_pt):
            new_pt = point.Point(self.position.x, self.position.y)

      return new_pt
   def set_position(self, point):
      self.position = point
   def get_position(self):
      return self.position
   def get_images(self):
      return self.imgs
   def get_rate(self):
      return self.rate
   def set_resource_count(self, n):
      self.resource_count = n
   def get_resource_count(self):
      return self.resource_count
   def get_resource_limit(self):
      return self.resource_limit
   def get_name(self):
      return self.name
   def get_animation_rate(self):
      return self.animation_rate

class MinerFull:
   def __init__(self, name, resource_limit, position, rate, imgs,
      animation_rate):
      self.name = name
      self.position = position
      self.rate = rate
      self.imgs = imgs
      self.current_img = 0
      self.resource_limit = resource_limit
      self.resource_count = resource_limit
      self.animation_rate = animation_rate
      self.pending_actions = []
   def next_position(self, world, dest_pt):
      horiz = sign(dest_pt.x - self.position.x)
      new_pt = point.Point(self.position.x + horiz, self.position.y)

      if horiz == 0 or worldmodel.is_occupied(world, new_pt):
         vert = sign(dest_pt.y - self.position.y)
         new_pt = point.Point(self.position.x, self.position.y + vert)

         if vert == 0 or worldmodel.is_occupied(world, new_pt):
            new_pt = point.Point(self.position.x, self.position.y)

      return new_pt
   def set_position(self, point):
      self.position = point
   def get_position(self):
      return self.position
   def get_images(self):
      return self.imgs
   def get_rate(self):
      return self.rate
   def set_resource_count(self, n):
      self.resource_count = n
   def get_resource_count(self):
      return self.resource_count
   def get_resource_limit(self):
      return self.resource_limit
   def get_name(self):
      return self.name
   def get_animation_rate(self):
      return self.animation_rate

class Vein:
   def __init__(self, name, rate, position, imgs, resource_distance=1):
      self.name = name
      self.position = position
      self.rate = rate
      self.imgs = imgs
      self.current_img = 0
      self.resource_distance = resource_distance
      self.pending_actions = []
   def next_position(self, world, dest_pt):
      horiz = sign(dest_pt.x - self.position.x)
      new_pt = point.Point(self.position.x + horiz, self.position.y)

      if horiz == 0 or worldmodel.is_occupied(world, new_pt):
         vert = sign(dest_pt.y - self.position.y)
         new_pt = point.Point(self.position.x, self.position.y + vert)

         if vert == 0 or worldmodel.is_occupied(world, new_pt):
            new_pt = point.Point(self.position.x, self.position.y)

      return new_pt
   def set_position(self, point):
      self.position = point
   def get_position(self):
      return self.position
   def get_images(self):
      return self.imgs
   def get_rate(self):
      return self.rate
   def get_name(self):
      return self.name

class Ore:
   def __init__(self, name, position, imgs, rate=5000):
      self.name = name
      self.position = position
      self.imgs = imgs
      self.current_img = 0
      self.rate = rate
      self.pending_actions = []
   def set_position(self, point):
      self.position = point
   def get_position(self):
      return self.position
   def get_images(self):
      return self.imgs
   def get_rate(self):
      return self.rate
   def get_name(self):
      return self.name

class Blacksmith:
   def __init__(self, name, position, imgs, resource_limit, rate,
      resource_distance=1):
      self.name = name
      self.position = position
      self.imgs = imgs
      self.current_img = 0
      self.resource_limit = resource_limit
      self.resource_count = 0
      self.rate = rate
      self.resource_distance = resource_distance
      self.pending_actions = []
   def set_position(self, point):
      self.position = point
   def get_position(self):
      return self.position
   def get_images(self):
      return self.imgs
   def get_rate(self):
      return self.rate
   def set_resource_count(self, n):
      self.resource_count = n
   def get_resource_count(self):
      return self.resource_count
   def get_resource_limit(self):
      return self.resource_limit
   def get_name(self):
      return self.name

class Obstacle:
   def __init__(self, name, position, imgs):
      self.name = name
      self.position = position
      self.imgs = imgs
      self.current_img = 0
   def set_position(self, point):
      self.position = point
   def get_position(self):
      return self.position
   def get_images(self):
      return self.imgs
   def get_name(self):
      return self.name

class OreBlob:
   def __init__(self, name, position, rate, imgs, animation_rate):
      self.name = name
      self.position = position
      self.rate = rate
      self.imgs = imgs
      self.current_img = 0
      self.animation_rate = animation_rate
      self.pending_actions = []
   def next_position(self, world, dest_pt):
      horiz = sign(dest_pt.x - self.position.x)
      new_pt = point.Point(self.position.x + horiz, self.position.y)

      if horiz == 0 or (worldmodel.is_occupied(world, new_pt) and
         not isinstance(worldmodel.get_tile_occupant(world, new_pt),
         entities.Ore)):
         vert = sign(dest_pt.y - self.positin.y)
         new_pt = point.Point(self.position.x, self.position.y + vert)

         if vert == 0 or (worldmodel.is_occupied(world, new_pt) and
            not isinstance(worldmodel.get_tile_occupant(world, new_pt),
            entities.Ore)):
            new_pt = point.Point(self.position.x, self.position.y)

      return new_pt
   def set_position(self, point):
      self.position = point
   def get_position(self):
      return self.position
   def get_images(self):
      return self.imgs
   def get_rate(self):
      return self.rate
   def get_name(self):
      return self.name
   def get_animation_rate(self):
      return self.animation_rate

class Quake:
   def __init__(self, name, position, imgs, animation_rate):
      self.name = name
      self.position = position
      self.imgs = imgs
      self.current_img = 0
      self.animation_rate = animation_rate
      self.pending_actions = []
   def set_position(self, point):
      self.position = point
   def get_position(self):
      return self.position
   def get_images(self):
      return self.imgs
   def get_name(   def get_animation_rate(self):
      return self.animation_rate):
      return self.name
   def get_animation_rate(self):
      return self.animation_rate

def sign(x):
   if x < 0:
      return -1
   elif x > 0:
      return 1
   else:
      return 0

def get_image(entity):
   return entity.imgs[entity.current_img]

def get_resource_distance(entity):
   return entity.resource_distance

def remove_pending_action(entity, action):
   if hasattr(entity, "pending_actions"):
      entity.pending_actions.remove(action)

def add_pending_action(entity, action):
   if hasattr(entity, "pending_actions"):
      entity.pending_actions.append(action)


def get_pending_actions(entity):
   if hasattr(entity, "pending_actions"):
      return entity.pending_actions
   else:
      return []

def clear_pending_actions(entity):
   if hasattr(entity, "pending_actions"):
      entity.pending_actions = []


def next_image(entity):
   entity.current_img = (entity.current_img + 1) % len(entity.imgs)


# This is a less than pleasant file format, but structured based on
# material covered in course.  Something like JSON would be a
# significant improvement.
def entity_string(entity):
   if isinstance(entity, MinerNotFull):
      return ' '.join(['miner', entity.name, str(entity.position.x),
         str(entity.position.y), str(entity.resource_limit),
         str(entity.rate), str(entity.animation_rate)])
   elif isinstance(entity, Vein):
      return ' '.join(['vein', entity.name, str(entity.position.x),
         str(entity.position.y), str(entity.rate),
         str(entity.resource_distance)])
   elif isinstance(entity, Ore):
      return ' '.join(['ore', entity.name, str(entity.position.x),
         str(entity.position.y), str(entity.rate)])
   elif isinstance(entity, Blacksmith):
      return ' '.join(['blacksmith', entity.name, str(entity.position.x),
         str(entity.position.y), str(entity.resource_limit),
         str(entity.rate), str(entity.resource_distance)])
   elif isinstance(entity, Obstacle):
      return ' '.join(['obstacle', entity.name, str(entity.position.x),
         str(entity.position.y)])
   else:
      return 'unknown'

