import numpy as np


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

            if 'init-wl-delta' in l and hasattr(self, 'init_wl') is False:
                self.init_wl = float(l.split('=')[1])

            if 'ref-t' in l and hasattr(self, 'temp') is None:
                self.temp = float(l.split(':')[1])

            if 'init-lambda-weights[' in l and hasattr(self, 'init_w'):
                self.init_w.append(float(l.split('=')[1]))

            if 'Started mdrun' in l:
                self.start = line_n  # the line number that the simulation starts
                break

        # Set the default of some attributes
        self.equil = False

    def extract_equil_info(self, logfile):
        """
        Extracts information about the execution of Wang-Landau algorithm, including the 
        Wang-Landau weights and the Wang-Landau incrementor. This function is specifically 
        for expanded ensemble simulations whose weights were being updated (equilibrated or
        not).
        """
        f = open(logfile, 'r')
        lines = f.readlines()
        f.close()

        # for saving wl_incrementor as a function of time
        wl_incrementor = [self.init_wl]
        update_step = []   # steps at which the weights are updated
        line_n = self.start

        for l in lines[self.start:]:
            line_n += 1

            # Step 1: Extract the Wang-Landau incrementor
            if 'weights are now: ' in l:
                # this line only appears before the WL incrementor is about to change
                weights_line = l.split(':')
                update_step.append(int(weights_line[0].split()[1]))

                # for searching WL incrementor
                search_lines = lines[line_n + 1: line_n + 15]
                # the info of the incrementor typically appears within the next 15 lines
                for l_search in search_lines:
                    if 'Wang-Landau incrementor is:' in l_search:
                        wl_incrementor.append(float(l_search.split(':')[1]))

            # Step 2: Extract the Wang-Landau weights if they are equilibrated
            if 'Weights have equilibrated' in l:
                self.equil = True
                # Step 1: search equilibrated weights
                # step at which the weights are equilibrated
                equil_step = l.split(':')[0].split()[1]
                # lines for searching weights
                search_lines = lines[line_n - 9:line_n]

                for l_search in search_lines:
                    if 'weights are now: ' in l_search:
                        self.equil_w = [float(i)
                                        for i in l_search.split(':')[2].split()]

                # Step 2: search equilibrated counts for each states
                self.equil_counts = []
                search_n = line_n - (30 + self.N_states)
                search_lines = lines[line_n - (30 + self.N_states): line_n]
                # 30 is the approximate number of lines of metadata between the counts data and the position
                # at which the weights are found equilibrated.

                for l_search in search_lines:
                    search_n += 1
                    if 'MC-lambda information' in l_search:
                        for i in range(self.N_states):
                            # start from lines[search_n + 2]
                            if lines[search_n + 2 + i].split()[-1] == '<<':
                                self.equil_counts.append(
                                    float(lines[search_n + 2 + i].split()[-4]))
                            else:
                                self.equil_counts.append(
                                    float(lines[search_n + 2 + i].split()[-3]))

                self.equil_time = float(equil_step) * \
                    self.dt / 1000   # units: ns

                break
            
        # some additional information if the weights are eqilibrated
        if self.equil is True:
            avg_counts = sum(equil_counts) / len(equil_counts)
            self.max_Nratio = max(equil_counts) / avg_counts
            self.min_Nratio = min(equil_counts) / avg_counts
            self.E_err = np.abs(np.log(equil_counts[0] / equil_counts[-1]))


        # Case 2-2: Non-equilibrated weights
        if self.fixed is False and self.equil is False:
            self.N_updated = len(wl_incrementor) - 1  
            self.N_update = int(np.ceil(np.log(self.cutoff / wl_incrementor[-1]) np.log(self.wl_scale)))  # number of updates required


        update_time = np.array(update_step) * self.dt / 1000   # units: ns
        wl_incrementor = np.array(wl_incrementor)

        return update_time, wl_incrementor

    def extract_final_counts(self, logfile):
        f = open(logfile, 'r')
        lines = f.readlines()
        f.close()
        lines.reverse()  

        final_found = False   # whether the final counts are found
        line_n = 0
        final_counts = np.zeros(self.N_states)
        self.final_w = np.zeros(self.N_states)
        for l in lines:
            line_n += 1
            if 'MC-lambda information' in l: # should find this line first (lines[line_n - 1])
                final_found = True
                if self.fixed is True:
                    data_line = line_n - 3
                else:
                    data_line = line_n - 4

                for i in range(self.N_states):
                    if lines[data_line - i].split()[-1] == '<<':
                        self.final_w.append(float(lines[data_line - i].split()[-3]))
                        final_counts[i] = float(lines[data_line - i].split()[-4])
                    else:
                        self.final_w.append(float(lines[data_line - i].split()[-2]))
                        final_counts[i] = float(lines[data_line - i].split()[-3])
            
            if '  Step  ' in l and final_found is True:  # lines[line_n - 1]
                self.final_time = float(lines[line_ne - 2].split()[1]) / 1000  # units: ns
                break

        return final_counts





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
