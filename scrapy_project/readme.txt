注意：由于搜狗（或者大多搜索引擎）的限制，单次搜索最多显示1000条条目，所以即使有3000+条结果，该爬虫也只能爬取1000条数据。 建议使用不同的搜索关键字来爬取更多的内容。

用法：
*由于搜狗需要二维码登录，该爬虫会让用户手动进行登录。
1.确保电脑安装了python， 并下载了 scrapy，MySQL-python(MySQLdb)以及selenium包。下载Chrome以及Chromedriver（目录下已提供）。准备好自己的手机。
2.将sougou文件夹至于桌面（该说明以桌面为准，可以根据自己需要自行调整目录）。
3.打开sougou/sougou/spider/results.py, 将第13行的地址改为自己的Chromedriver的地址
4.从开始菜单打开cmd窗口
5.输入‘cd Desktop’,回车，再输入‘cd sougou’,回车，最后输入scrapy crawl results -o items.csv,回车。
6.在弹出的Chrome浏览器中点击右上角的登录，用手机扫码登录，然后在搜索栏输入想搜索的关键字，回车或点击进入搜索界面。
7.在cmd菜单中‘ready？’条目下随意输入，再回车。
8.等待爬虫自动运行，完成。
9.当搜狗发现频繁访问时会跳出验证码网页，请输入验证码后再在程序界面输入no(除yes外其他都可以），回车，程序将继续运行。
10.当爬到第100页时请在程序界面输入yes,回车。

**关于导入mysql：
要设置code中用户名，密码以及数据库名称，并确认CSV路径正确，在mysql端建立table时一定要注意data type，建议使用如下语句：
CREATE TABLE `sougoutable` (
  `title` varchar(100) DEFAULT NULL,
  `pubdate` varchar(100) DEFAULT NULL,
  `author` varchar(100) DEFAULT NULL,
  `content` mediumtext
)