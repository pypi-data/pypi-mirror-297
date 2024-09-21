from setuptools import setup

setup(name='updns',
      version="2.0",
      description="用于更新本地自定义域名的DNS解析记录，以确保正常访问服务。",
      keywords='python、PyPi source、terminal',
      author='sanfeng',
      license='MIT',
      include_package_data=True,
      zip_safe=True,
      classifiers=[],
      packages=["updns"],
      install_requires=["rich"],
      entry_points={
          'console_scripts': [
              'updns = updns.updns:main'
          ]
      },
      )
