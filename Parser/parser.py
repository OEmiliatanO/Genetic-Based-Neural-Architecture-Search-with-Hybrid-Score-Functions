import argparse

def RD_search_argsparser():
    parser = argparse.ArgumentParser(description='rk-based-nas')
    parser.add_argument('--data_loc', default='../cifardata/', type=str, help='dataset folder')
    parser.add_argument('--api_loc', default='./NAS-Bench-201.pth',
                        type=str, help='path to API')
    parser.add_argument('--save_loc', default='results/ICML', type=str, help='folder to save results')
    parser.add_argument('--save_string', default='RD', type=str, help='prefix of results file')
    parser.add_argument('--nasspace', default='nasbench201', type=str, help='the nas search space to use')
    parser.add_argument('--batch_size', default=128, type=int)
    parser.add_argument('--kernel', action='store_true')
    parser.add_argument('--dropout', action='store_true')
    parser.add_argument('--repeat', default=1, type=int, help='how often to repeat a single image with a batch')
    parser.add_argument('--augtype', default='none', type=str, help='which perturbations to use')
    parser.add_argument('--sigma', default=1, type=float, help='noise level if augtype is "gaussnoise"')
    parser.add_argument('--GPU', default='0', type=str)
    parser.add_argument('--seed', default=1, type=int)
    parser.add_argument('--init', default='', type=str)

    parser.add_argument('--valid', action='store_true')
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--train', action='store_true')
    
    parser.add_argument('--save', action='store_true')

    parser.add_argument('--activations', action='store_true')
    parser.add_argument('--cosine', action='store_true')
    parser.add_argument('--dataset', default='cifar10', type=str)
    parser.add_argument('--n_samples', default=100, type=int)
    parser.add_argument('--n_runs', default=500, type=int)
    parser.add_argument('--stem_out_channels', default=16, type=int, help='output channels of stem convolution (nasbench101)')
    parser.add_argument('--num_stacks', default=3, type=int, help='#stacks of modules (nasbench101)')
    parser.add_argument('--num_modules_per_stack', default=3, type=int, help='#modules per stack (nasbench101)')
    parser.add_argument('--num_labels', default=1, type=int, help='#classes (nasbench101)')
    return parser.parse_args()

def GA_search_argsparser():
    parser = argparse.ArgumentParser(description='rk-based-nas')

    parser.add_argument('--maxn_pop', default=25, type=int, help='number of population')
    parser.add_argument('--maxn_iter', default=30, type=int, help='number of iteration')
    parser.add_argument('--prob_mut', default=0.07, type=float, help='probability of mutation')
    parser.add_argument('--prob_cr', default=0.8, type = float, help='probability of crossover')

    parser.add_argument('--data_loc', default='./cifardata/', type=str, help='dataset folder')
    parser.add_argument('--api_loc', default='./NAS-Bench-201.pth',
                        type=str, help='path to API')
    parser.add_argument('--save_loc', default='results/ICML', type=str, help='folder to save results')
    parser.add_argument('--save_string', default='GA', type=str, help='prefix of results file')
    parser.add_argument('--nasspace', default='nasbench201', type=str, help='the nas search space to use')
    parser.add_argument('--batch_size', default=128, type=int)
    parser.add_argument('--kernel', action='store_true')
    parser.add_argument('--dropout', action='store_true')
    parser.add_argument('--repeat', default=1, type=int, help='how often to repeat a single image with a batch')
    parser.add_argument('--augtype', default='none', type=str, help='which perturbations to use')
    parser.add_argument('--sigma', default=1, type=float, help='noise level if augtype is "gaussnoise"')
    parser.add_argument('--GPU', default='0', type=str)
    parser.add_argument('--seed', default=1, type=int)
    parser.add_argument('--init', default='', type=str)

    parser.add_argument('--valid', action='store_true')
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--train', action='store_true')

    parser.add_argument('--activations', action='store_true')
    parser.add_argument('--cosine', action='store_true')
    parser.add_argument('--dataset', default='cifar10', type=str)
    parser.add_argument('--n_samples', default=50, type=int)
    parser.add_argument('--n_runs', default=500, type=int)
    parser.add_argument('--stem_out_channels', default=16, type=int, help='output channels of stem convolution (nasbench101)')
    parser.add_argument('--num_stacks', default=3, type=int, help='#stacks of modules (nasbench101)')
    parser.add_argument('--num_modules_per_stack', default=3, type=int, help='#modules per stack (nasbench101)')
    parser.add_argument('--num_labels', default=1, type=int, help='#classes (nasbench101)')

    parser.add_argument('--verbose', action='store_true')
    return parser.parse_args()

def SA_search_argsparser():
    parser = argparse.ArgumentParser(description='rk-based-nas')
    parser.add_argument('--data_loc', default='./cifardata/', type=str, help='dataset folder')
    parser.add_argument('--api_loc', default='./NAS-Bench-201.pth',
                        type=str, help='path to API')
    parser.add_argument('--save_loc', default='results/ICML', type=str, help='folder to save results')
    parser.add_argument('--save_string', default='SA', type=str, help='prefix of results file')
    parser.add_argument('--nasspace', default='nasbench201', type=str, help='the nas search space to use')
    parser.add_argument('--batch_size', default=128, type=int)
    parser.add_argument('--kernel', action='store_true')
    parser.add_argument('--dropout', action='store_true')
    parser.add_argument('--repeat', default=1, type=int, help='how often to repeat a single image with a batch')
    parser.add_argument('--augtype', default='none', type=str, help='which perturbations to use')
    parser.add_argument('--sigma', default=1, type=float, help='noise level if augtype is "gaussnoise"')
    parser.add_argument('--GPU', default='0', type=str)
    parser.add_argument('--seed', default=1, type=int)
    parser.add_argument('--init', default='', type=str)

    parser.add_argument('--valid', action='store_true')
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--train', action='store_true')

    parser.add_argument('--trainval', action='store_true')
    parser.add_argument('--activations', action='store_true')
    parser.add_argument('--cosine', action='store_true')
    parser.add_argument('--dataset', default='cifar10', type=str)
    parser.add_argument('--n_samples', default=100, type=int)
    parser.add_argument('--n_runs', default=500, type=int)
    parser.add_argument('--stem_out_channels', default=16, type=int, help='output channels of stem convolution (nasbench101)')
    parser.add_argument('--num_stacks', default=3, type=int, help='#stacks of modules (nasbench101)')
    parser.add_argument('--num_modules_per_stack', default=3, type=int, help='#modules per stack (nasbench101)')
    parser.add_argument('--num_labels', default=1, type=int, help='#classes (nasbench101)')

    parser.add_argument('--end_T', default=1, type=float)
    parser.add_argument('--maxn_iter', default=1, type=int)
    parser.add_argument('--Rt', default=1, type=float)
    parser.add_argument('--init_T', default=1, type=int)
    parser.add_argument('--maxN', default=10, type=int)
    parser.add_argument('--alpha', default=0.25, type=float)
    parser.add_argument('--beta', default=1, type=float)

    return parser.parse_args()

def score_argsparser():
    parser = argparse.ArgumentParser(description='Genetic-Based NAS with Hybrid Score Functions')
    parser.add_argument('--data_loc', default='../cifardata/', type=str, help='dataset folder')
    parser.add_argument('--api_loc', default='./NAS-Bench-201.pth',
                        type=str, help='path to API')
    parser.add_argument('--save_loc', default='results', type=str, help='folder to save results')
    parser.add_argument('--save_string', default='score_networks', type=str, help='prefix of results file')
    parser.add_argument('--nasspace', default='nasbench201', type=str, help='the nas search space to use')
    parser.add_argument('--batch_size', default=128, type=int)
    parser.add_argument('--repeat', default=1, type=int, help='how often to repeat a single image with a batch')
    parser.add_argument('--augtype', default='none', type=str, help='which perturbations to use')
    parser.add_argument('--sigma', default=0.05, type=float, help='noise level if augtype is "gaussnoise"')
    parser.add_argument('--GPU', default='0', type=str)
    parser.add_argument('--seed', default=1, type=int)
    parser.add_argument('--init', default='', type=str)

    parser.add_argument('--valid', action='store_true')
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--train', action='store_true')

    parser.add_argument('--dropout', action='store_true')
    parser.add_argument('--dataset', default='cifar10', type=str)
    parser.add_argument('--maxofn', default=1, type=int, help='score is the max of this many evaluations of the network')
    parser.add_argument('--n_samples', default=50, type=int)
    parser.add_argument('--n_runs', default=500, type=int)
    parser.add_argument('--stem_out_channels', default=16, type=int, help='output channels of stem convolution (nasbench101)')
    parser.add_argument('--num_stacks', default=3, type=int, help='#stacks of modules (nasbench101)')
    parser.add_argument('--num_modules_per_stack', default=3, type=int, help='#modules per stack (nasbench101)')
    parser.add_argument('--num_labels', default=1, type=int, help='#classes (nasbench101)')
    return parser.parse_args()
