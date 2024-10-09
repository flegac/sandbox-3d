from pydantic import model_validator

from easy_config.my_model import MyModel
from sandbox_lib.humanoid.section import Section
from procedural_gen.region.vec import Vec


class Spines(MyModel):
    sections: list[Section] = [
        Section.from_size(width=.25, depth=.10, offset=.0),
        Section.from_size(width=.25, depth=.10, offset=1),
    ]
    number: int = 1
    length: float = .15

    @property
    def part_length(self):
        return self.length / self.number

    def interpolate(self, x: float):
        for idx, section in enumerate(self.sections):
            next_section = self.sections[idx + 1]
            if section.offset <= x <= next_section.offset:
                length = next_section.offset - section.offset
                offset = (x - section.offset) / length
                return section.size * (1 - offset) + next_section.size * offset

    def spine_size(self, i: int):
        if self.number == 1:
            x = 0
        else:
            x = i / (self.number - 1)
        return self.interpolate(x) + Vec.z_axis() * self.part_length

    @model_validator(mode='after')
    def check_sections(self):
        offset = 0
        for section in self.sections:
            if section.offset < offset:
                raise ValueError(f'Unsorted section offsets: {self.sections}')
            offset = section.offset
        return self
