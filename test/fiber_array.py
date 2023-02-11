from technologies import silicon_photonics
import ipkiss3.all as i3

from picazzo3.fibcoup.curved.cell import FiberCouplerCurvedGrating
from picazzo3.routing.place_route import PlaceAndAutoRoute
from picazzo3.traces.wire_wg import WireWaveguideTemplate

class Fiber_Array(PlaceAndAutoRoute):

    _name_prefix = "Fiber_array"

    n_o_channels = i3.PositiveIntProperty(default=10)
    gc = i3.ChildCellProperty()
    shunt_waveguide = i3.ChildCellProperty(doc="waveguide for the shunt")
    trace_template = i3.WaveguideTemplateProperty(doc="waveguide template")
    
    def _default_trace_template(self):
        return WireWaveguideTemplate()
    
    def _default_shunt_waveguide(self):
        return i3.RoundedWaveguide(name=self.name+"shunt",
                                   trace_template=self.trace_template)
    
    def _default_gc(self):
        return  FiberCouplerCurvedGrating()

    def _default_child_cells(self):
        k = {}
        for i in range(0, self.n_o_channels):
            k['gc{}'.format(i)] = self.gc
        k["shunt"] = self.shunt_waveguide
        return k

    def _default_links(self):
        return [("gc0:out", "shunt:in"),
                ("gc{}:out".format(self.n_o_channels-1), "shunt:out")]

    def _default_external_port_names(self):
        prt = {}
        for i in range(0, self.n_o_channels)[1:-1]:
            prt["gc{}:out".format(i)] = "out{}".format(i)
        return prt


    class Layout(PlaceAndAutoRoute.Layout):

        pitch = i3.PositiveNumberProperty(default=127)


        def _default_shunt_waveguide(self):
            length = (self.n_o_channels -1) * self.pitch
            temp =  self.cell.shunt_waveguide.get_default_view(self)
            temp.set(shape = [(0, 0), (length, 0)])
            return temp          

        def _default_child_transformations(self):
            ct = {}
            for i in range(self.n_o_channels):
                ct["gc{}".format(i)] = i3.Translation((0, self.pitch * i))
                
            ct["shunt"] = i3.Rotation(rotation=90.0) + i3.Translation(translation=(-40,0.0))
            return ct

        def _default_rounding_algorithm(self):
            return i3.SplineRoundingAlgorithm()

        def _default_manhattan(self):
            return True
        
        def _default_min_straight(self):
            return 10.0

       

if __name__ == "__main__":
    temp = Fiber_Array()
    temp_lo = temp.Layout()
    #temp_lo.visualize(annotate = True)
    temp_lo.write_gdsii("test.gds")
    print "down"