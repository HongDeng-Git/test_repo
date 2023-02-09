from technologies import silicon_photonics
import ipkiss3.all as i3
from picazzo3.traces.wire_wg import WireWaveguideTemplate

class StraightDC(i3.PCell):
    
    _name_prefix = "straight_DC"
    
    trace_template = i3.ChildCellProperty(doc="used_waveguide_template")
    wg = i3.ChildCellProperty(doc="the wg")
    
    def _default_trace_template(self):
        return WireWaveguideTemplate()
    
    def _default_wg(self):
        return i3.Waveguide(trace_template = self.trace_template)
    
    class Layout(i3.LayoutView):
        
        coupling_length = i3.NonNegativeNumberProperty(doc="straight_coupling_length")
        coupling_gap = i3.PositiveNumberProperty(doc="Center_to_center distence")
        
        def _default_coupling_length(self):
            return 15.0
        def _default_coupling_gap(self):
            return 0.68
        
        def _default_trace_template(self):
            tt = self.cell.trace_template.get_default_view(self)
            tt.set(core_width = 0.45, core_process=i3.TECH.PROCESS.WG)
            return tt
        def _default_wg(self):
            temp = self.cell.wg.get_default_view(self)
            temp.set(shape = [(-self.coupling_length / 2, 0), (self.coupling_length / 2, 0) ])
            return temp
        
        def _generate_instances(self, insts):
            
            insts += i3.SRef(self.wg, position=(0.0,self.coupling_gap/2))
            insts += i3.SRef(self.wg, position=(0.0, -self.coupling_gap/2))
            return insts
        def _generate_ports(self, ports):
            ports += i3.OpticalPort(name = "in1", position = (-self.coupling_length/2, -self.coupling_gap/2), angle_deg = 180, trace_template = self.trace_template)
            ports += i3.OpticalPort(name = "in2", position = (-self.coupling_length/2, +self.coupling_gap/2), angle_deg = 180, trace_template = self.trace_template)
            ports += i3.OpticalPort(name = "out1", position = (self.coupling_length/2, -self.coupling_gap/2),  trace_template = self.trace_template)
            ports += i3.OpticalPort(name = "out2", position = (self.coupling_length/2, +self.coupling_gap/2),  trace_template = self.trace_template)
            return ports
        
    class Netlist(i3.NetlistView):
        pass

from picazzo3.routing.place_route import PlaceAndConnect

class DC(PlaceAndConnect):
    _name_prefix = "DC"
    
    Straight_DC = i3.ChildCellProperty(doc="coupler")
    wg_in1 = i3.ChildCellProperty()
    wg_in2 = i3.ChildCellProperty()
    wg_out1 = i3.ChildCellProperty()
    wg_out2 = i3.ChildCellProperty()
    trace_template = i3.ChildCellProperty(doc="used trace template")
    
    def _default_Straight_DC(self):
        return StraightDC(trace_template = self.trace_template)
    def _default_wg_in1(self):
        return i3.RoundedWaveguide(name = "trace_in1", trace_template = self.trace_template)
    def _default_wg_in2(self):
        return i3.RoundedWaveguide(name = "trace_in2", trace_template = self.trace_template)
    def _default_wg_out1(self):
        return i3.RoundedWaveguide(name = "trace_out1", trace_template = self.trace_template)
    def _default_wg_out2(self):
        return i3.RoundedWaveguide(name = "trace_out2", trace_template = self.trace_template)
    def _default_trace_template(self):
        return WireWaveguideTemplate()
    def _default_child_cells(self):
        cc = {}
        cc["dc"] = self.Straight_DC
        cc["wg_in1"] = self.wg_in1
        cc["wg_in2"] = self.wg_in1
        cc["wg_out1"] = self.wg_in1
        cc["wg_out2"] = self.wg_in1
        
        return cc
    def _default_links(self):
        links = []
        links.append(("wg_in1:in", "dc:in1"))
        links.append(("wg_in2:in", "dc:in2"))
        links.append(("wg_out1:in", "dc:out1"))
        links.append(("wg_out2:in", "dc:out2"))
        return links
    def _default_external_port_names(self):
        
        epn = {}
        epn["in1"] = "wg_in1:in"
        epn["in2"] = "wg_in2:in"
        epn["out1"] = "wg_out1:out"
        epn["out2"] = "wg_out2:out"
        return epn
    
    class Layout(PlaceAndConnect.Layout):
        coupling_length = i3.NonNegativeNumberProperty(doc="straight_coupling_length")
        coupling_gap = i3.PositiveNumberProperty(doc="Center_to_center distence")
        
        def _default_coupling_length(self):
            return 15.0
        def _default_coupling_gap(self):
            return 0.68
        
        def _default_trace_template(self):
            tt = self.cell.trace_template.get_default_view(self)
            tt.set(core_width = 0.45, core_process=i3.TECH.PROCESS.WG)
            return tt
        def _default_Straight_DC(self):
            temp = self.cell.Straight_DC.get_default_view(self)
            temp.set(coupling_length = self.coupling_length,
                     coupling_gap = self.coupling_gap)
            return temp        
        def _default_wg_in1(self):
            temp = self.cell.wg_in1.get_default_view(self)
            temp.set(manhattan=True,
                     rounding_algorithm=i3.SplineRoundingAlgorithm(), 
                     bend_radius=10.0,
                     shape=[(-5, 0), (0, 0), (6, -6), (11, -6)], 
            )
            return temp 
        def _default_wg_in2(self):
            temp = self.cell.wg_in2.get_default_view(self)
            temp.set(manhattan=True,
                     rounding_algorithm=i3.SplineRoundingAlgorithm(), 
                     bend_radius=10.0,
                     shape=[(-20, 0), (0, 0), (0, 20), (20, 20)], 
            )
            return temp 
        def _default_wg_out1(self):
            temp = self.cell.wg_out1.get_default_view(self)
            temp.set(manhattan=True,
                     rounding_algorithm=i3.SplineRoundingAlgorithm(), 
                     bend_radius=10.0,
                     shape=[(-20, 0), (0, 0), (0, -20), (20, -20)],
                     )
            return temp
        def _default_wg_out2(self):
            temp = self.cell.wg_out2.get_default_view(self)
            temp.set(manhattan=True,
                     rounding_algorithm=i3.SplineRoundingAlgorithm(), 
                     bend_radius=10.0,
                     shape=[(-20, 0), (0, 0), (0, 20), (20, 20)],
                     )
            return temp
        def _default_child_transformations(self):
            
            wg_in_x = self.wg_in1.ports["in"].x
            wg_in_y = self.wg_in1.ports["in"].y
            wg_out_x = self.wg_in1.ports["out"].x
            wg_out_y = self.wg_in1.ports["out"].y             
            
            return {"dc": (0, 0),
                    "wg_in1": i3.HMirror()+ i3.Translation(translation=(+wg_in_x-self.coupling_length/2, -self.coupling_gap/2)) ,
                    "wg_in2": i3.HMirror()+ i3.VMirror() + i3.Translation(translation=(+wg_in_x-self.coupling_length/2, +self.coupling_gap/2)) ,
                    "wg_out1": i3.Translation(translation=(-wg_in_x+self.coupling_length/2, -self.coupling_gap/2)),
                    "wg_out2": i3.VMirror() +i3.Translation(translation=(-wg_in_x+self.coupling_length/2, +self.coupling_gap/2)),
                    }
    
    
    
    
    
if __name__ == "__main__":
    temp = DC()
    temp_lo = temp.Layout()
    #temp_lo.visualize(annotate = True)
    temp_lo.write_gdsii("test.gds")
    print "down"