from pymeasure.instruments import Instrument, SCPIMixin
from pymeasure.adapters import VISAAdapter

class PM101U(SCPIMixin, Instrument):
    power = Instrument.measurement("MEAS:SCAL:POW?", 
                                   """Get the power""")
    
    wavelength = Instrument.control("SENS:CORR:WAV?", 
                                    "SENS:CORR:WAV %g", 
                                    """Set/read wavelength""")
    
    dark_offset = Instrument.measurement("SENS:CORR:COLL:ZERO:MAGN?", 
                                         "Get dark offset")
    
    def __init__(self, adapter: VISAAdapter, **kwargs):
        super().__init__(adapter, "PM101U", **kwargs)
        
    def zero(self):
        self.write("SENS:CORR:COLL:ZERO:INIT")
