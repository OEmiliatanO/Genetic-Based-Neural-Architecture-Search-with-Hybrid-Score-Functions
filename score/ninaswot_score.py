import numpy as np
import torch
import random

def hooklogdet(K, labels=None):
    s, ld = np.linalg.slogdet(K)
    return ld

def get_batch_jacobian(net, x, target, device, args=None):
    net.zero_grad()
    x.requires_grad_(True)
    y, out = net(x)
    y.backward(torch.ones_like(y))
    jacob = x.grad.detach()
    return jacob, target.detach(), y.detach(), out.detach()

def naswot_score(network, train_loader, device, args):
    network.K = np.zeros((args.batch_size, args.batch_size))
    def counting_forward_hook(module, inp, out):
        try:
            if not module.visited_backwards:
                return
            if isinstance(inp, tuple):
                inp = inp[0]
            inp = inp.view(inp.size(0), -1)
            x = (inp > 0).float()
            K = x @ x.t()
            K2 = (1.-x) @ (1.-x.t())
            network.K = network.K + K.cpu().numpy() + K2.cpu().numpy()
        except:
            pass
            
    def counting_backward_hook(module, inp, out):    
        module.visited_backwards = True    

    forward_handler  = []
    backward_handler = []
    for name, module in network.named_modules():
        if 'ReLU' in str(type(module)):
            if hasattr(module, 'register_full_forward_hook'):
                forward_handler.append(module.register_full_forward_hook(counting_forward_hook))
                backward_handler.append(module.register_full_backward_hook(counting_backward_hook))
            else:
                forward_handler.append(module.register_forward_hook(counting_forward_hook))
                backward_handler.append(module.register_backward_hook(counting_backward_hook))

    network = network.to(device)    
    s = []

    data_iterator = iter(train_loader)
    x, target = next(data_iterator)
    x2 = torch.clone(x)
    x2 = x2.to(device)
    x, target = x.to(device), target.to(device)
    jacobs, labels, y, out = get_batch_jacobian(network, x, target, device, args)

    network(x2.to(device))
    s.append(hooklogdet(network.K, target))
    
    for i in range(len(forward_handler)):
        forward_handler[i].remove()
        backward_handler[i].remove()

    del network
    torch.cuda.empty_cache()
    return np.mean(s)

@torch.no_grad()
def ni_score(network, train_loader, device, args):
    network = network.to(device)
    data_iter = iter(train_loader)
    x, target = next(data_iter)
    x, target = x.to(device), target.to(device)

    noise = x.new(x.size()).normal_(0, args.sigma).to(device)
    x2 = x + noise

    o, _ = network(x)
    o_, _ = network(x2)
    o = o.detach().cpu().numpy()
    o_ = o_.detach().cpu().numpy()
    del network
    torch.cuda.empty_cache()
    return -np.sum(np.square(o-o_))

def ninaswot_score(network, train_loader, device, stds, means, args):
    scoreNASWOT = naswot_score(network, train_loader, device, args)
    scoreNI     = ni_score(network, train_loader, device, args)
    std_of_nas  = stds["naswot"]
    mean_of_nas = means["naswot"]
    stand_score_naswot = (scoreNASWOT - mean_of_nas) / std_of_nas
    std_of_ni  = stds["ni"]
    mean_of_ni = means["ni"]
    stand_score_ni  = (scoreNI - mean_of_ni) / std_of_ni
    return stand_score_naswot*2+stand_score_ni

