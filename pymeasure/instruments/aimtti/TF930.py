from enum import Enum
from pymeasure.instruments import Instrument, SCPIMixin
from pymeasure.instruments.validators import strict_discrete_set, strict_discrete_range

class TF930(SCPIMixin, Instrument):
    class TF930MasurementFunctions(Enum):
        BInputPeriod = 0
        AInputPeriod = 1
        AInputFrequency = 2
        BInputFrequency = 3
        FreqeuncyRatioBA = 4
        AInputWidthHigh = 5
        AInputWidthLow = 6
        AInputCount = 7
        AInputRatioHL = 8
        AInputDutyCycle = 9

    measurement_function = Instrument.setting("F%i",
                                              """Sets the measurement function""",
                                              validator = strict_discrete_set,
                                              values= TF930MasurementFunctions,
                                              set_process = lambda v: v.value)
    
    threshold_ac = Instrument.control("TO?",
                                      "TO%i",
                                      """Use with AC coupling. Threshold automatically adjusts to the average level of the waveform
                                        being measured, offset by <nr1> mV, where <nr1> is a number in the range -60 to +60; if
                                        no sign is present, <nr1> is assumed to be positive.""",
                                      validator=strict_discrete_set,
                                      values = range(-60, 61),
                                      get_process = lambda v: v.replace('mV', ''),
                                      cast = float)
    
    threshold_dc = Instrument.control("TT?",
                                      "TT%i",
                                      """Use with DC coupling. Threshold set to a level of <nr1> mV, where <nr1> is a number in
                                        the range -300 to +2100; if no sign is present, <nr1> is assumed to be positive.""",
                                      validator=strict_discrete_set,
                                      values = range(-300, 2101),
                                      get_process = lambda v: v.replace('mV', ''),
                                      cast = float)
    
    measurement_time = Instrument.setting("M%i",
                                          """Set the measurement time: 0.3s, 1s, 10s, 100s.""",
                                          validator=strict_discrete_set,
                                          values = {0.3: 1, 1: 2, 10: 3, 100: 4},
                                          map_values = True)
    
    every_result_query = Instrument.measurement("E?",
                                                """Every Result Query. Measurement results are sent continuously at the interval set for the
                                                measurement time (0.3s, 1s, 10s or 100s). Since these are 'measurement time' intervals,
                                                all results will be valid measurements. Stopped by <STOP> or any other command.""",
                                                get_process= lambda v: v.replace("Hz", '').replace("s", '').replace("%", ''),
                                                cast=float
                                                )
    
    continuous_result_query = Instrument.measurement("C?",
                                                """Continuous Result Query. Measurement results are sent continuously at the rate at which
                                                the LCD is updated for the selected measurement time - every 2s, 1s, 0.5s or 0.3s for
                                                measurement times of 100s, 10s, 1s or 0.3s respectively. Measurements are sent
                                                whether the <Measure> annunciator was flashing or not, i.e. the measurement may not
                                                be valid. Stopped by <STOP> or any other command.""",
                                                get_process= lambda v: v.replace("Hz", '').replace("s", '').replace("%", ''),
                                                cast=float
                                                )
    
    next_result_query = Instrument.measurement("N?",
                                                """Next Result Query. The measurement at the next LCD update provided the <Measure>
                                                annunciator is not flashing, i.e. the next valid measurement.""",
                                                get_process= lambda v: v.replace("Hz", '').replace("s", '').replace("%", ''),
                                                cast=float
                                                )
    
    current_result_query = Instrument.measurement("?",
                                                """Current Result Query. The measurement at the most recent LCD update whether the
                                                <Measure> annunciator was flashing or not, i.e. the measurement may not be valid.""",
                                                get_process= lambda v: v.replace("Hz", '').replace("s", '').replace("%", ''),
                                                cast=float
                                                )
    
    inputACoupling = Instrument.setting("%s",
                                        """Set input A coupling, AC or DC""",
                                        validator=strict_discrete_set,
                                        values = ["AC", "DC"])
    
    inputAImpedance = Instrument.setting("%s",
                                         """Set input A impedance, 1MOhm or 50Ohm""",
                                         validator=strict_discrete_set,
                                         values={"1MOhm": "Z1", "50Ohm": "Z5"},
                                         map_values=True)
    
    inputAAttenuation = Instrument.setting("%s",
                                           """Set input A attenuation, 1:1 or 5:1""",
                                           validator=strict_discrete_set,
                                           values={"5:1":"A5", "1:1":"A1"},
                                           map_values=True)
    
    edge_trigger = Instrument.setting("%s",
                                      """Set the edge trigger, either rising or falling""",
                                      validator=strict_discrete_set,
                                      values={"rising": "ER", "falling":"EF"},
                                      map_values=True)
    
    low_pass_filter_enable = Instrument.setting("%s",
                                                """Set the lowpass filter enable, either True or False""",
                                                validator=strict_discrete_set,
                                                values={True: "FI", False: "FO"},
                                                map_values=True)

    def __init__(self, adapter, *args, **kwargs):
        super().__init__(adapter, "TF930 3GHZ Counter", *args, **kwargs)

    def setAutotriggering(self):
        """Use with DC coupling. Threshold Level set to achieve auto triggering; the threshold
        automatically adjusts to the average level of the waveform being measured (no offset)."""
        self.write("TA")

    def stop(self):
        """Stops further measurements being sent in response to E? or C?; any other command will
        also stop further measurements being sent, as well as initiating the action of that
        command."""
        self.write("STOP")

if __name__ == "__main__":
    from pymeasure.adapters import VISAAdapter
    from pyvisa.constants import VI_ASRL_FLOW_XON_XOFF, VI_TRUE
    freqCount = TF930(VISAAdapter("ASRL5:INSTR", baud_rate = 115200, write_termination = "\n", read_termination = "\r\n", parity = False, flow_control = VI_ASRL_FLOW_XON_XOFF))
    freqCount.measurement_function = freqCount.TF930MasurementFunctions.AInputCount
    freqCount.adapter.close()

    import pyqtgraph as pg
    import numpy as np
    from PyQt6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    imv = pg.ImageView()
    imv.setImage(np.random.rand(200,200,200))
    #imv.timeLine
    imv.show()
    app.exec()
    