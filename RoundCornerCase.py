from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)
from build123d import *


class RoundCornerCase:
    eps = 0.001
    tol = 0.2

    def __init__(self,
                 size_x = 100.0,
                 size_y = 80.0,
                 size_z = 30.0,
                 outer_r = 7.0,
                 wall_th = 1.6,
                 cover_nut_h = 3.0,
                 screw_hole_dia = 4.0,
                 screw_hole_dep = 4.0):
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.outer_r = outer_r
        self.wall_th = wall_th
        self.cover_nut_h = cover_nut_h
        self.screw_hole_dia = screw_hole_dia
        self.screw_hole_dep = screw_hole_dep
        

    def cover(self):
        size_x = self.size_x
        size_y = self.size_y
        outer_r = self.outer_r
        wall_th = self.wall_th
        cover_nut_h = self.cover_nut_h
        eps = self.eps
        tol = self.tol

        cover = Box(size_x, size_y, wall_th, align=(Align.CENTER, Align.CENTER, Align.MIN))
        cover += Box(size_x - 2*(wall_th + tol), 
                     size_y - 2*(wall_th + tol), 
                     wall_th + cover_nut_h - tol,
                     align=(Align.CENTER, Align.CENTER, Align.MIN))

        vedges = cover.edges().filter_by(Axis.Z)
        iedges = vedges.filter_by_position(Axis.X, 
                                           minimum=size_x/2-wall_th-tol-eps,
                                           maximum=size_x/2-wall_th-tol+eps)
        iedges += vedges.filter_by_position(Axis.X,
                                            minimum=-size_x/2+wall_th+tol-eps, 
                                            maximum=-size_x/2+wall_th+tol+eps)


        cover = fillet(iedges, radius=(outer_r-wall_th-tol-eps))

        vedges = cover.edges().filter_by(Axis.Z)
        oedges = vedges.filter_by_position(Axis.X, minimum=size_x/2-eps, maximum=size_x/2+eps)
        oedges += vedges.filter_by_position(Axis.X, minimum=-size_x/2-eps, maximum=-size_x/2+eps)

        cover = fillet(oedges, radius=outer_r-eps)

        topf = cover.faces().sort_by().last
        cover = offset(cover, openings=topf, amount=-wall_th+eps+tol)

        hole_loc = self._hole_locations()
        hole_sk = Sketch() + [
            Plane.XY * loc * Circle(outer_r-wall_th-tol)
            for loc in hole_loc
        ]
        cover += extrude(hole_sk, wall_th + cover_nut_h - tol)

        screw_dia = 4.1
        holes = Sketch() + [
            loc * CounterBoreHole(radius= screw_dia/2,
    counter_bore_radius = 3.1, counter_bore_depth=2,
    depth = wall_th + cover_nut_h + 2).mirror(Plane.XY)
            for loc in hole_loc
        ]
        cover -= holes

#        show(cover)
#        topf = cover.faces().sort_by().last
#        cover = offset(cover, openings=topf, amount=-wall_th)


        return cover

    def base(self):
        size_x = self.size_x
        size_y = self.size_y
        size_z = self.size_z
        outer_r = self.outer_r
        wall_th = self.wall_th
        cover_nut_h = self.cover_nut_h
        screw_hole_dia = self.screw_hole_dia
        screw_hole_dep = self.screw_hole_dep      
        eps = self.eps

        corner_h = size_z - wall_th - cover_nut_h
        inner_r = outer_r - wall_th
        box = Box(size_x, size_y, size_z, align=(Align.CENTER, Align.CENTER, Align.MIN))
        topf = box.faces().sort_by().last

        box = offset(box, openings=topf, amount=-wall_th)

        ibox = Box(2 * inner_r, 2*inner_r, corner_h, 
                align=(Align.CENTER, Align.CENTER, Align.MIN)).move(Pos(size_x/2-outer_r, size_y/2-outer_r, wall_th))

        ibox += ibox.mirror(Plane.XZ)
        ibox += ibox.mirror(Plane.YZ)
        box +=ibox

        vedges = box.edges().filter_by(Axis.Z)
        iedges = vedges.filter_by_position(Axis.X, minimum=size_x/2-wall_th-(2*inner_r)-eps, maximum=size_x/2-wall_th+eps)
        iedges += vedges.filter_by_position(Axis.X, minimum=-size_x/2+wall_th-eps, maximum=-size_x/2+wall_th+(2*inner_r)+eps)

        box = fillet(iedges, radius=inner_r-eps)

        vedges = box.edges().filter_by(Axis.Z)
        oedges = vedges.filter_by_position(Axis.X, minimum=size_x/2-eps, maximum=size_x/2+eps)
        oedges += vedges.filter_by_position(Axis.X, minimum=-size_x/2-eps, maximum=-size_x/2+eps)

        box = fillet(oedges, radius=outer_r-eps)

        hole_loc = self._hole_locations()
        hole_sk = Sketch() + [
            Plane.XY.offset(size_z-cover_nut_h) * loc * Circle(screw_hole_dia/2)
            for loc in hole_loc
        ]
        box -= extrude(hole_sk, -screw_hole_dep)

        return box

    def _hole_locations(self):
        size_x = self.size_x
        size_y = self.size_y
        wall_th = self.wall_th
        inner_r = self.outer_r - self.wall_th
        return GridLocations(size_x-2*wall_th-2*inner_r, size_y-2*wall_th-2*inner_r, 2, 2)

if __name__ == '__main__':
    case = RoundCornerCase()
    show(case.base().move(Pos(0,100)),
         case.cover())