import point
import worldmodel
import actions
import image_store
import random

class Entity(object):
   def __init__(self, name, imgs):
      self.name = name
      self.imgs = imgs
      self.current_img = 0

   def get_images(self):
      return self.imgs
 
   def get_image(self):
      return self.imgs[self.current_img]

   def get_name(self):
      return self.name


class InGrid(Entity):
   def __init__(self, name, position, imgs):
      super(InGrid, self).__init__(name, imgs)
      self.position = position

   def set_position(self, point):
      self.position = point

   def get_position(self):
      return self.position


class NonBackground(InGrid):
   def __init__(self, name, position, imgs):
      super(NonBackground, self).__init__(name, position, imgs)
      self.pending_actions = []
   
   def remove_pending_action(self, action):
      if hasattr(self, "pending_actions"):
         self.pending_actions.remove(action)

   def add_pending_action(self, action):
      if hasattr(self, "pending_actions"):      
         self.pending_actions.append(action)

   def get_pending_actions(self):
      if hasattr(self, "pending_actions"):
         return self.pending_actions
      else:
         return []      

   def clear_pending_actions(self):
      if hasattr(self, "pending_actions"):
         self.pending_actions = []      

   def next_image(self):
      self.current_img = (self.current_img + 1) % len(self.imgs)
 

class Moving(NonBackground):
   def __init__(self, name, position, rate, imgs):
      super(Moving, self).__init__(name, position, imgs)
      self.rate = rate

   def next_position(self, world, dest_pt):
      horiz = sign(dest_pt.x - self.position.x)
      new_pt = point.Point(self.position.x + horiz, self.position.y)

      if horiz == 0 or world.is_occupied(new_pt):
         vert = sign(dest_pt.y - self.position.y)
         new_pt = point.Point(self.position.x, self.position.y + vert)

         if vert == 0 or world.is_occupied(new_pt):
            new_pt = point.Point(self.position.x, self.position.y)

      return new_pt

   def get_rate(self):
      return self.rate


class Miner(Moving):
   def __init__(self, name, resource_limit, position, rate, imgs, 
      animation_rate):
      super(Miner, self).__init__(name, position, rate, imgs)
      self.resource_limit = resource_limit
      self.animation_rate = animation_rate

   def set_resource_count(self, n):
      self.resource_count = n

   def get_resource_count(self):
      return self.resource_count

   def get_resource_limit(self):
      return self.resource_limit

   def get_animation_rate(self):
      return self.animation_rate

   def _schedule(self, world, ticks, i_store):
      actions.schedule_action(world, self, actions.create_miner_action(world, 
         self, i_store), ticks + self.get_rate())
      actions.schedule_animation(world, self)


class Background(Entity):
   def next_image(self):
      self.current_img = (self.current_img + 1) % len(self.imgs)


class MinerNotFull(Miner):
   def __init__(self, name, resource_limit, position, rate, imgs,
      animation_rate):
      super(MinerNotFull, self).__init__(name, resource_limit, position, rate, 
         imgs, animation_rate)
      self.resource_count = 0

   def miner_to_ore(self, world, ore):
      entity_pt = self.get_position()
      if not ore:
         return ([entity_pt], False)
      ore_pt = ore.get_position()
      if adjacent(entity_pt, ore_pt):
         self.set_resource_count(1 + self.get_resource_count())
         actions.remove_entity(world, ore)
         return ([ore_pt], True)
      else:
         new_pt = self.next_position(world, ore_pt)
         return (world.move_entity(self, new_pt), False)


class MinerFull:
   def __init__(self, name, resource_limit, position, rate, imgs,
      animation_rate):
      super(MinerNotFull, self).__init__(name, resource_limit, position, rate, 
         imgs, animation_rate)
      self.resource_count = resource_limit

   def miner_to_smith(self, world, smith):
      entity_pt = self.get_position()
      if not smith:
         return ([entity_pt], False)
      smith_pt = smith.get_position()
      if adjacent(entity_pt, smith_pt):
         smith.set_resource_count(smith.get_resource_count() +
            self.get_resource_count())
         self.set_resource_count(0)
         return ([], True)
      else:
         new_pt = self.next_position(world, smith_pt)
         return (world.move_entity(self, new_pt), False)


class Vein(Moving):
   def __init__(self, name, rate, position, imgs, resource_distance=1):
      super(Vein, self).__init__(name, rate, position, imgs)
      self.resource_distance = resource_distance

   def get_resource_distance(self):
      return self.resource_distance

   def _create_ore(self, world, name, pt, ticks, i_store):
      ore = Ore(name, pt, image_store.get_images(i_store, 'ore'),
         random.randint(actions.ORE_CORRUPT_MIN, actions.ORE_CORRUPT_MAX))
      ore._schedule(world, ticks, i_store)
      return ore

   def _schedule(self, world, ticks, i_store):
      actions.schedule_action(world, self, actions.create_vein_action(world,
         self, i_store), ticks + self.get_rate())


class Ore(NonBackground):
   def __init__(self, name, position, imgs, rate=5000):
      super(Ore, self).__init__(name, position, imgs)
      self.rate = rate

   def get_rate(self):
      return self.rate

   def _create_blob(self, world, name, pt, rate, ticks, i_store):
      blob = OreBlob(name, pt, rate,
         image_store.get_images(i_store, 'blob'),
         random.randint(actions.BLOB_ANIMATION_MIN, actions.BLOB_ANIMATION_MAX)
         * actions.BLOB_ANIMATION_RATE_SCALE)
      blob._schedule(world, ticks, i_store)
      return blob

   def _schedule(self, world, ticks, i_store):
      actions.schedule_action(world, self,
         actions.create_ore_transform_action(world, self, i_store),
         ticks + self.get_rate())


class Blacksmith(NonBackground):
   def __init__(self, name, position, imgs, resource_limit, rate,
      resource_distance=1):
      super(Blacksmith, self).__init__(name, position, imgs)
      self.resource_limit = resource_limit
      self.resource_count = 0
      self.rate = rate
      self.resource_distance = resource_distance

   def get_rate(self):
      return self.rate

   def set_resource_count(self, n):
      self.resource_count = n

   def get_resource_count(self):
      return self.resource_count

   def get_resource_limit(self):
      return self.resource_limit

   def get_resource_distance(self):
      return self.resource_distance


class Obstacle(InGrid):
   def __init__(self, name, position, imgs):
      super(Obstacle, self).__init__(name, position, imgs)


class OreBlob(Moving):
   def __init__(self, name, position, rate, imgs, animation_rate):
      super(OreBlob, self).__init__(name, position, rate, imgs)
      self.animation_rate = animation_rate

   def get_animation_rate(self):
      return self.animation_rate

   def _create_quake(self, world, pt, ticks, i_store):
      quake = Quake("quake", pt, image_store.get_images(i_store, 'quake'), 
         actions.QUAKE_ANIMATION_RATE)
      quake._schedule(world, ticks)
      return quake

   def _schedule(self, world, ticks, i_store):
      actions.schedule_action(world, self, 
         actions.create_ore_blob_action(world, self, i_store), 
         ticks + self.get_rate())
      actions.schedule_animation(world, self)

   def blob_to_vein(self, world, vein):
      entity_pt = self.get_position()
      if not vein:
         return ([entity_pt], False)
      vein_pt = vein.get_position()
      if adjacent(entity_pt, vein_pt):
         actions.remove_entity(world, vein)
         return ([vein_pt], True)
      else:
         new_pt = self.next_position(world, vein_pt)
         old_entity = world.get_tile_occupant(new_pt)
         if isinstance(old_entity, Ore):
            actions.remove_entity(world, old_entity)
         return (world.move_entity(self, new_pt), False)


class Quake(NonBackground):
   def __init__(self, name, position, imgs, animation_rate):
      super(Quake, self).__init__(name, position, imgs)
      self.animation_rate = animation_rate

   def get_animation_rate(self):
      return self.animation_rate

   def _schedule(self, world, ticks):
      actions.schedule_animation(world, self, actions.QUAKE_STEPS) 
      actions.schedule_action(world, self, 
         actions.create_entity_death_action(world, self), ticks + 
         actions.QUAKE_DURATION)


def sign(x):
   if x < 0:
      return -1
   elif x > 0:
      return 1
   else:
      return 0

def adjacent(pt1, pt2):
   return ((pt1.x == pt2.x and abs(pt1.y - pt2.y) == 1) or
      (pt1.y == pt2.y and abs(pt1.x - pt2.x) == 1))

def get_image(entity):
   return entity.imgs[entity.current_img]

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

