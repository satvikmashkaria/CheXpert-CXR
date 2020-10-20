from __future__ import print_function
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms, models
from collections import OrderedDict
import torchvision
from resnext import resnext101_64x4d
from vgg import vgg19

from hparams import hparams

class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()
        self.feature = models.densenet121(num_classes=1000, pretrained='imagenet', progress=True)
        num_ftrs = self.model.classifier.in_features
        self.feature.classifier = nn.Sequential()
        self.intermediate = nn.Sequential(
                                nn.Linear(num_ftrs, 512),
                                nn.ReLU(True),
                                nn.Dropout(hparams.drop_rate),
                            )
        self.classifier = nn.Sequential(
                                nn.Linear(9*512, 4096),
                                nn.ReLU(True),
                                nn.Dropout(hparams.drop_rate),
                                nn.Linear(4096, 4096),
                                nn.ReLU(True),
                                nn.Dropout(hparams.drop_rate),
                                nn.Linear(4096, hparams.num_classes),
                            )

#         self.feature = vgg19(num_classes=1000, pretrained='imagenet', progress=True)
#         num_ftrs = 512 * 2 * 2 #self.model.classifier.in_features
#         self.feature.classifier = nn.Sequential()
#         self.feature.avgpool = nn.Sequential()
#         self.intermediate = nn.Sequential(
#                                 nn.Linear(num_ftrs, 512),
#                                 nn.ReLU(True),
#                                 nn.Dropout(hparams.drop_rate),
#                             )
#         self.classifier = nn.Sequential(
#                                 nn.Linear(9*512, 4096),
#                                 nn.ReLU(True),
#                                 nn.Dropout(hparams.drop_rate),
#                                 nn.Linear(4096, 4096),
#                                 nn.ReLU(True),
#                                 nn.Dropout(hparams.drop_rate),
#                                 nn.Linear(4096, hparams.num_classes),
#                             )

        

    def forward(self, x):

        bs = x.shape[0]
#         print(x.shape)
        x = x.reshape(-1, 3, hparams.image_shape[0], hparams.image_shape[1])
#         print(x.shape)
        x = self.model.feature(x)
#         print(x.shape)
        x = self.intermediate(x)
#         print(x2.shape)
        x = x.reshape(bs, 9, -1)
#         print(x2.shape)
        x = x.reshape(bs, -1)
#         print(x2.shape)
        x = self.classifier(x)
#         print(x3.shape)
        return x