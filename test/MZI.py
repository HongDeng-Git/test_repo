from technologies import silicon_photonics
import ipkiss3.all as i3

from picazzo3.routing.place_route import PlaceAndAutoRoute
from directional_coupler import DC
from picazzo3.traces.wire_wg import WireWaveguideTemplate

class MZI_for_DC_test(PlaceAndAutoRoute):
    _name_prefix = "MZI_test"
    
    splitter = i3.ChildCellProperty()
    combiner = i3.ChildCellProperty()
    
    trace_template = i3.ChildCellProperty()
    cp = i3.ChildCellProperty(doc = "control_point")
    
    def _default_splitter(self):
        return DC(name = self.name + "DC", trace_template = self.trace_template)
    def _default_combiner(self):
        return self.splitter
    
    def _default_trace_template(self):
        return WireWaveguideTemplate()
    
    def _default_cp(self):
        return i3.Waveguide(trace_template = self.trace_template)
    
    def _default_child_cells(self):
        
        cc = {}
        cc["splitter"] = self.splitter
        cc["combiner"] = self.combiner
        cc["cp"] = self.cp
        return cc
    
    def _default_links(self):
        links = [("splitter:out1", "combiner:in1"),
                 ( "splitter:out2", "cp:in"), ("cp:out", "combiner:in2")]
        return links
    def _default_external_port_names(self):
        epn = {}
        epn["splitter:in1"] = "in1"
        epn["splitter:in2"] = "in2"
        epn["combiner:out1"] = "out1"
        epn["combiner:out2"] = "out2"
        return epn
    
    
    class Layout(PlaceAndAutoRoute.Layout):
        
        coupling_length = i3.NonNegativeNumberProperty(doc="DC_straight_coupling_length")
        coupling_gap = i3.PositiveNumberProperty(doc="DC_Center_to_center distence")
        
        def _default_coupling_length(self):
            return 15.0
        def _default_coupling_gap(self):
            return 0.68
        def _default_trace_template(self):
            tt = self.cell.trace_template.get_default_view(self)
            tt.set(core_width = 0.45, core_process=i3.TECH.PROCESS.WG)
            return tt
        def _default_combiner(self):
            temp =  self.cell.combiner.get_default_view(self)
            temp.set(coupling_length = self.coupling_length, coupling_gap = self.coupling_gap)
            return temp
        def _default_splitter(self):
            temp =  self.cell.splitter.get_default_view(self)
            temp.set(coupling_length = self.coupling_length, coupling_gap = self.coupling_gap)
            return temp
        def _default_cp(self):
            temp =  self.cell.cp.get_default_view(self)
            temp.set(shape = [(0, 0), (1, 0)])
            return temp          
            
        def _default_manhattan(self):
            return True
        def _default_bend_radius(self):
            return 10
        def _default_rounding_algorithm(self):
            return i3.SplineRoundingAlgorithm()
        def _default_min_straight(self):
            return 0.0
        
        def _default_child_transformations(self):
            return {
                "splitter": (0, 0),
                "combiner": i3.HMirror() +i3.VMirror() + i3.Translation((0, -40)),
                "cp": i3.Rotation(rotation=-90) + i3.Translation((50, -20)),     
            }
        
        
    
if __name__ == "__main__":
    
    test = MZI_for_DC_test()
    test_lo = test.Layout()
    test_lo.write_gdsii("test.gds")
    #test_lo.visualize(annotate = True)
    print "down"