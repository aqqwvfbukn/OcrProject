FROM python:3.10.1
ENV PYTHONUNBUFFERED 1
RUN mkdir /OcrProject
WORKDIR /OcrProject
ADD . /OcrProject

# 更新pip并安装依赖
RUN pip3 install pip -U -i https://pypi.tuna.tsinghua.edu.cn/simple/
RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
RUN pip3 uninstall opencv-python -y
RUN pip3 install opencv-python-headless -i https://mirrors.aliyun.com/pypi/simple

# 设置环境变量
ENV SPIDER=/OcrProject