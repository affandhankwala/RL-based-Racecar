from racecar import Racecar
from track import Track
def test(directory: str, track_name: str) -> None:
    track = Track(directory, track_name)
    r = Racecar(track)
    show = False
    # Test Accelerate
    r.update_acceleration([0, 1], show)
    r.update_acceleration([-1, 1], show)
    r.update_acceleration([0, 0], show)
    # Test Fail accelerate
    r.update_acceleration([-2, 1], show)
    r.update_acceleration([0, 3], show)

    # Test velocity
    r.set_acceleration([1, -1])
    r.update_velocity(show)
    r.update_velocity(show)
    r.update_velocity(show)
    r.update_velocity(show)
    r.update_velocity(show)
    r.update_velocity(show)

    # Test Position
    r.set_velocity([1, 2])
    r.update_position(show)
    r.update_position(show)
    r.update_position(show)
    r.set_velocity([-1, -2])
    r.update_position(show)
    r.update_position(show)
    r.update_position(show)

    # Test Hit wall
    r.set_velocity([5, 5])
    r.reset_position()
    print(r.get_position())
    r.update_position(True)
    r.hit_wall(True)