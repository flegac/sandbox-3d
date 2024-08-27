from enum import Enum, auto

from procedural_gen.region.vec import Vec


class Symmetry(Enum):
    default = auto()
    left_low = auto()
    right_low = auto()

    left_up = auto()
    right_up = auto()

    def select[T](self, left: T, right: T) -> T:
        match self:
            case Symmetry.left_low:
                return left
            case Symmetry.right_low:
                return right
            case Symmetry.left_up:
                return left
            case Symmetry.right_up:
                return right

    def mirror_value(self) -> float:
        return self.select(1, -1)

    def reverse(self):
        match self:
            case Symmetry.left_low:
                return Symmetry.right_low
            case Symmetry.right_low:
                return Symmetry.left_low
            case Symmetry.left_up:
                return Symmetry.right_up
            case Symmetry.right_up:
                return Symmetry.left_up

    @property
    def direction(self):
        match self:
            case Symmetry.left_low:
                return -Vec.x_axis()
            case Symmetry.left_up:
                return -Vec.x_axis()

            case Symmetry.right_low:
                return Vec.x_axis()
            case Symmetry.right_up:
                return Vec.x_axis()
        raise NotImplementedError(f'{self}')
