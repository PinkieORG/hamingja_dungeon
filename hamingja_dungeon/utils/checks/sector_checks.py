

def check_chamber_of_id_exists(chamber_id: int, chamber_ids: list[int]) -> None:
    if chamber_id not in chamber_ids:
        raise ValueError("The chamber of this id does not exist.")
