from setuptools import setup, find_packages 
setup(
    name="pyaqcv", # 用自己的名替换其中的YOUR_USERNAME_
    version="1.1.41",    #包版本号，便于维护版本
    author="aqrose",    #作者，可以写自己的姓名
    author_email="developer@aqrose.com",    #作者联系方式，可写自己的邮箱地址
    description="Aqcv package",#包的简述
    long_description="Aqcv package",    #包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    url="",    #自己项目地址，比如github的项目地址
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',    #对python的最低版本要求
    packages=find_packages(),  
    package_data={  
        'pyaqcv': ['./*.dll', './*.py', './*.pyd'],  # 确保DLL文件被包含  
    },  
    install_requires=['numpy'],
    include_package_data=True
)

