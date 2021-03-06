# Detect torch
import platform
import subprocess

try:
    import torch
    torch.no_grad
    # _TORCH_INSTALLED = torch.__version__ >= "1.11"
    _TORCH_INSTALLED = True
except ImportError:
    print("Required torch is not detected!")
    _TORCH_INSTALLED = False
except AttributeError:
    print("torch properly not rightly installed!, which has not attribute no_grad. Ready to uninstall torch")
    subprocess.run(['pip', 'uninstall', 'torch'])
    _TORCH_INSTALLED = False
    # exit(0)

if not _TORCH_INSTALLED:
    if platform.system() == 'Windows':
        print('Install torch on Windows via https://download.pytorch.org/whl/cu113", please wait')
        subprocess.run(['pip', 'install', 'torch', 'torchaudio', 'torchvision',
                        '--extra-index-url', 'https://download.pytorch.org/whl/cu113'])
        print('Torch installed finished')
    elif platform.system() == 'Darwin':
        print('Install torch on Mac which is not supported on cuda')
        subprocess.run(['pip', 'install', 'torch', 'torchaudio', 'torchvision'])
        print('Torch installed finished')
    else:
        print('Install torch on Linux via "https://download.pytorch.org/whl/cu113", please wait')
        subprocess.run(['pip', 'install', 'torch', 'torchaudio', 'torchvision',
                        '--extra-index-url', 'https://download.pytorch.org/whl/cu113'])
        print('Torch installed finished')


import torch
import os
from PIL import Image
import numpy as np
from pathlib import Path
import torch.nn as nn
import torchvision.transforms as transforms


class BasicBlock(nn.Module):
    """Basic Block for resnet 18 and resnet 34

    """
    # BasicBlock and BottleNeck block
    # have different output size
    # we use class attribute expansion
    # to distinct
    expansion = 1

    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()

        # residual function
        self.residual_function = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels * BasicBlock.expansion, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels * BasicBlock.expansion)
        )

        # shortcut
        self.shortcut = nn.Sequential()

        # the shortcut output dimension is not the same with residual function
        # use 1*1 convolution to match the dimension
        if stride != 1 or in_channels != BasicBlock.expansion * out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels * BasicBlock.expansion, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels * BasicBlock.expansion)
            )

    def forward(self, x):
        return nn.ReLU(inplace=True)(self.residual_function(x) + self.shortcut(x))


class BottleNeck(nn.Module):
    """Residual block for resnet over 50 layers

    """
    expansion = 4

    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.residual_function = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, stride=stride, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels * BottleNeck.expansion, kernel_size=1, bias=False),
            nn.BatchNorm2d(out_channels * BottleNeck.expansion),
        )

        self.shortcut = nn.Sequential()

        if stride != 1 or in_channels != out_channels * BottleNeck.expansion:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels * BottleNeck.expansion, stride=stride, kernel_size=1, bias=False),
                nn.BatchNorm2d(out_channels * BottleNeck.expansion)
            )

    def forward(self, x):
        return nn.ReLU(inplace=True)(self.residual_function(x) + self.shortcut(x))


class BigResNet(nn.Module):

    def __init__(self, block, num_block, num_classes=1):
        super().__init__()

        self.in_channels = 64

        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True))
        # we use a different inputsize than the original paper
        # so conv2_x's stride is 1
        # self.conv2_x = self._make_layer(block, 64, num_block[0], 1)
        # self.conv3_x = self._make_layer(block, 128, num_block[1], 2)
        # self.conv4_x = self._make_layer(block, 256, num_block[2], 2)
        # self.conv5_x = self._make_layer(block, 512, num_block[3], 2)
        # self.avg_pool = nn.AdaptiveAvgPool2d((1, 1))
        # self.fc = nn.Linear(512 * block.expansion, num_classes)

        self.conv2_x = self._make_layer(block, 64, num_block[0], 1)
        self.conv3_x = self._make_layer(block, 64, num_block[1], 2)
        self.conv4_x = self._make_layer(block, 64, num_block[2], 2)
        self.conv5_x = self._make_layer(block, 64, num_block[3], 2)
        self.avg_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(64 * block.expansion, num_classes)

        # self.fc_out = nn.Linear(num_classes, 1)
        # self.sigmoid = torch.nn.Sigmoid()

    def _make_layer(self, block, out_channels, num_blocks, stride):
        """make resnet layers(by layer i didnt mean this 'layer' was the
        same as a neuron netowork layer, ex. conv layer), one layer may
        contain more than one residual block

        Args:
            block: block type, basic block or bottle neck block
            out_channels: output depth channel number of this layer
            num_blocks: how many blocks per layer
            stride: the stride of the first block of this layer

        Return:
            return a resnet layer
        """

        # we have num_block blocks per layer, the first block
        # could be 1 or 2, other blocks would always be 1
        strides = [stride] + [1] * (num_blocks - 1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_channels, out_channels, stride))
            self.in_channels = out_channels * block.expansion

        return nn.Sequential(*layers)

    def forward(self, x):
        output = self.conv1(x)
        output = self.conv2_x(output)
        output = self.conv3_x(output)
        output = self.conv4_x(output)
        output = self.conv5_x(output)
        output = self.avg_pool(output)
        output = output.view(output.size(0), -1)
        output = self.fc(output)
        # output = self.fc_out(output)
        # output = self.sigmoid(output)
        return output


class SmallResNet(nn.Module):

    def __init__(self, block, num_block, num_classes=1):
        super().__init__()

        self.in_channels = 64

        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True))
        # we use a different inputsize than the original paper
        # so conv2_x's stride is 1
        # self.conv2_x = self._make_layer(block, 64, num_block[0], 1)
        # self.conv3_x = self._make_layer(block, 128, num_block[1], 2)
        # self.conv4_x = self._make_layer(block, 256, num_block[2], 2)
        # self.conv5_x = self._make_layer(block, 512, num_block[3], 2)
        # self.avg_pool = nn.AdaptiveAvgPool2d((1, 1))
        # self.fc = nn.Linear(512 * block.expansion, num_classes)

        # self.conv2_x = self._make_layer(block, 64, num_block[0], 1)
        # self.conv3_x = self._make_layer(block, 64, num_block[1], 2)
        # self.conv4_x = self._make_layer(block, 64, num_block[2], 2)
        self.conv5_x = self._make_layer(block, 64, num_block[3], 2)
        self.avg_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(64 * block.expansion, num_classes)

        # self.fc_out = nn.Linear(num_classes, 1)
        # self.sigmoid = torch.nn.Sigmoid()

    def _make_layer(self, block, out_channels, num_blocks, stride):
        """make resnet layers(by layer i didnt mean this 'layer' was the
        same as a neuron netowork layer, ex. conv layer), one layer may
        contain more than one residual block

        Args:
            block: block type, basic block or bottle neck block
            out_channels: output depth channel number of this layer
            num_blocks: how many blocks per layer
            stride: the stride of the first block of this layer

        Return:
            return a resnet layer
        """

        # we have num_block blocks per layer, the first block
        # could be 1 or 2, other blocks would always be 1
        strides = [stride] + [1] * (num_blocks - 1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_channels, out_channels, stride))
            self.in_channels = out_channels * block.expansion

        return nn.Sequential(*layers)

    def forward(self, x):
        output = self.conv1(x)
        # output = self.conv2_x(output)
        # output = self.conv3_x(output)
        # output = self.conv4_x(output)
        output = self.conv5_x(output)
        output = self.avg_pool(output)
        output = output.view(output.size(0), -1)
        output = self.fc(output)
        return output


# ?????????????????????
def model_init(version_id, gpu=True):

    cache = {}

    def singleton(version_id, gpu):
        args = (version_id, gpu)
        if args not in cache:
            # ???????????????????????????????????????
            module = globals()[version_id]
            # ???????????????
            net = module(block=BasicBlock, num_block=[1, 1, 1, 1], num_classes=6)
            # print('net', net)
            # ??????????????????
            pth_dict = torch.load(version_pth)
            # ??????????????????????????????
            net.load_state_dict(pth_dict)
            net.eval()
            cache[args] = net
        return cache[args]

    # validate version_id
    pth = os.path.join(str(Path(__file__).resolve().parent), 'models')
    version_pth = os.path.join(pth, version_id)
    version_pth = version_pth if version_pth.endswith('.pth') else '.'.join([version_pth, 'pth'])
    if not os.path.exists(version_pth):
        raise FileNotFoundError('file: %s not found' % version_pth)

    # # ???????????????????????????????????????
    # module = globals()[version_id]
    # # print('globals module', module, type(module))
    # # ??????torch ??????
    # net = module(block=BasicBlock, num_block=[1, 1, 1, 1], num_classes=6)
    # # print('net', net)
    # pth_dict = torch.load(version_pth)
    # net.load_state_dict(pth_dict)
    # net.eval()

    # ??????????????????????????????????????????
    net = singleton(version_id, gpu)

    if gpu:
        net.cuda()

    globals()['net'] = net
    globals()['gpu'] = gpu
    return net
    # print('globals', globals()['net'], globals()['gpu'])


# infer_from_files(tga_file_path:List[str])->np.array
# def infer_from_files(tga_dir):
def infer_from_files(tga_files):
    func = transforms.Compose([transforms.ToTensor(), ])
    batch = []
    # for tga_file in os.listdir(tga_dir):
    #     tga_file = os.path.join(tga_dir, tga_file)
    #     if os.path.exists(tga_file):
    #         image_pic = Image.open(tga_file)
    #         image = np.array(image_pic.getdata()).reshape(image_pic.size[0], image_pic.size[1], -1)
    #         image = image[:, :, 0:3]
    #         image = (image / 255 - 0.5) * 2
    #         # image = self.transform(image)
    #         image = func(image)
    #         batch.append(image)
    for tga_file in tga_files:
        image_pic = Image.open(tga_file)
        image = np.array(image_pic.getdata()).reshape(image_pic.size[0], image_pic.size[1], -1)
        image = image[:, :, 0:3]
        image = (image / 255 - 0.5) * 2
        # image = self.transform(image)
        image = func(image)
        batch.append(image)

    batch = torch.stack(batch)
    batch = batch.type(torch.FloatTensor)
    # load global variable
    net = globals()['net']
    gpu = globals()['gpu']
    if gpu:
        batch = batch.cuda()
    out = net(batch)
    out = out.cpu().detach().numpy()
    return out

# infer_from_file(tga_file_path:str)->np.array
def infer_from_file(tga_file):
    func = transforms.Compose([transforms.ToTensor(), ])
    batch = []
    # for tga_file in tga_paths:
    if os.path.exists(tga_file):
        image_pic = Image.open(tga_file)
        image = np.array(image_pic.getdata()).reshape(image_pic.size[0], image_pic.size[1], -1)
        image = image[:, :, 0:3]
        image = (image / 255 - 0.5) * 2
        # image = self.transform(image)
        image = func(image)
        batch.append(image)
    batch = torch.stack(batch)
    batch = batch.type(torch.FloatTensor)
    # load global variable
    net = globals()['net']
    gpu = globals()['gpu']
    if gpu:
        batch = batch.cuda()
    out = net(batch)
    out = out.cpu().detach().numpy()
    return out


# infer_from_array(np_array:np.array)->np.array
def infer_from_array(batch):
    batch = torch.tensor(batch, dtype=torch.float32)
    # load global variable
    net = globals()['net']
    gpu = globals()['gpu']

    if gpu:
        batch = batch.cuda()
    out = net(batch)
    out = out.cpu().detach().numpy()
    return out


# infer_from_tensor(tensor:tensor)->tensor
def infer_from_tensor(tensor):
    # load global variable
    net = globals()['net']
    gpu = globals()['gpu']
    if gpu:
        tensor = tensor.cuda()
    out = net(tensor)
    out = out.cpu().detach().numpy()
    return out
