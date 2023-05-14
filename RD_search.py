import argparse
import nasspace
import datasets
import random
import numpy as np
import torch
from torch import nn
import importlib
import os
import sys
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import trange
from statistics import mean
from numpy import std
import time
from utils import add_dropout, remap_dataset_names
from score import *
from encoder import encoder
from scipy.stats import kendalltau
from Parser import parser

args = parser.RD_search_argsparser()
os.environ['CUDA_VISIBLE_DEVICES'] = args.GPU
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

print("RD search algo")
print(f"Use GPU {args.GPU}...")
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(f"The current device used is {device}")

# Reproducibility
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
random.seed(args.seed)
np.random.seed(args.seed)
torch.manual_seed(args.seed)

print(f"Initialize the train loader...")
print(f"dataset = {args.dataset}, data location = {args.data_loc}, validation = {args.valid}")
train_loader = datasets.get_data(args.dataset, args.data_loc, args.valid, args.batch_size, args.augtype, args.repeat, args)

print(f"Initialize the nas bench api ({args.nasspace}) ...")
if args.nasspace == "nasbench201":
    args.dataset, acc_type = remap_dataset_names(args.dataset, args.valid, args.test, args.train)
else:
    acc_type = None
print(f"dataset = {args.dataset}, validation = {args.valid}")
searchspace = nasspace.get_search_space(args)

print(f"Making sure {args.save_loc} exist.")
os.makedirs(args.save_loc, exist_ok=True)

times = []
accs = {"ni": [], "naswot": [], "logsynflow": [], "rank-based": []}

Encoder = encoder.get_encoder(args.nasspace)

algo_module = importlib.import_module(f"search.{args.nasspace}_RD_rk")
RD = getattr(algo_module, "RD")
RD_kwargs = {"searchspace": searchspace, "train_loader": train_loader, "device": device, "args": args, "acc_type": None, "Encoder": Encoder}
if args.nasspace == "nasbench201":
    RD_kwargs["acc_type"] = acc_type

taus = {"rk":[], "ni": [], "naswot": [], "logsynflow": []}
cnt = 0
runs = trange(args.n_runs, desc='acc: ')
for N in runs:
    start = time.time()

    #w = weight_giver(archstrs)
    sol = RD(**RD_kwargs)
    niuid, naswotuid, logsynuid, bestrk_uid, rk_tau, ni_tau, naswot_tau, logsyn_tau, maxacc, rk_maxacc= sol.search()

    taus['rk'].append(rk_tau)
    taus['ni'].append(ni_tau)
    taus['naswot'].append(naswot_tau)
    taus['logsynflow'].append(logsyn_tau)

    accs["ni"].append(searchspace.get_final_accuracy(int(niuid), acc_type, args.valid))
    accs["naswot"].append(searchspace.get_final_accuracy(int(naswotuid), acc_type, args.valid))
    accs["logsynflow"].append(searchspace.get_final_accuracy(int(logsynuid), acc_type, args.valid))
    accs["rank-based"].append(searchspace.get_final_accuracy(int(bestrk_uid), acc_type, args.valid))

    times.append(time.time()-start)
    runs.set_description(f"acc_ni: {mean(accs['ni']):.2f}({std(accs['ni']):.3f}),{mean(taus['ni']):.3f}, acc_naswot: {mean(accs['naswot']):.2f}({std(accs['naswot']):.3f}),{mean(taus['naswot']):.3f}, acc_logsyn: {mean(accs['logsynflow']):.2f}({std(accs['logsynflow']):.3f}),{mean(taus['logsynflow']):.3f}, rk-based: {mean(accs['rank-based']):.2f}({std(accs['rank-based']):.3f}),{mean(taus['rk']):.3f}")

state = {'ni-accs': accs["ni"],
         'naswot': accs["naswot"],
         'logsynflow': accs["logsynflow"],
         'rank-based': accs["rank-based"],
         'chosen': chosen,
         'times': times,
         'topscores': topscores,
         }

fname = f"{args.save_loc}/{args.save_string}_{args.score}_{args.nasspace}_{args.dataset}_{args.kernel}_{args.dropout}_{args.augtype}_{args.sigma}_{args.repeat}_{args.batch_size}_{args.n_runs}_{args.n_samples}_{args.seed}.t7"
torch.save(state, fname)
