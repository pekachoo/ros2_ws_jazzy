#!/bin/bash

while true; do
  # Move forward
  for x in $(seq 0.0 0.1 2.0); do
    gz service -s /world/empty/set_pose \
      --reqtype gz.msgs.Pose \
      --reptype gz.msgs.Boolean \
      --timeout 1000 \
      --req "name: \"moving_box\", position: {x: $x, y: 1.0, z: 0.25}, orientation: {w: 1.0}"
    sleep 0.05
  done

  # Move backward
  for x in $(seq 2.0 -0.1 0.0); do
    gz service -s /world/empty/set_pose \
      --reqtype gz.msgs.Pose \
      --reptype gz.msgs.Boolean \
      --timeout 1000 \
      --req "name: \"moving_box\", position: {x: $x, y: 1.0, z: 0.25}, orientation: {w: 1.0}"
    sleep 0.05
  done
done