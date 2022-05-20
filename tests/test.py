from digitalBrain.api import model_init, infer_from_files, infer_from_file

if __name__ == '__main__':

    # 在安装digitalBrain环境中执行
    version_id = 'BigResNet'
    # version_id = 'SmallResNet'
    model_init(version_id, gpu=False)

    out_1 = infer_from_files([r'D:\liuhx\数字大脑\PycharmProjects\sdk\tests\00018ee1333e2fb9a1978bde304f73bc_[00000_00000_00128_00128].tga'])
    print('infer_from_files', out_1)
    out_2 = infer_from_file(r'D:\liuhx\数字大脑\PycharmProjects\sdk\tests\00018ee1333e2fb9a1978bde304f73bc_[00000_00000_00128_00128].tga')
    print('infer_from_file', out_2)

    # # 在digitalBrain环境保存单独的模型
    # import torch
    # from digitalBrain.api import SmallResNet, BigResNet, BasicBlock
    # module = BigResNet(block=BasicBlock, num_block=[1, 1, 1, 1], num_classes=6)
    # torch.save(module, r'D:\liuhx\数字大脑\PycharmProjects\sdk\tests\BigResNet.model')

    # # 验证是否是独立的模型, 在没有digitalBrain环境中测试，针对于PDF第三点，模型文件为独立存在
    # import torch
    # net = torch.load(r'D:\liuhx\数字大脑\PycharmProjects\sdk\tests\BigResNet.model')
    # print('net', net)
