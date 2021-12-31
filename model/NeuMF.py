import torch.nn as nn
import torch
from model.GMF import GMF
from model.MLP import MLP

class NeuMF(nn.Module):
    def __init__(self,
                 num_users: int,
                 num_items: int,
                 num_factor: int = 8,
                 use_pretrain: bool = False,
                 layer=None, # layer for MLP
                 ):
        super(NeuMF,self).__init__()
        self.use_pretrain = use_pretrain
        # layer for MLP
        if layer is None:
            layer = [32,16, 8]

        if use_pretrain == True:
            # not implemented
            pass
        else:
            self.GMF=GMF(num_users,num_items,num_factor,use_pretrain=use_pretrain)
            self.MLP=MLP(num_users,num_items,num_factor,layer,use_pretrain=use_pretrain)
        self.last_layer=nn.Sequential(nn.Linear(2,1),nn.Sigmoid())

    def _init_weight(self):
        if not self.use_pretrain:
            for layer in self.last_layer:
                if isinstance(layer,nn.Linear):
                    nn.init.normal_(layer.weight,std=1e-2)
                    layer.bias.data.zero()

    def forward(self,user,item):
        before_last_layer_output = torch.cat((self.GMF(user,item),self.MLP(user,item)),dim=-1)
        output = self.last_layer(before_last_layer_output)
        return output
