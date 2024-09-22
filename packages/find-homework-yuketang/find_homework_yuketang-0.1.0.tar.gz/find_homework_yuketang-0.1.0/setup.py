from setuptools import setup, find_namespace_packages

setup(
    name='find_homework_yuketang',  # 项目名称
    version='0.1.0',  # 版本号
    author='Diluc',  # 作者
    author_email='1727327536@qq.com',  # 作者邮箱
    description='just find homework',  # 项目描述
    url='https://github.com/yourusername/your_project',  # 项目主页
    packages=find_namespace_packages(),  # 自动找到项目中的所有包
    install_requires=[
        'requests',
        'selenium'
    ],
    python_requires='>=3.12',  # Python版本要求,
    entry_points={
        'console_scripts': [
            'find-homework=find_homework_yuketang.main:cli',
        ],
    },
)