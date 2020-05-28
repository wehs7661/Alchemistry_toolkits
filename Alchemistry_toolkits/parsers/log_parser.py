import os

class REMD_LogInfo:
    def __init__(self, logfiles):
        """
        Gets the needed parameters and data from the log file and set up
        relevant attributes to run the analysis

        Parameters
        ----------
        logfiles : list
            A list of the filenames of log files
        
        Attributes
        ----------
        nex :

        replex : 

        N_states : int
            The number of alchemicla intermediate states
        dt : float
            The time step used in the simulation
        """
        # the info from all the log files in the same list should be the same
        f = open(logfiles[0], 'r')
        lines = f.readlines()
        f.close()

        self.nex = None
        self.replex = None
        self.N_states = None
        self.dt = None

        line_n = 0
        for l in lines:
            line_n += 1

            if 'dt  ' in l and self.dt is None:
                self.dt = float(l.split('=')[1])

            if 'Command line' in l:
                if 'nex' in lines[line_n]:
                    self.nex = True  
                else:
                    self.nex = False            

                if 'replex' in lines[line_n]:
                    self.replex = float(lines[line_n].split('replex')[1].split()[0])

            if 'Replica exchange in ' in l:
                self.N_states = len(lines[line_n].split())

            if 'Started mdrun' in l:
                self.start = line_n
                # the line number that the simulation got started
                break


        

