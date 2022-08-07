# 从Docker仓库中拉去带有Python3.7的Linux环境
FROM python:3.7
#
# # 设置 python 环境变量
ENV PYTHONUNBUFFERED 1
# 换源解决aptget超时
RUN  sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN  apt-get clean

# 添加这两行
RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev -y
# # 创建 code 文件夹并将其设置为工作目录
RUN mkdir /code
WORKDIR /code
# # 更新 pip并换源
RUN pip install pip -U -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple
RUN pip config set install.trusted-host mirrors.aliyun.com

# # 将 requirements.txt 复制到容器的 code 目录
ADD requirements.txt /code/
# # 安装库
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# # 将当前目录复制到容器的 code 目录
ADD . /code/
