
class EXE_LogInfo:
    def __init__(self, logfile):
        """
        Obtain the simulation parameters of expanded ensemble from the log file.

        Parameters
        ----------
        logfile : str
            The filename of the log file
        """
        f = open(logfile, 'r')
        lines = f.readlines()
        f.close()

        line_n = 0

        for l in lines:
            line_n += 1
            if 'dt  ' in l and hasattr(self, 'dt') is False:
                self.dt = float(l.split('=')[1])

            if 'nstlog' in l and hasattr(self, 'nstlog') is False:
                self.nstlog = float(l.split('=')[1])

            if 'weight-equil-wl-delta' in l and hasattr(self, 'cutoff') is False:
                self.cutoff = float(l.split('=')[1])

            if 'wl-ratio' in l and hasattr(self, 'wl_ratio') is False:
                self.wl_ratio = float(l.split('=')[1])

            if 'wl-scale' in l and hasattr(self, 'wl_sclae') is False:
                self.wl_scale = float(l.split('=')[1])

            if 'n-lambdas' in l and hasattr(self, 'N_states') is False:
                self.N_states = int(l.split('=')[1])

            if 'lmc-stats' in l and hasattr(self, 'fixed') is False:
                if l.split('=')[1].split()[0] == 'no':
                    self.fixed = True
                else:
                    self.fixed = False

            if 'ref-t' in l and hasattr(self, 'temp') is None:
                self.temp = float(l.split(':')[1])

            if 'init-lambda-weights[' in l and hasattr(self, 'init_w'):
                self.init_w.append(float(l.split('=')[1]))

            if 'Started mdrun' in l:
                self.start = line_n  # the line number that the simulation starts
                break


class REMD_LogInfo:
    def __init__(self, logfile):
        """
        Obtain the simulation parameters of Hamiltonian replica exchange from the log file.

        Parameters
        ----------
        logfile : str
            The filename of the log file

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
        f = open(logfile, 'r')
        lines = f.readlines()
        f.close()

        line_n = 0

        for l in lines:
            line_n += 1

            if 'dt  ' in l and hasattr(self, 'dt') is False:
                self.dt = float(l.split('=')[1])

            if 'Command line' in l:
                if 'nex' in lines[line_n]:  # number of exchanges
                    self.nex = True
                else:
                    self.nex = False

                if 'replex' in lines[line_n]:  # neighboring exchanges
                    self.replex = float(
                        lines[line_n].split('replex')[1].split()[0])

            if 'Replica exchange in ' in l:
                self.N_states = len(lines[line_n].split())

            if 'Started mdrun' in l:
                self.start = line_n
                # the line number that the simulation got started
                break
