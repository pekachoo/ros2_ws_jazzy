#!/bin/bash

# Helper function to move a box in a back-and-forth Y pattern
move_box() {
  name=$1
  x=$2
  y_start=$3
  y_end=$4
  step=$5

  for y_pos in $(seq "$y_start" "$step" "$y_end"); do
    gz service -s /world/empty/set_pose \
      --reqtype gz.msgs.Pose \
      --reptype gz.msgs.Boolean \
      --timeout 1000 \
      --req "name: \"$name\", position: {x: $x, y: $y_pos, z: 0.25}, orientation: {w: 1.0}"
    sleep 0.05
  done
  for y_pos in $(seq "$y_end" "-$step" "$y_start"); do
    gz service -s /world/empty/set_pose \
      --reqtype gz.msgs.Pose \
      --reptype gz.msgs.Boolean \
      --timeout 1000 \
      --req "name: \"$name\", position: {x: $x, y: $y_pos, z: 0.25}, orientation: {w: 1.0}"
    sleep 0.05
  done
}

while true; do
  # Launch each box motion in parallel
  move_box "moving_box_1" 0.0 -4.2 -1.4 0.1 &     # Up/down sweep in tighter corridor
  move_box "moving_box_2" 1.4 -5.6 -2.8 0.1 &     # Lateral sweep
  move_box "moving_box_3" -2.1 -8.4 -5.6 0.1 &    # Diagonal-style motion

  wait
done
