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
    parser.add_argument('-m',
                        '--mdp',
                        type=str,
                        help='The .mdp file as the basis of the newly generated .mdp\
                            file for the fixed-weight simulation. Note that a new .mdp\
                            file will be generated only if there were only one log\
                            file provided and the weights had been equilibrated.')
    parser.add_argument('-w',
                        '--weights',
                        type=str,
                        choices=['equilibrated', 'adjusted', 'average'],
                        default='adjusted',
                        help='Which kind of weights to be used in the new .mdp file.')
    
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

    # Case 1: equilibrated weights
    if EXE.fixed is False and EXE.equil is True:
        print(f'The weights were equilibrated at {EXE.equil_time} ns\n')
        print(f'The Wang-Landau ratio was set as {EXE.wl_ratio}, which means that all N_ratio should be larger than {EXE.wl_ratio} and smaller than { 1 / float(log_info.wl_ratio: .3f)}.\n')
        print(f'At the time that the weights were equilibrated, the largest and smallest N_ratio are {EXE.max_Nratio: .5f} and {EXE.min_Nratio: .5f}, respectively.\n')
        print(f'The equilibrated weights are: {weights_f} \n')
        print(f'The uncertainty of the free energy difference estimated from equilibrated counts is {EXE.E_err: .3f} kT.')
        #print('The adjusted weights based on the equilibrated histogram are (RMSD: %6.5f kT):\n %s\n' % (RMSD, wght_adjstd_str))




    

    

        


