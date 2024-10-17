import random
from copy import deepcopy


from hamingja_dungeon.dungeon_elements.chamber import Chamber
from hamingja_dungeon.dungeon_elements.hallway import Hallway
from hamingja_dungeon.dungeon_elements.mask import Mask
from hamingja_dungeon.dungeon_elements.room_factory import RoomFactory
from hamingja_dungeon.hallway_designers.hallway_designer import (
    DesignerError,
    HallwayDesigner,
)
from hamingja_dungeon.utils.dimension_sampler import DimensionSampler
from hamingja_dungeon.dungeon_elements.sector import Sector
from hamingja_dungeon.utils.direction import Direction
from hamingja_dungeon.utils.exceptions import EmptyFitArea
from hamingja_dungeon.dungeon_designers.config.dungeon_area_config import (
    DungeonAreaConfig,
)
from hamingja_dungeon.tile_types import carpet


# TODO look for entrances and not put new ones close to the already placed.
class PrototypeDesigner:
    def __init__(self, config: DungeonAreaConfig):
        self._to_process: list[int] = []
        self.hallway_designer = None
        self.config = config
        if config.room_size_method == "factor":
            self.room_dim_sampler = DimensionSampler.as_factor(
                config.size,
                config.factor_room_size,
            )
        elif config.room_size_method == "range":
            self.room_dim_sampler = DimensionSampler(config.range_room_size)
        else:
            self.room_dim_sampler = DimensionSampler.fixed(config.fixed_room_size)
        self.room_factory = RoomFactory()

    def _get_room(self):
        size = self.room_dim_sampler.sample()
        num = random.random()
        if num < 0.6:
            room = self.room_factory.rectangle_room(size)
        elif num < 0.8:
            room = self.room_factory.l_room(size)
        else:
            room = self.room_factory.circle_room(min(size))
        return room

    def _create_hallway(self, dungeon_area: Sector, room_id: int):
        room = dungeon_area.get_child(room_id)
        if not isinstance(room, Chamber):
            raise ValueError("Hallway can be created only from a room.")
        room_origin = dungeon_area.get_child_origin(room_id)

        anchor_point = room.entrypoints.sample_mask_coordinate()
        origin_point = room_origin + anchor_point
        return self.hallway_designer.design_hallway(
            origin_point, Direction.get_all_directions()
        )

    def _prepare(self, dungeon_area: Sector):
        start_room = self._get_room()
        start_room.draw_borderless(carpet)
        fit_area = dungeon_area.fit_in(start_room)
        if fit_area.is_empty():
            raise EmptyFitArea("Cannot fit the first room.")
        origin = fit_area.sample_mask_coordinate()
        id = dungeon_area.add_chamber(origin, start_room)
        self._to_process.append(id)
        self.hallway_designer = HallwayDesigner(dungeon_area)

    def connect_nearby(self, sector: Sector, room_id: int) -> None:
        room = sector.get_chamber(room_id)
        origin = sector.get_child_origin(room_id)
        if not isinstance(room, Chamber):
            raise ValueError("Can connect only rooms.")

        entrypoints = Mask.empty_mask(sector.size).insert_mask(origin, room.entrypoints)

        nearby = set()
        for entrypoint in entrypoints.mask_coordinates():
            ids = sector.get_children_at(entrypoint)
            ids.remove(room_id)
            for id in ids:
                child = sector.get_child(id)
                if not isinstance(child, Chamber):
                    continue
                child_entrypoints = Mask.empty_mask(sector.size).insert_mask(
                    sector.get_child_origin(room_id), child.entrypoints
                )
                if not (entrypoints & child_entrypoints).is_empty():
                    nearby.add(id)

        # for nearby_id in nearby:
        #     distance = sector.children.distances(room_id, nearby_id)[0][0]
        #     if distance < 3:
        #         continue
        #     sector.make_entrance_between(room_id, nearby_id)

    def _add_room(self, sector: Sector):
        if len(self._to_process) == 0:
            return -1
        tries = 0
        neighbour_id = random.choice(self._to_process)
        while tries < 2:
            num = random.random()
            if num < 0.6 or isinstance(sector.get_child(neighbour_id), Hallway):
                room = self._get_room()
                try:
                    new_room_id = sector.add_room_adjacent(room, neighbour_id)
                    # sector.make_entrance(neighbour_id, new_room_id)
                    self.connect_nearby(sector, new_room_id)
                except EmptyFitArea:
                    tries += 1
                    continue
                self._to_process.append(new_room_id)
                return 1
            else:
                try:
                    origin, hallway = self._create_hallway(sector, neighbour_id)
                    new_room_id = sector.add_chamber(origin, hallway)
                    # sector.make_entrance(neighbour_id, new_room_id)
                    self.connect_nearby(sector, new_room_id)

                except DesignerError:
                    tries += 1
                    continue
                self._to_process.append(new_room_id)
                return 1
        self._to_process.remove(neighbour_id)
        return 1

    def remove_dead_ends(self, sector: Sector):
        rooms_copy = deepcopy(sector.get_chambers())
        for room_id, room in rooms_copy.items():
            if not isinstance(room.area, Hallway):
                continue
            if room.area.has_dead_end():
                sector.remove_chamber(room_id)

    # TODO populate with iterations.
    def populate(self, sector: Sector):
        self._prepare(sector)
        while sector.fullness() < self.config.fullness:
            code = self._add_room(sector)
            if code == -1:
                break

