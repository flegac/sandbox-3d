from typing import override

import math
from pydantic import model_validator

from procedural_gen.region.vec import Vec
from sandbox_core.controls.params.float_param import FloatParam
from sandbox_core.controls.params.vec_param import VecParam
from sandbox_creature.behavior.behavior import Behavior
from sandbox_creature.core.symmetry import Symmetry

MAX_LATERAL_BALANCE = 1


class WalkBehavior(Behavior):
    @model_validator(mode='after')
    def post_init(self):
        self.config.with_vec(
            'hips_opening', VecParam.create(
                value=Vec(),
                low=Vec.at(-10, -85, -45),
                high=Vec.at(85, 85, 5),
                speed=Vec.cast(3)
            )
        ).with_vec(
            'balance', VecParam.create(
                value=Vec(),
                low=Vec.at(-45, -120, 0),
                high=Vec.at(45, 120, 0),
                speed=Vec.cast(3)
            )
        ).with_param(
            'knee_flexion', FloatParam(current=5, low=5, high=155, max_speed=10)
        ).with_param(
            'torso_flexion', FloatParam(current=0, low=-100, high=100, max_speed=5)
        ).with_param(
            'foot_balance', FloatParam(current=0, low=-.98, high=.98, max_speed=5)
        ).with_param(
            'forward', FloatParam(current=0, low=-1000, high=1000, max_speed=.1)
        ).with_param(
            'side', FloatParam(current=0, low=-1, high=1, max_speed=2)
        )
        return self

    def hips(self, side: Symmetry):
        return self.skeleton.single_joint(f'hips {side.name}')

    def knee(self, side: Symmetry):
        return self.skeleton.single_joint(f'knee {side.name}')

    def ankle(self, side: Symmetry):
        return self.skeleton.single_joint(f'ankle {side.name}')

    def lateral_balance(self, offset: float = 0):
        forward = self.config.params['forward']
        lateral_balance = MAX_LATERAL_BALANCE * math.sin(2 * math.pi * (forward.current * .05 + offset))
        # print(f'f:{forward.value:.2f} -> {lateral_balance}')
        return lateral_balance

    def walk_lateral(self, offset: float = 0):
        lateral_balance = self.lateral_balance(offset)
        normalized_center_delta = self.skeleton.normalized_balance(self.skeleton.mass_center)
        delta = lateral_balance - normalized_center_delta.x
        self.config.params['balance.x'].add_value(.1 * delta)

    def walk_hips(self, offset: float = 0):
        lateral_balance = self.lateral_balance(offset)
        opening = self.config.params['hips_opening.y']
        opening.set_value(20 * lateral_balance)

    def walk_knee(self, offset: float = 0):
        lateral_balance = self.lateral_balance(offset)
        self.config.params['side'].set_value(lateral_balance)

    @override
    def update(self):
        for shoulder in self.skeleton.search_joint('shoulder'):
            self.config.params[f'{shoulder.tags}.z'].set_value(90)

        self.config.update()

        # self.walk_lateral()
        # self.walk_hips()
        self.walk_knee()

        for side in [Symmetry.left_low, Symmetry.right_low]:
            self.handle_knee_flexion(side)
            self.handle_hips_opening(side)

            self.handle_balance(side)
            self.handle_ankle(side)
        self.handle_torso()

    def handle_knee_flexion(self, side: Symmetry):
        flexion = 0
        if side.mirror_value() * self.config.float('side') < 0:
            flexion = 40 * abs(self.config.float('side'))

        self.knee(side).current.y = self.config.float('knee_flexion') + flexion

    def handle_hips_opening(self, side: Symmetry):
        hips = self.hips(side)

        opening_x = self.config.float('hips_opening.x')
        opening_y = self.config.float('hips_opening.y') * side.mirror_value()
        opening_z = self.config.float('hips_opening.z') * side.mirror_value()
        knee_y = self.knee(side).current.y

        hips.current.x = opening_z
        hips.current.y = - .5 * knee_y - opening_y
        hips.current.z = opening_x

    def handle_balance(self, side: Symmetry):
        hips = self.hips(side)
        knee = self.knee(side)
        side_balance = self.config.params['balance.x']

        foot_balance = self.config.float('foot_balance')
        normalized_center_delta = self.extra.normalized_balance(self.skeleton.mass_center)

        # correct lateral balance
        delta = foot_balance - normalized_center_delta.x
        side_balance.add_value(.2 * delta)

        # lateral balance
        balance_delta = side_balance.current * side.mirror_value()

        foot_distance = self.extra.foot_delta().x
        if balance_delta > 0:
            k = 4 * foot_distance
        else:
            k = -10 * foot_distance
            knee.current.y += 2 * k * balance_delta
            hips.current.y -= k * balance_delta

        hips.current.z += 4 * balance_delta

    def handle_ankle(self, side: Symmetry):
        hips = self.hips(side)
        knee = self.knee(side)
        ankle = self.ankle(side)

        opening_y = self.config.float('hips_opening.y') * side.mirror_value()
        ankle.current.y = -.5 * knee.current.y + opening_y
        ankle.current.z = hips.current.z * side.mirror_value()

    def handle_torso(self):
        torso_flexion = self.config.float('torso_flexion')

        for hips in self.skeleton.search_joint('hips'):
            hips.current.y += torso_flexion

        # frontal balance
        spinal_coef = -.15
        for joint in self.skeleton.search_joint('spinal_disc'):
            joint.current.y = spinal_coef * torso_flexion
