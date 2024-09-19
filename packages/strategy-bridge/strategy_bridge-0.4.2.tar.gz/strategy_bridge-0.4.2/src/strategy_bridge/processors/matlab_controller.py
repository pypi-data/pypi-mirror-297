import attr
import numpy as np

from strategy_bridge.bus import DataReader, DataWriter, DataBus
from strategy_bridge.common import config
from strategy_bridge.matlab.engine import matlab_engine
from strategy_bridge.model.referee import RefereeCommand
from strategy_bridge.processors import BaseProcessor


# TODO: Refactor this class and corresponding matlab scripts
from strategy_bridge.utils.debugger import debugger


@attr.s(auto_attribs=True)
class MatlabController(BaseProcessor):

    max_commands_to_persist: int = 20

    vision_reader: DataReader = attr.ib(init=False)
    referee_reader: DataReader = attr.ib(init=False)
    commands_writer: DataWriter = attr.ib(init=False)

    CAMERAS_COUNT: int = 4
    MAX_BALLS_IN_CAMERA: int = 64
    MAX_BALLS_IN_FIELD: int = CAMERAS_COUNT * MAX_BALLS_IN_CAMERA
    BALL_PACKET_SIZE: int = 3

    ROBOTS_MAX_COUNT: int = 32
    TEAM_ROBOTS_MAX_COUNT: int = ROBOTS_MAX_COUNT // 2
    SINGLE_ROBOT_PACKET_SIZE = 5
    ROBOT_TEAM_PACKET_SIZE: int = SINGLE_ROBOT_PACKET_SIZE * TEAM_ROBOTS_MAX_COUNT

    GEOMETRY_PACKET_SIZE: int = 2

    def initialize(self, data_bus: DataBus) -> None:
        super(MatlabController, self).initialize(data_bus)
        self.vision_reader = DataReader(self.data_bus, config.VISION_DETECTIONS_TOPIC)
        self.referee_reader = DataReader(self.data_bus, config.REFEREE_COMMANDS_TOPIC)
        self.commands_writer = DataWriter(self.data_bus, config.ROBOT_COMMANDS_TOPIC, self.max_commands_to_persist)

    def get_last_referee_command(self) -> RefereeCommand:
        referee_commands = self.referee_reader.read_new()
        if referee_commands:
            return referee_commands[-1].content
        return RefereeCommand(0, 0, False)

    @debugger
    def process(self) -> None:
        balls = np.zeros(self.BALL_PACKET_SIZE * self.MAX_BALLS_IN_FIELD)
        robots_blue = np.zeros(self.ROBOT_TEAM_PACKET_SIZE)
        robots_yellow = np.zeros(self.ROBOT_TEAM_PACKET_SIZE)
        field_info = np.zeros(self.GEOMETRY_PACKET_SIZE)

        for ssl_record in self.vision_reader.read_new():
            ssl_package = ssl_record.content
            geometry = ssl_package.geometry
            if geometry:
                field_info[0] = geometry.field.field_length
                field_info[1] = geometry.field.field_width

            detection = ssl_package.detection
            if not detection:
                continue

            camera_id = detection.camera_id
            for ball_ind, ball in enumerate(detection.balls):
                balls[ball_ind + (camera_id - 1) * self.MAX_BALLS_IN_CAMERA] = camera_id
                balls[ball_ind + self.MAX_BALLS_IN_FIELD + (camera_id - 1) * self.MAX_BALLS_IN_CAMERA] = ball.x
                balls[ball_ind + 2 * self.MAX_BALLS_IN_FIELD + (camera_id - 1) * self.MAX_BALLS_IN_CAMERA] = ball.y

            # TODO: Barrier states
            for robot in detection.robots_blue:
                robots_blue[robot.robot_id] = camera_id
                robots_blue[robot.robot_id + self.TEAM_ROBOTS_MAX_COUNT] = robot.x
                robots_blue[robot.robot_id + self.TEAM_ROBOTS_MAX_COUNT * 2] = robot.y
                robots_blue[robot.robot_id + self.TEAM_ROBOTS_MAX_COUNT * 3] = robot.orientation

            for robot in detection.robots_yellow:
                robots_yellow[robot.robot_id] = camera_id
                robots_yellow[robot.robot_id + self.TEAM_ROBOTS_MAX_COUNT] = robot.x
                robots_yellow[robot.robot_id + self.TEAM_ROBOTS_MAX_COUNT * 2] = robot.y
                robots_yellow[robot.robot_id + self.TEAM_ROBOTS_MAX_COUNT * 3] = robot.orientation

            referee_command = self.get_last_referee_command()
            rules = await matlab_engine.run_function(
                "main_func",
                robots_blue.reshape(self.TEAM_ROBOTS_MAX_COUNT, self.SINGLE_ROBOT_PACKET_SIZE).tolist(),
                robots_yellow.reshape(self.TEAM_ROBOTS_MAX_COUNT, self.SINGLE_ROBOT_PACKET_SIZE).tolist(),
                balls.tolist(),
                field_info.tolist(),
                [referee_command.state],
                [referee_command.commandForTeam],
                [referee_command.isPartOfFieldLeft]
            )
            self.commands_writer.write(rules)
