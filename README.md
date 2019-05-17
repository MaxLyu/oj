# OnlineJudge难度与正确度的相关性检验
<p>　　本着做题的心态，上了东莞理工学院的 oj&nbsp;网；在选择难度的时候发现有些题目通过率和难度可能存在着某些关系，于是决定爬下这些数据简单查看一下是否存在关系。</p>
<p>&nbsp;</p>
<p><span style="font-size: 15px;"><strong>一、新建项目</strong></span></p>
<p>　　我是用&nbsp;Scrapy&nbsp;框架爬取的（因为刚学没多久，顺便练练手）。首先，先新建&nbsp;project （下载 Scarpy 部分已省略），在控制台输入&nbsp;scrapy&nbsp;startproject&nbsp;onlineJudge（其中，&nbsp;onlineJudge为项目名称），敲击回车键新建项目完成。</p>
<p><strong><span style="font-size: 15px;">二、明确目的</span></strong></p>
<p>　　在动手写代码之前，先分析一下网页结构。网站是通过动态加载的，数据通过 json&nbsp;文件加载。</p>
<p><img src="https://img2018.cnblogs.com/blog/1458123/201902/1458123-20190214223735371-940491986.png" alt="" /></p>
<p>&nbsp;</p>
<p>　　1、明确要爬取的目标： http://oj.dgut.edu.cn/problems&nbsp; 网站里的题目，难度，提交量，通过率。在查找&nbsp;json 的时候发现只有通过数，那么通过率就要自己计算。</p>
<p>　　2、打开 onlineJudge 目录下的 items.py&nbsp;写下如下代码：</p>
<div class="cnblogs_code">
<pre><span style="color: #0000ff;">class</span><span style="color: #000000;"> OnlinejudgeItem(scrapy.Item):

    id </span>= scrapy.Field()                    
    title = scrapy.Field()                 
    difficulty = scrapy.Field()            
    submissionNo = scrapy.Field()      　　　
    acceptedNo = scrapy.Field()         　
    passingRate = scrapy.Field()           
</div>
<p><strong><span style="font-size: 15px;">三、制作爬虫</span></strong></p>
<p>　　1、在当前目录下输入命令：<code>scrapy genspider oj "oj.dgut.edu.cn" （其中 oj 是爬虫的名字，"oj.dgut.edu.cn"算是一个约束，规定一个域名）</code></p>
<p>　　2、打开 onlineJudge/spiders&nbsp;下的&nbsp;ojSpider.py ，增加或修改代码为：</p>
<div class="cnblogs_code">
<pre>
<code>
import scrapy
import json
from onlineJudge.items import OnlinejudgeItem

class OjSpider(scrapy.Spider):
    name = 'oj'        # 爬虫的名字
    allowed_domains = ['oj.dgut.edu.cn']　　　　　# 域名范围
    offset = 0
    url = 'http://oj.dgut.edu.cn/api/xproblem/?limit=20&offset='
    start_urls = [url + str(offset)]　　　　　　　# 爬取的URL元祖/列表

    def parse(self, response):
        data = json.loads(response.text)['data']['results']
        if len(data):
            for i in range(len(data)):
                submissionNo = data[i]['submission_number']
                acceptedNo = data[i]['accepted_number']
                try:
                    passingRate = round((int(acceptedNo)/int(submissionNo)) * 100, 2)
                except ZeroDivisionError as e:
                    passingRate = 0
    
                strPR = str(passingRate) + "%"
    
                item = OnlinejudgeItem()
    
                item['id'] = data[i]['_id']
                item['title'] = data[i]['title']
                item['difficulty'] = data[i]['difficulty']
                item['submissionNo'] = submissionNo
                item['acceptedNo'] = acceptedNo
                item['passingRate'] = strPR
    
                yield item

                print(i)
            self.offset += 20
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
</code>
</pre>
</div>
<p><span style="font-size: 15px;"><strong>四、存储数据</strong></span></p>
<p>&nbsp; &nbsp; 1、打算将数据存储为&nbsp;excel&nbsp;文档，要先安装 openpyxl&nbsp;模块，通过 pip&nbsp;install openpyxl&nbsp;下载。</p>
<p>&nbsp; &nbsp; 2、下载完成后，在&nbsp;pipelines.py&nbsp;中写入如下代码</p>
<div class="cnblogs_code">
<pre>
<code>
from openpyxl import Workbook

class OnlinejudgePipeline(object):

    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active                # 激活工作簿
        self.ws.append(['编号', '标题', '难度', '提交量', '正确数', '正确率'])    # 设置表头

    def process_item(self, item, spider):
        line = [item['id'], item['title'], item['difficulty'],
                item['submissionNo'], item['acceptedNo'], item['passingRate']]
        self.ws.append(line)
        self.wb.save('oj.xlsx')
        return item
</code>
</pre>
</div>
<p><span style="font-size: 15px;"><strong>五、设置 settings.py&nbsp;</strong></span></p>
<p>&nbsp; &nbsp; 修改并增加代码：</p>
<div class="cnblogs_code">
<pre>LOG_FILE = <span style="color: #800000;">"</span><span style="color: #800000;">oj.log</span><span style="color: #800000;">"</span><span style="color: #000000;">

ROBOTSTXT_OBEY </span>=<span style="color: #000000;"> True

ITEM_PIPELINES </span>=<span style="color: #000000;"> {
    </span><span style="color: #800000;">'</span><span style="color: #800000;">onlineJudge.pipelines.OnlinejudgePipeline</span><span style="color: #800000;">'</span>: 300<span style="color: #000000;">,
}</span></pre>
</div>
<p><span style="font-size: 15px;"><strong>六、运行爬虫</strong></span></p>
<p>　　在当前目录下新建一个 main.py&nbsp;并写下如下代码</p>
<div class="cnblogs_code">
<pre><span style="color: #0000ff;">from</span> scrapy <span style="color: #0000ff;">import</span><span style="color: #000000;"> cmdline

cmdline.execute(</span><span style="color: #800000;">"</span><span style="color: #800000;">scrapy crawl oj</span><span style="color: #800000;">"</span>.split())</pre>
</div>
<p>　　然后运行&nbsp;main.py&nbsp;文件。</p>
<p>&nbsp;</p>
<p>　　于是，想要的数据就被爬下来了</p>
<p><img src="https://img2018.cnblogs.com/blog/1458123/201902/1458123-20190214223415234-608524774.png" alt="" /></p>
<p>&nbsp;</p>
<p><strong><span style="font-size: 15px;">七、分析数据</span></strong></p>
<p>　　分析数据之前，先安装好&nbsp;numpy，pandas，matplotlib，xlrd。</p>
<div class="cnblogs_code">
<pre><span style="color: #0000ff;">import</span><span style="color: #000000;"> pandas as pd
</span><span style="color: #0000ff;">import</span><span style="color: #000000;"> xlrd

data </span>= pd.read_excel(<span style="color: #800000;">"</span><span style="color: #800000;">../onlineJudge/onlineJudge/oj.xlsx</span><span style="color: #800000;">"</span><span style="color: #000000;">)　　<span style="color: #008000;"># 导入 excel 文件</span>
data.describe()<br /></span></pre>
</div>
<p><img src="https://img2018.cnblogs.com/blog/1458123/201902/1458123-20190214221423475-1763069508.png" alt="" /></p>
<p>　　通过观察，数据没有异常值以及确实值，虽然提交量和正确数有为0的部分，但属于正常范围，不做处理。</p>
<div class="cnblogs_code">
<pre>data = data.set_index('编号')　　<span style="color: #008000;"># 设置编号为索引</span><br />data.head()　　　　　　　　　　　　<span style="color: #008000;"># 显示前五条信息</span></pre>
</div>
<p><img src="https://img2018.cnblogs.com/blog/1458123/201902/1458123-20190214221841620-1888312435.png" alt="" /></p>
<div class="cnblogs_code">
<pre><span style="color: #0000ff;">from</span> matplotlib <span style="color: #0000ff;">import</span><span style="color: #000000;"> pyplot as plt
</span><span style="color: #0000ff;">import</span><span style="color: #000000;"> matplotlib.style as psl
</span>%<span style="color: #000000;">matplotlib inline

psl.use(</span><span style="color: #800000;">'</span><span style="color: #800000;">seaborn-colorblind</span><span style="color: #800000;">'</span>)    <span style="color: #008000;">#</span><span style="color: #008000;"> 设置图表风格</span>
plt.rcParams[<span style="color: #800000;">'</span><span style="color: #800000;">font.sans-serif</span><span style="color: #800000;">'</span>]=[<span style="color: #800000;">'</span><span style="color: #800000;">SimHei</span><span style="color: #800000;">'</span>] <span style="color: #008000;">#</span><span style="color: #008000;">用来正常显示中文标签</span></pre>
</div>
<p>　　查看题目各难度的数目：</p>
<div class="cnblogs_code">
<pre>level_values = data[<span style="color: #800000;">'</span><span style="color: #800000;">难度</span><span style="color: #800000;">'</span><span style="color: #000000;">].values

difficulties </span>=<span style="color: #000000;"> {
    </span><span style="color: #800000;">'</span><span style="color: #800000;">简单</span><span style="color: #800000;">'</span><span style="color: #000000;">: 0,
    </span><span style="color: #800000;">'</span><span style="color: #800000;">中等</span><span style="color: #800000;">'</span><span style="color: #000000;">: 0,
    </span><span style="color: #800000;">'</span><span style="color: #800000;">困难</span><span style="color: #800000;">'</span><span style="color: #000000;">: 0
}

</span><span style="color: #0000ff;">for</span> value <span style="color: #0000ff;">in</span><span style="color: #000000;"> level_values:
    </span><span style="color: #0000ff;">if</span> value == <span style="color: #800000;">'</span><span style="color: #800000;">简单</span><span style="color: #800000;">'</span><span style="color: #000000;">:
        difficulties[</span><span style="color: #800000;">'</span><span style="color: #800000;">简单</span><span style="color: #800000;">'</span>] += 1
    <span style="color: #0000ff;">elif</span> value == <span style="color: #800000;">'</span><span style="color: #800000;">中等</span><span style="color: #800000;">'</span><span style="color: #000000;">:
        difficulties[</span><span style="color: #800000;">'</span><span style="color: #800000;">中等</span><span style="color: #800000;">'</span>] += 1
    <span style="color: #0000ff;">else</span><span style="color: #000000;">:
        difficulties[</span><span style="color: #800000;">'</span><span style="color: #800000;">困难</span><span style="color: #800000;">'</span>] += 1<span style="color: #000000;">

level </span>=<span style="color: #000000;"> pd.Series(difficulties)
</span><span style="color: #0000ff;">print</span><span style="color: #000000;">(level)

level.plot(kind </span>= <span style="color: #800000;">'</span><span style="color: #800000;">bar</span><span style="color: #800000;">'</span>, figsize=(6, 7<span style="color: #000000;">))
plt.grid(axis</span>=<span style="color: #800000;">'</span><span style="color: #800000;">y</span><span style="color: #800000;">'</span>)</pre>
</div>
<p><img src="https://img2018.cnblogs.com/blog/1458123/201902/1458123-20190214222307366-92150033.png" alt="" /></p>
<p>　　验证正确率与难度之间是否存在关系：</p>
<div class="cnblogs_code">
<pre><span style="color: #0000ff;">import</span><span style="color: #000000;"> numpy as np

relation </span>= data[[<span style="color: #800000;">'</span><span style="color: #800000;">难度</span><span style="color: #800000;">'</span>, <span style="color: #800000;">'</span><span style="color: #800000;">正确率</span><span style="color: #800000;">'</span><span style="color: #000000;">]]
rate_values </span>= relation[<span style="color: #800000;">'</span><span style="color: #800000;">正确率</span><span style="color: #800000;">'</span><span style="color: #000000;">].values

fig, axes </span>= plt.subplots(figsize=(15, 6<span style="color: #000000;">))
axes.scatter(rate_values, level_values)
plt.grid(axis</span>=<span style="color: #800000;">'</span><span style="color: #800000;">x</span><span style="color: #800000;">'</span><span style="color: #000000;">)
plt.xticks(np.arange(0, </span>1, 0.05<span style="color: #000000;">))
plt.xlabel(</span><span style="color: #800000;">'</span><span style="color: #800000;">正确率</span><span style="color: #800000;">'</span><span style="color: #000000;">)
plt.ylabel(</span><span style="color: #800000;">'</span><span style="color: #800000;">难度</span><span style="color: #800000;">'</span>)</pre>
</div>
<p><img src="https://img2018.cnblogs.com/blog/1458123/201902/1458123-20190214222454536-1770171007.png" alt="" /></p>
<p>　　根据图像显示，题目难度跟正确率存在一定关系，困难的题目正确率相对集中于8%-28%，中等难度的题目比较集中在23%-55%，简单难度的题目正确率主要在40%以上。</p>
<p>&nbsp;</p>
