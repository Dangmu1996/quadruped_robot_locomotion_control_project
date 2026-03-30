# SPDX-FileCopyrightText: Copyright (c) 2021-2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": False})

import carb
import numpy as np
import omni
import omni.appwindow  # Contains handle to keyboard
import omni.replicator.core as rep

from pxr import Gf
from isaacsim.core.api import World
from isaacsim.core.utils.prims import define_prim
from isaacsim.core.utils.extensions import enable_extension
from isaacsim.robot.policy.examples.robots import AnymalFlatTerrainPolicy
from isaacsim.storage.native import get_assets_root_path

enable_extension("isaacsim.ros2.bridge")
simulation_app.update()


class Anymal_runner(object):
    def __init__(self, physics_dt, render_dt) -> None:
        """
        creates the simulation world with preset physics_dt and render_dt and creates an anymal robot inside the warehouse

        Argument:
        physics_dt {float} -- Physics downtime of the scene.
        render_dt {float} -- Render downtime of the scene.

        """
        # default code
        self._world = World(stage_units_in_meters=1.0, physics_dt=physics_dt, rendering_dt=render_dt)

        assets_root_path = get_assets_root_path()
        if assets_root_path is None:
            carb.log_error("Could not find Isaac Sim assets folder")

        # spawn warehouse scene
        prim = define_prim("/World/Warehouse", "Xform")
        asset_path = assets_root_path + "/Isaac/Environments/Simple_Warehouse/warehouse.usd"
        prim.GetReferences().AddReference(asset_path)

        self._anymal = AnymalFlatTerrainPolicy(
            prim_path="/World/Anymal",
            name="Anymal",
            position=np.array([0, 0, 0.7]),
        )

        self._base_command = np.zeros(3)

        # bindings for keyboard to command
        self._input_keyboard_mapping = {
            # forward command
            "NUMPAD_8": [1.0, 0.0, 0.0],
            "UP": [1.0, 0.0, 0.0],
            # back command
            "NUMPAD_2": [-1.0, 0.0, 0.0],
            "DOWN": [-1.0, 0.0, 0.0],
            # left command
            "NUMPAD_6": [0.0, -1.0, 0.0],
            "RIGHT": [0.0, -1.0, 0.0],
            # right command
            "NUMPAD_4": [0.0, 1.0, 0.0],
            "LEFT": [0.0, 1.0, 0.0],
            # yaw command (positive)
            "NUMPAD_7": [0.0, 0.0, 1.0],
            "N": [0.0, 0.0, 1.0],
            # yaw command (negative)
            "NUMPAD_9": [0.0, 0.0, -1.0],
            "M": [0.0, 0.0, -1.0],
        }
        self.needs_reset = False
        self.first_step = True

        # for lidar prim (match URDF chain: base -> lidar_cage -> lidar)
        self.lidar_parent = "/World/Anymal/base"
        self.lidar_name = "lidar_frame"
        self.hydra_texture = None

    def setup(self) -> None:
        """
        Set up keyboard listener and add physics callback

        """
        self._appwindow = omni.appwindow.get_default_app_window()
        self._input = carb.input.acquire_input_interface()
        self._keyboard = self._appwindow.get_keyboard()
        self._sub_keyboard = self._input.subscribe_to_keyboard_events(self._keyboard, self._sub_keyboard_event)
        self._world.add_physics_callback("anymal_forward", callback_fn=self.on_physics_step)

        self.setup_lidar_ros2()
    
    def setup_lidar_ros2(self):
        _, sensor = omni.kit.commands.execute(
            "IsaacSensorCreateRtxLidar",
            path=self.lidar_name,
            parent=self.lidar_parent,
            config="Example_Rotary",
            translation=(0.35, 0.0, 0.2),  # match URDF lidar_cage_to_lidar
            orientation=Gf.Quatd(1, 0.0, 0.0, 0.0),  # yaw -pi/2
        )

        self.hydra_texture = rep.create.render_product(sensor.GetPath(), [1, 1], name="Isaac")

        # ROS2 PointCloud2 publish
        writer = rep.writers.get("RtxLidarROS2PublishPointCloud")
        writer.initialize(
            topicName="point_cloud",
            frameId="lidar_frame"
        )
        writer.attach([self.hydra_texture])

        # Isaac Sim 내부 debug draw
        debug_writer = rep.writers.get("RtxLidarDebugDrawPointCloud")
        debug_writer.attach([self.hydra_texture])

    def on_physics_step(self, step_size) -> None:
        """
        Physics call back, initialize robot (first frame) and call controller forward function to compute and apply joint torque

        """
        if self.first_step:
            self._anymal.initialize()
            self.first_step = False
        elif self.needs_reset:
            self._world.reset(True)
            self.needs_reset = False
            self.first_step = True
        else:
            self._anymal.forward(step_size, self._base_command)

    def run(self) -> None:
        """
        Step simulation based on rendering downtime

        """
        # change to sim running
        while simulation_app.is_running():
            self._world.step(render=True)
            if self._world.is_stopped():
                self.needs_reset = True
        return

    def _sub_keyboard_event(self, event, *args, **kwargs) -> bool:
        """
        Keyboard subscriber callback to when kit is updated.

        """

        # when a key is pressed for released  the command is adjusted w.r.t the key-mapping
        if event.type == carb.input.KeyboardEventType.KEY_PRESS:
            # on pressing, the command is incremented
            if event.input.name in self._input_keyboard_mapping:
                self._base_command += np.array(self._input_keyboard_mapping[event.input.name])

        elif event.type == carb.input.KeyboardEventType.KEY_RELEASE:
            # on release, the command is decremented
            if event.input.name in self._input_keyboard_mapping:
                self._base_command -= np.array(self._input_keyboard_mapping[event.input.name])
        return True


def main():
    """
    Parse arguments and instantiate the ANYmal runner

    """
    physics_dt = 1 / 200.0
    render_dt = 1 / 60.0

    runner = Anymal_runner(physics_dt=physics_dt, render_dt=render_dt)
    simulation_app.update()
    runner._world.reset()
    simulation_app.update()
    runner.setup()
    simulation_app.update()
    runner.run()
    simulation_app.close()


if __name__ == "__main__":
    main()
