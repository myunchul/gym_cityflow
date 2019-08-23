_source:_ [CityFlow Docs](https://cityflow.readthedocs.io/en/latest/start.html)

## Data Access API

`get_vehicle_count()`:
* Get number of total running vehicles.
* Return an int

`get_lane_vehicle_count()`:
* Get number of running vehicles on each lane.
* Return a dict with lane id as key and corresponding number as value.

`get_lane_waiting_vehicle_count()`:
* Get number of waiting vehicles on each lane. Currently, vehicles with speed less than 0.1m/s is considered as waiting.
* Return a dict with lane id as key and corresponding number as value.

## Control API

`set_tl_phase(intersection_id, phase_id)`:
* Only works when `rlTrafficLight=true` in `config.json`
* Set the phase of traffic light of `intersection_id` to `phase_id`
* The `intersection_id` should be defined in `roadnet.json`
* `phase_id` is the no. of phase of the traffic light, defined in `roadnet.json`