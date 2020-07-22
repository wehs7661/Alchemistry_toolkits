import sys
import time as timer

sys.path.insert(1, '../')
from parsers.log_parser import EXE_LogInfo

# Some settings for plotting
rc('font', **{
        'family': 'sans-serif',
        'sans-serif': ['DejaVu Sans'],
        'size': 10
})
# Set the font used for MathJax - more on this later
rc('mathtext', **{'default': 'regular'})
plt.rc('font', family='serif')

def initialize():
    """
    An argument parser as an initializing function
    """

    parser = argparse.ArgumentParser(
        description='This code analyzes the log file generated from expanded \
                    ensemble simulations.')
    parser.add_argument('-l',
                        '--log',
                        type=str,
                        help='The filename of the log file.')
    parser.add_argument('-p',
                        '--prefix',
                        type=str,
                        help='The common prefix of the files.')
    parser.add_argument('-t',
                        '--temp',
                        type=float,
                        default=298.15,
                        help='The simulation temperature.')
    parser.add_argument('-a',
                        '--avg_len',
                        type=float,
                        default=20,
                        help='The length of the simulation that the calculation \
                            of average weights are based on. -a 20 means that the \
                            weights of last 20 ns before the weights are eauilibrated\
                            will be averaged. Default: 20 ns. If multiple files are\
                            given, the same value applies to all.')
    parser.add_argument('-w',
                        '--weights',
                        type=str,
                        choices=['equilibrated', 'adjusted', 'average'],
                        default='adjusted',
                        help='Generate the weights to be fixed in the next expanded ensemble simulation.')
    
    args = parser.parse_args()

    if args.log is None:
        for file in os.listdir('.'):
            if file.endswith('.log'):
                args.log.append(file)
        try:
            open(args.log)
        except FileNotFoundError:
            print('No log files found! Please check if the directory is correct or specify the name of the log file.')

    if args.prefix is None:
        args.prefix = args.log.split('.')[0]

    return args

def main():
    time_needed = []
    s0 = timer.time()
    args = initialize()

    print(f'\nThe log file to be analyzed: {args.log}.')
    result_str = f'Data analysis of the file {args.log}:'
    print(result_str)
    print('=' * len(result_str))

    # Analysis starts!
    EXE = EXE_LogInfo(args.log)
    updated_time, wl_incrementor = EXE.extract_equil_info(args.log)
    final_counts = EXE.extract_final_counts(args.log)

    # Case 1: equilibrated weights
    if EXE.fixed is False and EXE.equil is True:
        print(f'The weights were equilibrated at {EXE.equil_time} ns\n')
        print(f'The Wang-Landau ratio was set as {EXE.wl_ratio}, which means that all N_ratio should be larger than {EXE.wl_ratio} and smaller than { 1 / float(log_info.wl_ratio: .3f)}.\n')
        print(f'At the time that the weights were equilibrated, the largest and smallest N_ratio are {EXE.max_Nratio: .5f} and {EXE.min_Nratio: .5f}, respectively.\n')
        print(f'The equilibrated weights are: {weights_f} \n')
        print(f'The uncertainty of the free energy difference estimated from equilibrated counts is {EXE.E_err: .3f} kT.')
        #print('The adjusted weights based on the equilibrated histogram are (RMSD: %6.5f kT):\n %s\n' % (RMSD, wght_adjstd_str))
    
    # Case 2: Non-equilibrated weights
    if EXE.fixed is False and self.equil is False:
        N_updated = len(wl_incrementor) -1 
        N_update = int(np.ceil(np.log(self.cutoff / wl_incrementor[-1]) /
                               np.log(self.wl_scale)))  # number of updates required
        diff_w = np.array(self.final_w) - np.array(self.init_w)
        diff_w = [round(x, 2) for x in diff_w]
        print('The weights have not equilibrated.')
        print(f'Initial weights: {' '.join([str(i) for i in self.init_w])}')
        print(f'Final weights: {' '.join([str(i) for i in self.final_w])}')
        print(f'Difference between the initial weights and the final weights: {' '.join(str(i) for i in diff_w)}')
        print(f'\nThe Wan-Landau incrementor has been updated for {N_updated} times.')
        print(f'The last time frame that the Wang-Landau incrementor was updated ({updated_time[-1]: .3f} ns) is {wl_incrementor[-1]}.')
        print(f'The Wang-Landau scale and the cutoff of Wang-Landau incrementor are {self.wl_scale} and {self.cutoff}, respectively.')
        print(f'Therefore, it requires {N_update} more updates in Wang-Landau incrementor for the weights to be equilibrated.')
        print('Check the log file for more information.')

    # Case 3: Fixed weights
    if EXE.fixed is True:
        




    

    

        


