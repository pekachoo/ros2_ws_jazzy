#!/bin/bash

# Helper function to move a box
move_box() {
  name=$1
  x=$2
  y=$3
  direction=$4

  if [ "$direction" == "up" ]; then
    for y_pos in $(seq "$y" 0.1 0.5); do
      gz service -s /world/empty/set_pose \
        --reqtype gz.msgs.Pose \
        --reptype gz.msgs.Boolean \
        --timeout 1000 \
        --req "name: \"$name\", position: {x: $x, y: $y_pos, z: 0.25}, orientation: {w: 1.0}"
      sleep 0.05
    done
    for y_pos in $(seq 0.5 -0.1 -6.5); do
      gz service -s /world/empty/set_pose \
        --reqtype gz.msgs.Pose \
        --reptype gz.msgs.Boolean \
        --timeout 1000 \
        --req "name: \"$name\", position: {x: $x, y: $y_pos, z: 0.25}, orientation: {w: 1.0}"
      sleep 0.05
    done
  else
    for y_pos in $(seq "$y" -0.1 -6.5); do
      gz service -s /world/empty/set_pose \
        --reqtype gz.msgs.Pose \
        --reptype gz.msgs.Boolean \
        --timeout 1000 \
        --req "name: \"$name\", position: {x: $x, y: $y_pos, z: 0.25}, orientation: {w: 1.0}"
      sleep 0.05
    done
    for y_pos in $(seq -6.5 0.1 0.5); do
      gz service -s /world/empty/set_pose \
        --reqtype gz.msgs.Pose \
        --reptype gz.msgs.Boolean \
        --timeout 1000 \
        --req "name: \"$name\", position: {x: $x, y: $y_pos, z: 0.25}, orientation: {w: 1.0}"
      sleep 0.05
    done
  fi
}

while true; do
  # run in parallel so all boxes move at the same time
  move_box "moving_box_1" 2 -2 down &
  move_box "moving_box_2" 5 -3 up &
  move_box "moving_box_3" 8 -5 down &

  wait
done
