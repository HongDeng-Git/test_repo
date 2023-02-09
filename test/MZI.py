from technologies import silicon_photonics
import ipkiss3.all as i3

from picazzo3.routing.place_route import PlaceAndAutoRoute
from picazzo3.filters.mmi import MMI2x2
from directional_coupler import DC
from picazzo3.traces.wire_wg import WireWaveguideTemplate

class MZI_test(PlaceAndAutoRoute):
    _name_prefix = "MZI_test"
    
    splitter = i3.ChildCellProperty()
    combiner = i3.ChildCellProperty()
    
    trace_template = i3.ChildCellProperty()
    cp = i3.ChildCellProperty(doc = "control_point")
    
    def _default_splitter(self):
        return MMI2x2(mmi_trace_template=self.trace_template,)
    def _default_combiner(self):
        return DC(name = self.name + "DC", trace_tempalte = self.trace_template)
    
    def _default_trace_template(self):
        return WireWaveguideTemplate()
    
    def _default_cp(self):
        return i3.Waveguide(trace_template = self.trace_template)
    
    
    class Layout(MZI.Layout):
        
        def _default_arm1(self):
            temp = self.cell.arm1.get_default_view(self)
            temp.set(extra_length = 20)
            return temp
        def _default_combiner_transformation(self):
            return i3.VMirror() + i3.Translation((100.0, 0.0))
    
if __name__ == "__main__":
    
    test = MZI_test()
    test_lo = test.Layout()
    test_lo.visualize(annotate = True)
    print "down"