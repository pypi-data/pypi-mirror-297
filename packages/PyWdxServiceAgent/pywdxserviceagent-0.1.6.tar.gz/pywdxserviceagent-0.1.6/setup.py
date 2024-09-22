from setuptools import setup, find_packages

setup(
    name="PyWdxServiceAgent",  # 패키지 이름
    version="0.1.6",  # 버전
    packages=find_packages(),  # 패키지들을 자동으로 찾음
    install_requires=[
        # 여기에 필요한 패키지 의존성을 작성
        # 예: 'numpy>=1.21.0', 'pandas'
    ],
    author="genfeel",
    author_email="genfeel@hotmail.com",
    description="Wdworker BackendService Agent",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/genfeel/Wdworker",  # GitHub 리포지토리 URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # MIT 라이선스 (변경 가능)
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 파이썬 최소 버전
)
