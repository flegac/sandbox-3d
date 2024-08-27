from sandbox_creature.core.skeleton import Skeleton
from sandbox_lib.humanoid.bones.abdomen import Abdomen
from sandbox_lib.humanoid.bones.head import Head
from sandbox_lib.humanoid.bones.neck import Neck
from sandbox_lib.humanoid.bones.pelvis import Pelvis
from sandbox_lib.humanoid.bones.torso import Torso
from sandbox_lib.humanoid.bones.walk_support import WalkSupport
from sandbox_lib.humanoid.limbs import Limbs
from procedural_gen.region.vec import Vec


class Humanoid(Skeleton):

    def create(self, origin: Vec):
        pelvis = Pelvis.new(
            self,
            origin=origin,
            size=Vec.at(.31, .13, .13)
        )


        abdomen = Abdomen.new(
            self,
            origin=pelvis.at('end'),
            size=Vec.at(.25, .10, .15)
        )
        torso = Torso.new(
            self,
            origin=abdomen.at('end'),
            size=Vec.at(.35, .15, .35)
        )
        neck = Neck.new(self, torso.at('end'))
        head = Head.new(self, neck.at('end'))

        Limbs.lower(self, pelvis)
        Limbs.upper(self, torso)

        # self.left_foot.phys.density = 0
        # self.pelvis.phys.density = 0
        # self.pelvis.phys.density=0

        return self
