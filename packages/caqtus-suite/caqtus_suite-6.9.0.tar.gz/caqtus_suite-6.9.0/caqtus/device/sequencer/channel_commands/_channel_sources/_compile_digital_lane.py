import numpy as np

import caqtus.formatter as fmt
from caqtus.device.sequencer.instructions import (
    SequencerInstruction,
    Pattern,
    concatenate,
)
from caqtus.shot_compilation.compilation_contexts import ShotContext
from caqtus.types.expression import Expression
from caqtus.types.recoverable_exceptions import InvalidTypeError
from caqtus.types.timelane import DigitalTimeLane
from ...timing import number_time_steps_between, TimeStep


def compile_digital_lane(
    lane: DigitalTimeLane,
    time_step: TimeStep,
    shot_context: ShotContext,
) -> SequencerInstruction[np.bool_]:
    step_names = shot_context.get_step_names()
    if len(lane) != len(step_names):
        raise ValueError(
            f"Number of steps in lane ({len(lane)}) does not match number of"
            f" steps ({len(step_names)})"
        )

    step_bounds = shot_context.get_step_start_times()
    instructions = []
    for cell_value, (start, stop) in zip(
        lane.block_values(), lane.block_bounds(), strict=True
    ):
        length = number_time_steps_between(
            step_bounds[start], step_bounds[stop], time_step
        )
        if isinstance(cell_value, bool):
            instructions.append(get_constant_instruction(cell_value, length))
        elif isinstance(cell_value, Expression):
            value = cell_value.evaluate(shot_context.get_variables())
            if not isinstance(value, bool):
                raise InvalidTypeError(
                    f"{fmt.expression(cell_value)} does not evaluate to "
                    f"{fmt.type_(bool)}, but to {fmt.type_(type(value))}",
                )
            instructions.append(get_constant_instruction(value, length))

        else:
            raise NotImplementedError(f"Unexpected value {cell_value} in digital lane")
    return concatenate(*instructions)


def get_constant_instruction(
    value: bool, length: int
) -> SequencerInstruction[np.bool_]:
    return Pattern([value]) * length


#
# elif isinstance(cell_value, Blink):
# period = (
#     cell_value.period.evaluate(variables | units).to("ns").magnitude
# )
# duty_cycle = (
#     Quantity(cell_value.duty_cycle.evaluate(variables | units))
#     .to(dimensionless)
#     .magnitude
# )
# if not 0 <= duty_cycle <= 1:
#     raise ShotEvaluationError(
#         f"Duty cycle '{cell_value.duty_cycle.body}' must be between 0 and"
#         f" 1, not {duty_cycle}"
#     )
# num_ticks_per_period, _ = divmod(period, time_step)
# num_ticks_high = math.ceil(num_ticks_per_period * duty_cycle)
# num_ticks_low = num_ticks_per_period - num_ticks_high
# num_clock_pulses, remainder = divmod(length, num_ticks_per_period)
# phase = (
#     Quantity(cell_value.phase.evaluate(variables | units))
#     .to(dimensionless)
#     .magnitude
# )
# if not 0 <= phase <= 2 * math.pi:
#     raise ShotEvaluationError(
#         f"Phase '{cell_value.phase.body}' must be between 0 and 2*pi, not"
#         f" {phase}"
#     )
# split_position = round(phase / (2 * math.pi) * num_ticks_per_period)
# clock_pattern = (
#         Pattern([True]) * num_ticks_high + Pattern([False]) * num_ticks_low
# )
# a, b = clock_pattern[:split_position], clock_pattern[split_position:]
# clock_pattern = b + a
# pattern = (
#         clock_pattern * num_clock_pulses + Pattern([False]) * remainder
# )
# if not len(pattern) == length:
#     raise RuntimeError(
#         f"Pattern length {len(pattern)} does not match expected length"
#         f" {length}"
#     )
# print(f"{pattern=}")
