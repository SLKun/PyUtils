# JavaBean Generator

## 简介

自动生成JavaBean的小工具, 只需要将参数填入json配置文件就可以自动生成. 

## RoadMap

- 维护一个全局的Environment
- 每一层将Envinronment入栈
- 检查每一层的数据类型
	- 如果是dict, 则认为是下一层
	- 如果是List, 则将其并列展开
	- 允许添加name$Method指定解析方式
		- list$arg
	- 如果是其他类型则默认加入Environment
- 允许prefix_name避免单元素的List
	- arg_type, arg_name
- 允许key&进行部分填入
	- modifier&填入public, 子层可以填入其他modfier同时采用父层Modifier
- 允许name#\d分组
	- Varibles#1, Varibles#2
	- 不同的组可以使用不同的全局参数
- 允许自定义变量%var%Exception
	- 可以嵌入到文本中去
- 内建特殊的处理函数
	- 可以通过&func:1执行
- 允许模糊化处理
	- *arg*匹配key
- 允许使用python外的argv引入需要执行的处理函数
- 更加友好的默认化处理和报错
- 生成函数时, 可以根据模板和holder进行生成
- 可以将JSON映射为Python类
- 可以指定前端对接其他数据类型, 比如xml