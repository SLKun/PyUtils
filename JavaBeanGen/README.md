# JavaBean Generator

## 简介

自动生成JavaBean的小工具, 只需要将参数填入json配置文件就可以自动生成. 

## RoadMap

- 维护一个全局的Environment [ok]
- 每一层将Environment入栈 [ok]
- 检查每一层的数据类型    [ok]
    - 如果是其他类型则默认加入Environment
	- 如果是dict, 则认为是下一层
	- 如果是List
	    - 如果下一层是基本类型, 则以,分隔加入env
	    - 如果下一层是dict, 且dict的元素全为基本类型, 而且名称与上层前缀相同
	        - 则认为是并列数据 prefix_name_index
	        - 存在index则按照index的次序进行排序, 从0开始
	        - 如果不存在index则按照文本先后顺序排序拼接
- 允许key&进行部分填入 [ok]
	- modifier&填入public, 子层可以填入其他modifier同时采用父层Modifier
	- key$标记不采用部分填入, 而采用该值
- 允许添加name$Method指定解析方式
		- list$arg
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