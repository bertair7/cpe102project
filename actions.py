import entities
import worldmodel
import pygame
import math
import random
import point
import image_store

BLOB_RATE_SCALE = 4
BLOB_ANIMATION_RATE_SCALE = 50
BLOB_ANIMATION_MIN = 1
BLOB_ANIMATION_MAX = 3

ORE_CORRUPT_MIN = 20000
ORE_CORRUPT_MAX = 30000

QUAKE_STEPS = 10
QUAKE_DURATION = 1100
QUAKE_ANIMATION_RATE = 100

VEIN_SPAWN_DELAY = 500
VEIN_RATE_MIN = 8000
VEIN_RATE_MAX = 17000



def create_miner_not_full_action(world, entity, i_store):
   def action(current_ticks):
      entity.remove_pending_action(action)

      entity_pt = entity.get_position()
      ore = world.find_nearest(entity_pt, entities.Ore)
      (tiles, found) = entity.miner_to_ore(world, ore)

      new_entity = entity
      if found:
         new_entity = try_transform_miner(world, entity,
            try_transform_miner_not_full)

      schedule_action(world, new_entity,
         create_miner_action(world, new_entity, i_store),
         current_ticks + new_entity.get_rate())
      return tiles
   return action


def create_miner_full_action(world, entity, i_store):
   def action(current_ticks):
      entity.remove_pending_action(action)

      entity_pt = entity.get_position()
      smith = world.find_nearest(entity_pt, entities.Blacksmith)
      (tiles, found) = entity.miner_to_smith(world, smith)

      new_entity = entity
      if found:
         new_entity = try_transform_miner(world, entity,
            try_transform_miner_full)

      schedule_action(world, new_entity,
         create_miner_action(world, new_entity, i_store),
         current_ticks + new_entity.get_rate())
      return tiles
   return action


def create_ore_blob_action(world, entity, i_store):
   def action(current_ticks):
      entity.remove_pending_action(action)

      entity_pt = entity.get_position()
      vein = world.find_nearest(entity_pt, entities.Vein)
      (tiles, found) = entity.blob_to_vein(world, vein)

      next_time = current_ticks + entity.get_rate()
      if found:
         quake = entity._create_quake(world, tiles[0], current_ticks, 
            i_store)
         world.add_entity(quake)
         next_time = current_ticks + entity.get_rate() * 2

      schedule_action(world, entity,
         create_ore_blob_action(world, entity, i_store),
         next_time)

      return tiles
   return action


def find_open_around(world, pt, distance):
   for dy in range(-distance, distance + 1):
      for dx in range(-distance, distance + 1):
         new_pt = point.Point(pt.x + dx, pt.y + dy)

         if (world.within_bounds(new_pt) and
            (not world.is_occupied(new_pt))):
            return new_pt

   return None


def create_vein_action(world, entity, i_store):
   def action(current_ticks):
      entity.remove_pending_action(action)

      open_pt = find_open_around(world, entity.get_position(),
         entity.get_resource_distance())
      if open_pt:
         ore = entity._create_ore(world,
            "ore - " + entity.get_name() + " - " + str(current_ticks),
            open_pt, current_ticks, i_store)
         world.add_entity(ore)
         tiles = [open_pt]
      else:
         tiles = []

      schedule_action(world, entity,
         create_vein_action(world, entity, i_store),
         current_ticks + entity.get_rate())
      return tiles
   return action


def try_transform_miner_full(world, entity):
   new_entity = entities.MinerNotFull(
      entity.get_name(), entity.get_resource_limit(),
      entity.get_position(), entity.get_rate(),
      entity.get_images(), entity.get_animation_rate())

   return new_entity


def try_transform_miner_not_full(world, entity):
   if entity.resource_count < entity.resource_limit:
      return entity
   else:
      new_entity = entities.MinerFull(
         entity.get_name(), entity.get_resource_limit(),
         entity.get_position(), entity.get_rate(),
         entity.get_images(), entity.get_animation_rate())
      return new_entity


def try_transform_miner(world, entity, transform):
   new_entity = transform(world, entity)
   if entity != new_entity:
      clear_pending_actions(world, entity)
      world.remove_entity_at(entity.get_position())
      world.add_entity(new_entity)
      schedule_animation(world, new_entity)

   return new_entity


def create_miner_action(world, entity, image_store):
   if isinstance(entity, entities.MinerNotFull):
      return create_miner_not_full_action(world, entity, image_store)
   else:
      return create_miner_full_action(world, entity, image_store)


def create_animation_action(world, entity, repeat_count):
   def action(current_ticks):
      entity.remove_pending_action(action)

      entity.next_image()

      if repeat_count != 1:
         schedule_action(world, entity,
            create_animation_action(world, entity, max(repeat_count - 1, 0)),
            current_ticks + entity.get_animation_rate())

      return [entity.get_position()]
   return action


def create_entity_death_action(world, entity):
   def action(current_ticks):
      entity.remove_pending_action(action)
      pt = entity.get_position()
      remove_entity(world, entity)
      return [pt]
   return action


def create_ore_transform_action(world, entity, i_store):
   def action(current_ticks):
      entity.remove_pending_action(action)
      blob = entity._create_blob(world, entity.get_name() + " -- blob",
         entity.get_position(), entity.get_rate() // BLOB_RATE_SCALE,
         current_ticks, i_store)

      remove_entity(world, entity)
      world.add_entity(blob)

      return [blob.get_position()]
   return action


def remove_entity(world, entity):
   for action in entity.get_pending_actions():
      world.unschedule_action(action)
   entity.clear_pending_actions()
   world.remove_entity(entity)


def schedule_action(world, entity, action, time):
   entity.add_pending_action(action)
   world.schedule_action(action, time)


def schedule_animation(world, entity, repeat_count=0):
   schedule_action(world, entity,
      create_animation_action(world, entity, repeat_count),
      entity.get_animation_rate())


def clear_pending_actions(world, entity):
   for action in entity.get_pending_actions():
      world.unschedule_action(action)
   entity.clear_pending_actions()
