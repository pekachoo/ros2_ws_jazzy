#!/bin/bash

while true; do
  for i in $(seq 0 0.1 2.8); do
    # Box 1: moves up/down around y = -4.2
    gz service -s /world/empty/set_pose --reqtype gz.msgs.Pose --reptype gz.msgs.Boolean \
      --timeout 1000 --req "name: \"moving_box_1\", position: {x: 0.0, y: $((-4.2 + i)), z: 0.25}, orientation: {w: 1.0}"

    # Box 2: moves left/right around x = 1.4
    gz service -s /world/empty/set_pose --reqtype gz.msgs.Pose --reptype gz.msgs.Boolean \
      --timeout 1000 --req "name: \"moving_box_2\", position: {x: $((1.4 + i)), y: -5.6, z: 0.25}, orientation: {w: 1.0}"

    # Box 3: diagonal motion
    gz service -s /world/empty/set_pose --reqtype gz.msgs.Pose --reptype gz.msgs.Boolean \
      --timeout 1000 --req "name: \"moving_box_3\", position: {x: $((-2.1 + i)), y: $((-8.4 + i)), z: 0.25}, orientation: {w: 1.0}"

    sleep 0.05
  done

  for i in $(seq 2.8 -0.1 0); do
    gz service -s /world/empty/set_pose --reqtype gz.msgs.Pose --reptype gz.msgs.Boolean \
      --timeout 1000 --req "name: \"moving_box_1\", position: {x: 0.0, y: $((-4.2 + i)), z: 0.25}, orientation: {w: 1.0}"

    gz service -s /world/empty/set_pose --reqtype gz.msgs.Pose --reptype gz.msgs.Boolean \
      --timeout 1000 --req "name: \"moving_box_2\", position: {x: $((1.4 + i)), y: -5.6, z: 0.25}, orientation: {w: 1.0}"

    gz service -s /world/empty/set_pose --reqtype gz.msgs.Pose --reptype gz.msgs.Boolean \
      --timeout 1000 --req "name: \"moving_box_3\", position: {x: $((-2.1 + i)), y: $((-8.4 + i)), z: 0.25}, orientation: {w: 1.0}"

    sleep 0.05
  done
done
