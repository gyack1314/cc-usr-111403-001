# 资料语义与接口边界

关系AST只含scan、eq-join、select、project和union-all；没有否定、聚合和外连接。每个物理源行的token为(table,snapshot,row_id)，同行内容相同但row_id不同仍独立。每个输入token在自然数多项式中是变量，join为乘，union-all及投影后的同值归并为加；次数和系数均不可布尔化。来源解释在固定快照上有效。将被屏蔽token赋0、其余赋1得到该输出行仍有的重数。源同表被两个别名扫描时token身份相同，可能产生平方。已有rows.py实现无来源的小规模参考解释器，proofs.py只实现叶子token的身份编码。新增结构可以因子化，无需枚举所有单项式；有预算的展开结果须给complete标志。

proofs.py只编码来源叶子；rows.py是原有的无来源查询。普通行输出不含推导图。

正文摘要绑定完整值，样例数据不限定输入规模；错误不等同空结果，接口使用中文错误说明。
