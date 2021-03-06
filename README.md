# SDK


### 布局说明
------digitalBrain
------------api.py
------------models
--------------BigResNet.pth
--------------SmallResNet.pth


### 安装方式
```python
	pip install digitalBrain-1.3rc0.tar.gz
    pip uninstall digitalBrain
```


### model_init(version_id, gpu:bool=True)

接口地址：model_init

接口备注：根据传入的version_id, 初始化模型

调用示例：
```python
from digitalBrain.api import model_init

model_init(version_id='SmallResNet')

```
返回示例说明：
空


### infer_from_files(tga_files_path:list[str]) -> np.array

接口地址：infer_from_files

接口备注：传入一些列tga文件列表进行计算

调用示例：
```python
from digitalBrain.api import infer_from_files
output = infer_from_files([r'C:\Users\Administrator\Desktop\static_tga'])
```

返回示例说明：
```python
[[0.42290255, 0.6763047, 0.9308898, 1.3593276, 1.7301302, 1.9988524 ]
 [0.12040028, 0.2568135, 0.38907474, 0.6280041, 0.8635222, 1.0941315 ]
 [0.10534315, 0.23383129, 0.35158077, 0.52322376, 0.6611633, 0.76737595]]
```


### infer_from_file(tga_file:str) -> np.array

接口地址：infer_from_file

接口备注：根据tga文件计算

调用示例：
```python
from digitalBrain.api import infer_from_file
output = infer_from_file(r'C:\Users\Administrator\Desktop\static_tga\test.tga')
```

返回示例说明：
```python
[[ 1.771759, 3.2017446, 4.5778866, 7.194329, 9.188715, 10.9264]]
```


### infer_from_array(batch:np.array) -> np.array

接口地址：infer_from_array

接口备注：基于np.array进行计算

调用示例：
```python
from digitalBrain.api import infer_from_array
output = infer_from_array(...)
```

返回示例说明：
```python
[[ 1.771759, 3.2017446, 4.5778866, 7.194329, 9.188715, 10.9264]]
```


### infer_from_tensor(tensor:torch.tensor) -> np.array

接口地址：infer_from_tensor

接口备注：基于tensor对象进行计算

调用示例：
```python
from digitalBrain.api import infer_from_tensor
output = infer_from_tensor(...)
```

返回示例说明：
```python
[[ 1.771759, 3.2017446, 4.5778866, 7.194329, 9.188715, 10.9264]]
```
