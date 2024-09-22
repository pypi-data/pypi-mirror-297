import torch
if torch.cuda.is_available():
    import hamming_l2_cuda

class HammingL2Function(torch.autograd.Function):
    @staticmethod
    def forward(ctx, luts, gamma):
        output = hamming_l2_cuda.forward(luts) if luts.is_cuda else None
        if output is None: raise "HammingL2 CPU not Implemented"
        ctx.save_for_backward(luts, gamma)
        return output

    @staticmethod
    def backward(ctx, output_grad):
        luts, gamma = ctx.saved_tensors
        luts_grad = hamming_l2_cuda.backward(luts, float(gamma)) if luts.is_cuda else None
        if luts_grad is None: raise ValueError("HammingL2 CPU not Implemented")
        return luts_grad, None

class HammingL2(torch.nn.Module):
    def __init__(self, gamma):
        super().__init__()
        self.gamma = gamma
    
    def forward(self, model):
        loss = 0
        for param in model.parameters():
            if param.requires_grad and param.__dict__.get('is_lut', False):
                loss += HammingL2Function.apply(param, torch.tensor(self.gamma)).mean()
        return loss
