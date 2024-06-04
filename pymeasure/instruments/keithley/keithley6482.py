from pymeasure.instruments import Instrument, SCPIMixin, Channel
from pymeasure.instruments.validators import strict_range, strict_discrete_set, strict_discrete_range
from pymeasure.adapters import VISAAdapter
import numpy as np
import time

class Keithley6482Chnanel(Channel):

    sourcing_mode = Instrument.control("SOUR{ch}:VOLT:MODE?",
                                       "SOUR{ch}:VOLT:MODE %s",
                                       """Configure the sourcing mode. Choose between fixed FIX, list LIST or sweep SWE""",
                                       validator=strict_discrete_set,
                                       preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                       values=["FIX", "LIST", "SWE"],
                                       cast=str)
    
    settling_time = Instrument.control("SOUR{ch}:DEL?",
                                   "SOUR{ch}:DEL %g",
                                   """Control the the settling time (s) of the source. This is the delay between the source turning on and the actual voltage being applied at the output""",
                                   validator=strict_range,
                                   preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                   values=(0, 9999.999),
                                   cast=float)
    
    current = Instrument.measurement("FORM:ELEM CURR{ch}; :READ?",
                                     """Measure the current. The size of the output will be equal to the product arm_count*trigger_count""",
                                     preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                     cast=float)
    
    current_autorange = Instrument.control("SENS{ch}:CURR:RANG:AUTO?",
                                        "SENS{ch}:CURR:RANG:AUTO %i",
                                        """Turn current autorange on or off.""",
                                        validator=strict_discrete_set,
                                        preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                        values=(True, False),
                                        cast=bool)
    
    ground_connect = Instrument.control("SOUR{ch}:GCON?",
                                        "SOUR{ch}:GCON %i",
                                        """Turn ground connect on or off.""",
                                        validator=strict_discrete_set,
                                        preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                        values=(True, False),
                                        cast=bool)
    
    output = Instrument.control("OUTP{ch}?",
                                "OUTP{ch} %i",
                                """Turn output on or off.""",
                                validator=strict_discrete_set,
                                values=(True, False),
                                preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                cast=bool)
    
    auto_delay = Instrument.control("SOUR{ch}:DEL:AUTO?",
                                    "SOUR{ch}:DEL:AUTO %i",
                                    """Turn auto-delay on or off.""",
                                    validator=strict_discrete_set,
                                    values=(True, False),
                                    preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                    cast=bool)
    
    #fixed config
    voltage = Instrument.control("SOUR{ch}:VOLT?",
                                   "SOUR{ch}:VOLT %g",
                                   """Control the amplitude (V) of the voltage source.""",
                                   validator=strict_range,
                                   preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                   values=(-30, 30),
                                   cast=float)
    
    #sweep config
    start = Instrument.control("SOUR{ch}:VOLT:STAR?",
                                   "SOUR{ch}:VOLT:STAR %g",
                                   """Control the sweep start voltage (V).""",
                                   validator=strict_range,
                                   preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                   values=(-30, 30),
                                   cast=float)
    
    stop = Instrument.control("SOUR{ch}:VOLT:STOP?",
                                   "SOUR{ch}:VOLT:STOP %g",
                                   """Control the sweep stop voltage (V).""",
                                   validator=strict_range,
                                   preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                   values=(-30, 30),
                                   cast=float)
    
    step = Instrument.control("SOUR{ch}:VOLT:STEP?",
                                   "SOUR{ch}:VOLT:STEP %g",
                                   """Control the sweep step size.""",
                                   validator=strict_range,
                                   preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                   values=(-30, 30),
                                   cast=float)
    
    points = Instrument.control("SOUR{ch}:SWE:POIN?",
                                   "SOUR{ch}:SWE:POIN %i",
                                   """Control the sweep number of points.""",
                                   validator=strict_discrete_set,
                                   preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                   values=range(1,3000),
                                   cast=int)
    
    center = Instrument.control("SOUR{ch}:VOLT:CENT?",
                                   "SOUR{ch}:VOLT:CENT %g",
                                   """Control the sweep center voltage (V).""",
                                   validator=strict_range,
                                   preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                   values=(-30, 30),
                                   cast=float)
    
    span = Instrument.control("SOUR{ch}:VOLT:SPAN?",
                                   "SOUR{ch}:VOLT:SPAN %g",
                                   """Control the sweep span (V).""",
                                   validator=strict_range,
                                   preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                   values=(-30, 30),
                                   cast=float)
    
    spacing = Instrument.control("SOUR{ch}:SWE:SPAC?",
                                 "SOUR{ch}:SWE:SPAC %s",
                                 """Control the spacing of the sweep. Choose between linear LIN or logarithmic LOG.""",
                                 validator=strict_discrete_set,
                                 preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                 values=["LIN", "LOG"],
                                 cast=str)
    
    ranging = Instrument.control("SOUR{ch}:SWE:RANG?",
                                 "SOUR{ch}:SWE:RANG %s",
                                 """Control the ranging of the sweep. Choose between best fixed BEST, auto AUTO, or fixed FIX.""",
                                 validator=strict_discrete_set,
                                 preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                 values=["BEST", "AUTO", "FIX"],
                                 cast=str)

    direction = Instrument.control("SOUR{ch}:SWE:DIR?",
                                 "SOUR{ch}:SWE:DIR %s",
                                 """Control the direction of the sweep. Choose between start to stop UP or stop to start DOWN.""",
                                 validator=strict_discrete_set,
                                 preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                 values=["UP", "DOWN"],
                                 cast=str)
    
    #median filter commands
    #TODO: implement the rest of the functions

    median_filter_enable = Instrument.control("SENS{ch}:MED:STAT?",
                                               "SENS{ch}:MED:STAT %i",
                                               """Turn the median filter on or off""",
                                               validator=strict_discrete_set,
                                               preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                               values=(True, False),
                                               cast=bool)
    
    #accuracy setting
    speed_accuracy = Instrument.control("SENS{ch}:CURR:NPLC?",
                                   "SENS{ch}:CURR:NPLC %g",
                                   """Control the speed/accuracy of the device. 0.01 lowest accuracy/highest speed, 10 highest accuracy/lowest speed""",
                                   validator=strict_range,
                                   preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                   values=(0.01, 10),
                                   cast=float)

    #TODO: list config

    #average filter
    average_filter_enable = Instrument.control("SENS{ch}:AVER:STAT?",
                                               "SENS{ch}:AVER:STAT %i",
                                               """Turn the average filter on or off""",
                                               validator=strict_discrete_set,
                                               preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                               values=(True, False),
                                               cast=bool)
    
    average_filter_count = Instrument.control("SENS{ch}:AVER:COUN?",
                                              "SENS{ch}:AVER:COUN %i",
                                              """Control the measurement counts for averaging.""",
                                              validator=strict_discrete_set,
                                              preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                              values=range(1,101))
    
    average_filter_type = Instrument.control("SENS{ch}:AVER:TCON?",
                                             "SENS{ch}:AVER:TCON %s",
                                             """Control the average filter type. Choose between moving MOV or repeating REP. Use REP for sweeps.""",
                                             validator=strict_discrete_set,
                                             preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                             values=["MOV", "REP"],
                                             cast=str)
    
    advanced_filter_enable = Instrument.control("SENS{ch}:AVER:ADV?",
                                                "SENS{ch}:AVER:ADV %i",
                                                """Turn the advanced averaging filter (it includes noise) on or off.""",
                                                validator=strict_discrete_set,
                                                preprocess_reply= lambda v: v.replace('\x13', '').replace('\x11', ''),
                                                values=(True, False),
                                                cast=bool)

    def slow_voltage(self, voltage:float, delay: float = 2e-3, steps: int = 50):
        if not self.sourcing_mode == "FIX":
            raise ValueError("The sourcing mode has to be FIX for slow_voltage!")
        if self.voltage == voltage:
            return
        voltages = np.linspace(self.voltage, voltage, steps)
        for v in voltages:
            self.voltage = v


class Keithley6482(SCPIMixin, Instrument):
    #adapter: VISAAdapter("ASRL4::INSTR")

    channel1 = Instrument.ChannelCreator(Keithley6482Chnanel, "1")
    channel2 = Instrument.ChannelCreator(Keithley6482Chnanel, "2")

    #set trigger
    trigger_count = Instrument.control("TRIG:COUN?",
                                       "TRIG:COUN %i",
                                       """Set trigger count. The product of trigger and arm counts should not excede 3000.""",
                                       validator=strict_discrete_set,
                                       values=range(1,3000))
    
    arm_count = Instrument.control("ARM:COUN?",
                                   "ARM:COUN %i",
                                   """Set arm count. The product of trigger and arm counts should not excede 3000.""",
                                   validator=strict_discrete_set,
                                   values=range(1,3000))

    def __init__(self, adapter: VISAAdapter, *args, **kwargs):
        super().__init__(adapter, 
                         name = "Keithley 6482", 
                         *args, 
                         **kwargs)

    def close(self):
        self.adapter.close()

# Example usage:
if __name__ == "__main__":
    
    sourcemeter = Keithley6482(adapter=VISAAdapter("ASRL3::INSTR", timeout = 10000))
    sourcemeter.reset()
    sourcemeter.channel1.sourcing_mode = "FIX"
    sourcemeter.channel1.current_autorange = True
    sourcemeter.channel1.slow_voltage(0.5)
    #sourcemeter.channel1.auto_delay = True
    #sourcemeter.channel1.spacing = "LIN"
    #sourcemeter.channel1.points = 100
    #sourcemeter.channel1.start = 0.1
    #sourcemeter.channel1.stop = 0.15
    #sourcemeter.channel1.ranging = "AUTO"
    sourcemeter.arm_count = 1
    sourcemeter.trigger_count = 100
    #sourcemeter.channel1.output = True
    print(sourcemeter.channel1.voltage)

    # Configure staircase sweep parameters
    start_voltage = 0.00  # V
    stop_voltage = 0.10  # V
    n_points = 10  #  you actually will get n_points+1 in the end; n_points<=2999
    ave = 10  # Number of sweep points
    delay = 0.001  # Source delay in seconds

    sourcemeter.close()