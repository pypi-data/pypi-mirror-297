from setuptools import setup, find_packages

setup(
    name="moregoodturtle",  # 你的包的名字
    version="0.1.0",  # 包的版本
    packages=find_packages(),  # 自动查找子目录中的包
    install_requires=[],  # 列出任何依赖包
    include_package_data=True,  # 包括数据文件
    description="this page was good for turtle",
    author="mopi studio",
    author_email="f9qz3dydpx@tippabble.com",
    url="https://https://github.com/lldxlzy/made-moregood-turtle-on-python",  # 可以放你的包的主页或仓库地址
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 指定最低 Python 版本
    license='MIT'
)