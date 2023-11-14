# savannah-review

主要有两处修改

## 添加记录下载url文件

为了解决大批量下载过程中因为网络原因中断后从头开始的问题，添加一个file_url.txt用于记录已经下载的url。当执行download函数时，首先判断待下载的文件是否已经下载。

![](D:\大学\Typora图片\20231113\QQ图片20231113180614.png)

## 添加对find_all的报错处理

极少数页面会存在find_all的AttributeError

![](D:\大学\Typora图片\20231113\QQ图片20231113175842.png)

其web页面如下：

![](D:\大学\Typora图片\20231113\QQ图片20231113180044.png)

貌似还可以下载，但是由于这种情况较少，目前是不做任何处理，只是输出相关url。

添加对该错误的处理代码：

![](D:\大学\Typora图片\20231113\QQ图片20231113180709.png)

以下是会触发该错误的url

```
# FLAG
# http://download.savannah.gnu.org/releases/akfquiz/
# http://download.savannah.gnu.org/releases/bibledit/source/web/
# http://download.savannah.gnu.org/releases/comma/commaspec-html/
# http://download.savannah.gnu.org/releases/comma/doxygen/
# http://download.savannah.gnu.org/releases/construo/doxygen/
# http://download.savannah.gnu.org/releases/getfem/html/homepage/
# http://download.savannah.gnu.org/releases/getht/
# http://download.savannah.gnu.org/releases/liboggpp/dox/
# http://download.savannah.gnu.org/releases/swarm/apps/objc/contrib/lunabook/
# http://download.savannah.gnu.org/releases/swarm/docs/refbook-java/
```



对于整个代码平台，已经不下载文件的遍历过一遍，共有40505个下载链接。

依旧存在一个问题，部分文件存在签名和验证文件或者不同压缩版本的文件，但是没有统一规范，也不太好区分，目前是下载所有的文件。
