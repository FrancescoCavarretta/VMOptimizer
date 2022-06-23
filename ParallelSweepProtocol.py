import bluepyopt.ephys as ephys
import os
import numpy as np
import tempfile
import sys

class SweepProtocol(ephys.protocols.Protocol):
    def __init__(self, name=None, stimuli=None, recordings=None, cvode_active=None, deterministic=False):
        """Constructor

        Args:
            name (str): name of this object
            stimuli (list of Stimuli): Stimulus objects used in the protocol
            recordings (list of Recordings): Recording objects used in the
                protocol
            cvode_active (bool): whether to use variable time step
            deterministic (bool): whether to force all mechanism
                to be deterministic
        """

        super(SweepProtocol, self).__init__(name)

        # command line string format for running the evaluation        
        self._command_line_fmt = './x86_64/special protocol_process.py %s --etype %s --param_file %s --response_file %s >/dev/null'
        self._core_neuron_switch = '--coreneuron' if '--coreneuron' in sys.argv else ''
        self.stimuli = stimuli
        self.recordings = recordings
        self.cvode_active = cvode_active
        self.deterministic = deterministic


    def run(self, cell_model, param_values, sim=None, isolate=None, timeout=None):
      param_file = tempfile.NamedTemporaryFile(prefix="bpo_in_", suffix=".npy").name # parameter file
      response_file = tempfile.NamedTemporaryFile(prefix="bpo_out_", suffix=".npy").name # response file

      # store the parameters in a file
      np.save(param_file, param_values, allow_pickle=True)
      
      # simulation execution, generation of responses
      command_line = self._command_line_fmt % (self._core_neuron_switch, cell_model.name, param_file, response_file) # make the command line

      try:
        os.system(command_line) # execute
        recordings = np.load(response_file, allow_pickle=True).tolist() # load the responses
        responses = {recording.name:recording.response for recording in recordings} # get the responses
      except:
        responses = {recording.name:None for recording in self.recordings}

      try:        
          os.remove(param_file) # remove the param file
      except:
          pass
        
      try:
          os.remove(response_file) # remove the response file
      except:
          pass

      return responses

      
    def adjust_stochasticity(func):
      pass


    def instantiate(self, sim=None, icell=None):
      pass
    

    def destroy(self, sim=None):
      pass


    def __str__(self):
        """String representation"""

        content = '%s:\n' % self.name

        content += '  stimuli:\n'
        for stimulus in self.stimuli:
            content += '    %s\n' % str(stimulus)

        content += '  recordings:\n'
        for recording in self.recordings:
            content += '    %s\n' % str(recording)

        return content


class StepProtocol(SweepProtocol):

    """Protocol consisting of step and holding current"""

    def __init__(
            self,
            name=None,
            step_stimulus=None,
            holding_stimulus=None,
            recordings=None,
            cvode_active=None,
            deterministic=False):
        """Constructor

        Args:
            name (str): name of this object
            step_stimulus (list of Stimuli): Stimulus objects used in protocol
            recordings (list of Recordings): Recording objects used in the
                protocol
            cvode_active (bool): whether to use variable time step
            deterministic (bool): whether to force all mechanism
                to be deterministic
        """

        super(StepProtocol, self).__init__(
            name,
            stimuli=[
                step_stimulus,
                holding_stimulus]
            if holding_stimulus is not None else [step_stimulus],
            recordings=recordings,
            cvode_active=cvode_active)

        self.step_stimulus = step_stimulus
        self.holding_stimulus = holding_stimulus

    @property
    def step_delay(self):
        """Time stimulus starts"""
        return self.step_stimulus.step_delay

    @property
    def step_duration(self):
        """Time stimulus starts"""
        return self.step_stimulus.step_duration
