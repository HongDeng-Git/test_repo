from technologies import silicon_photonics
import ipkiss3.all as i3

from picazzo3.fibcoup.curved.cell import FiberCouplerCurvedGrating
from picazzo3.routing.place_route import PlaceAndAutoRoute
from picazzo3.traces.wire_wg import WireWaveguideTemplate
from directional_coupler import DC
from MZI import MZI_for_DC_test
from fiber_array import Fiber_Array

class Top_cell_for_DC_test(PlaceAndAutoRoute):
    
    _name_prefix = "DC_test_top_cell"
    
    FA = i3.ChildCellProperty(doc = "Fiber Array")
    dc = i3.ChildCellProperty(doc="DC")
    MZI = i3.ChildCellProperty(doc="MZI")
    
    cp = i3.ChildCellProperty(doc="control point")
    
    def _default_trace_template(self):
        return WireWaveguideTemplate()
    
    def _default_FA(self):
        return Fiber_Array(name = self.name + "FA", n_o_channels = 6)
    
    def _default_dc(self):
        return DC(name = self.name + "dc")
    
    def _default_MZI(self):
        return MZI_for_DC_test(name = self.name + "MZI")
    
    def _default_cp(self):
        return i3.Waveguide(trace_template = self.trace_template)
    
    def _default_child_cells(self):
        
        cc = {}
        cc["FA1"] = self.FA
        cc["FA2"] = self.FA
        cc["dc"] = self.dc
        cc["MZI"] = self.MZI
        
        return cc
    
    def _default_links(self):
        links = []
        links.extend([("FA1:out1", "dc:in1"), ("FA1:out2", "dc:in2"), ("FA1:out3", "dc:out2"), ("FA1:out4", "MZI:in2")])
        links.extend([("FA2:out1", "dc:out1"), ("FA2:out2", "MZI:out2"), ("MZI:out1", "FA2:out3" ), ("MZI:in1", "FA2:out4")])
        return links
    
    class Layout(PlaceAndAutoRoute.Layout):
        
        def _default_manhattan(self):
            return True
        def _default_bend_radius(self):
            return 10
        def _default_rounding_algorithm(self):
            return i3.SplineRoundingAlgorithm()
        def _default_min_straight(self):
            return 0.0
        
        def _default_child_transformations(self):
            
            ct = {}
            ct["FA1"] = (0, 0)
            ct["FA2"] = i3.HMirror() + i3.Translation(translation=(500.0,0.0))
            ct["dc"] = (80, 170)
            ct["MZI"] = i3.HMirror() + i3.Translation(translation=(100.0,450.0))
            return ct
        
if __name__ == "__main__":
            
    test = Top_cell_for_DC_test()
    test_lo = test.Layout()
    test_lo.write_gdsii("test.gds")
    #test_lo.visualize(annotate = True)
    print "down"            