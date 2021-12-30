## 基本面数据

### 基差

> 代码

`BASIS`

> 描述

基差是某一特定商品于某一特定的时间和地点的现货价格与期货价格之差。它的计算方法是现货价格减去期货价格。若现货价格低于期货价格，基差为负值；现货价格高于期货价格，基差为正值。

> 格式

```
{
    "日期": "2016-01-11",
    "螺纹钢": 29,
    "菜籽粕": 54
}
```

### 企业景气及企业家信心指数

> 代码

`BCEEI`

> 描述

企业家信心指数也称"宏观经济景气指数"，是根据企业家对企业外部市场经济环境与宏观政策的认识、看法、判断与预期而编制的指数，用以综合反映企业家对宏观经济环境的感受与信心。

> 格式

```
{
    "季度": "2005第1季度",
    "企业家信心指数": {
        "指数": 135.9,
        "同比": 0.3585,
        "环比": 0.0504
    },
    "企业景气指数": {
        "指数": 132.5,
        "同比": 0.3246,
        "环比": -0.0227
    }
}
```

### 交易结算资金(银证转账)

> 代码

`BTSF`

> 描述

银证转账是指将股民在银行开立的个人结算存款账户与证券公司的资金账户建立对应关系，通过银行的电话银行、网上银行、网点自助设备和证券公司的电话、网上交易系统及证券公司营业部的自助设备将资金在银行和证券公司之间划转。

> 格式

```
{
    "日期": "2014年06月20日",
    "上证指数收盘": 2026.67,
    "上证指数涨跌幅": -0.0213,
    "交易结算资金日均余额(亿)": 5783,
    "交易结算资金期末余额(亿)": 7265,
    "银证转账减少额(亿)": 1686,
    "银证转账变动净额(亿)": 1801,
    "银证转账增加额(亿)": 3487
}
```

### 存款准备金率

> 代码

`CKZBJ`

> 描述

存款准备金是指金融机构为保证客户提取存款和资金清算需要而准备的，是缴存在中央银行的存款，中央银行要求的存款准备金占其存款总额的比例就是存款准备金率。

> 格式

```
{
    "日期": "2007年01月15日",
    "中小金融机构": {
        "调整前": 0.09,
        "调整后": 0.095,
        "调整幅度": 0.005
    },
    "大型金融机构": {
        "调整前": 0.09,
        "调整后": 0.095,
        "调整幅度": 0.005
    },
    "消息公布次日指数涨跌": {
        "上证": 0.0249,
        "深证": 0.0245
    }
}
```

### 居民消费价格指数

> 代码

`CPI`

> 描述

居民消费价格指数是反映与居民生活有关的产品及劳务价格统计出来的物价变动指标，以百分比变化为表达形式。它是衡量通货膨胀的主要指标之一。一般定义超过 3％为通货膨胀，超过 5％就是比较严重的通货膨胀。

> 格式

```
{
    "月份": "2008年01月份",
    "全国": 107.1,
    "农村": 107.7,
    "城市": 106.8
}
```

### 财政收入

> 代码

`CZSR`

> 描述

财政收入是指政府为履行其职能、实施公共政策和提供公共物品与服务需要而筹集的一切资金的总和。它是衡量一国政府财力的重要指标，政府在社会经济活动中提供公共物品和服务的范围和数量，在很大程度上决定于财政收入的充裕状况。

> 格式

```
{
    "月份": "2008年01月份",
    "当月(亿美元)": 7396.64,
    "当月同比增长": 0.4235,
    "环比增长": 1.352,
    "累计(亿美元)": 7396.64,
    "累计同比增长": 0.424
}
```

### 外商直接投资数据

> 代码

`FDI`

> 描述

外商直接投资指外国企业和经济组织或个人(包括华侨、港澳台胞以及我国在境外注册的企业)按我国有关政策、法规，用现汇、实物、技术等在我国境内开办外商独资企业、与我国境内的企业或经济组织共同举办中外合资经营企业、合作经营企业或合作开发资源的投资(包括外商投资收益的再投资)，以及经政府有关部门批准的项目投资总额内企业从境外借入的资金。

> 格式

```
{
    "月份": "2008年01月份", 
    "当月(亿美元)": 112, 
    "当月同比增长": 1.1642, 
    "环比增长": -0.1446, 
    "累计(亿美元)": 114.38, 
    "累计同比增长": 1.0523
}
```

### 外汇和黄金储备

> 代码

`FEGR`

> 描述

外汇又称为外汇存底，是指一国政府所持有的国际储备资产中的外汇部分，即一国政府保有的以外币表示的债权。是一个国家货币当局持有并可以随时兑换外国货币的资产。黄金储备：指一国货币当局持有的，用以平衡国际收支，维持或影响汇率水平，作为金融资产持有的黄金。

> 格式

```
{
    "月份": "2008年01月份",
    "国家外汇储备(亿美元)": {
        "金额": 15898.1,
        "同比增长": 0.4391,
        "环比增长": 0.0403
    },
    "黄金储备(万盎司)": {
        "金额": 1929,
        "同比增长": 0,
        "环比增长": 0
    }
}
```

### 国内生产总值

> 代码

`GDP`

> 描述

国内生产总值，Gross Domestic Product，简称 GDP，是指在一定时期内(一个季度或一年)，一个国家或地区的经济中所生产出的全部最终产品和劳务的价值，常被公认为衡量国家经济状况的最佳指标。

> 格式

```
{
    "季度": "2020年第1季度", 
    "国内生产总值(亿元)": 206504, 
    "第一产业(亿元)": 10186, 
    "第二产业(亿元)": 73638, 
    "第三产业(亿元)": 122680
}
```

### 全国股票交易统计表

> 代码

`GPJYTJ`

> 描述

股票账户统计详细数据(旧版2008年至今)

> 格式

```
{
    "日期": "2008年01月",
    "A股最低综合股价指数": {
        "上海": 4330.7,
        "深圳": 1424.35
    },
    "A股最高综合股价指数": {
        "上海": 5522.78,
        "深圳": 1667.91
    },
    "发行总股本": {
        "上海": 14198.16,
        "深圳": 2818.71
    },
    "市价总值": {
        "上海": 225354.97,
        "深圳": 52499.85
    },
    "成交量": {
        "上海": 1771.83,
        "深圳": 874.06
    },
    "成交金额": {
        "上海": 30759.73,
        "深圳": 15770.72
    }
}
```

### 股票账户统计详细数据

> 代码

`GPZHSJ`

> 描述

股票账户统计详细数据(新版2015年至今)

> 格式

```
{
    "日期": "2015年04月",
    "上证指数": {
        "收盘": 4441.655,
        "涨跌幅": 18.51053083
    },
    "新增投资者": {
        "数量(万户)": 497.53,
        "同比增长": 0,
        "环比增长": 0
    },
    "期末投资者(万户)": {
        "总量": 8184.79,
        "同比增长": 8108.3,
        "环比增长": 235.92
    },
    "沪深总市值(亿)": 563491.335037778,
    "沪深户均市值(万)": 69.4956
}
```

### 工业增加值增长

> 代码

`GYZJZ`

> 描述

工业增加值增长是指工业企业在报告期内以货币形式表现的工业生产活动的最终成果，是指工业企业在一定时期内工业生产活动创造的价值，是国内生产总值的组成部分。公式： 工业增加值=固定资产折旧+劳动者报酬+生产税净值+营业盈余。

> 格式

```
{
    "月份": "2008年02月份",
    "同比增长": 15.4,
    "累计增长": 15.4
}
```

### 货币供应量

> 代码

`HBGYL`

> 描述

货币供应量亦称货币存量、货币供应，指某一时点流通中的现金量和存款量之和。货币供应量是各国中央银行编制和公布的主要经济统计指标之一。它由包括中央银行在内的金融机构供应的存款货币和现金货币两部分构成。世界各国中央银行货币估计口径不完全一致，但划分的基本依据是一致的，即流动性大小。

> 格式

```
{
    "月份": "2008年01月份",
    "流通中的现金(M0)": {
        "数量(亿元)": 36673.15,
        "同比增长": 0.3121,
        "环比增长": 0.209
    },
    "货币和准货币(M2)": {
        "数量(亿元)": 417846.17,
        "同比增长": 0.1888,
        "环比增长": 0.0358
    },
    "货币(M1)": {
        "数量(亿元)": 154872.59,
        "同比增长": 0.2054,
        "环比增长": 0.0154
    }
}
```

### 海关进出口增减情况一览表

> 代码

`HGJCK`

> 描述

海关进出口增减指实际进出我国国境的货物总金额。进出口总额用以观察一个国家在对外贸易方面的总规模。我国规定出口货物按离岸价格统计，进口货物按到岸价格统计。

> 格式

```
{
    "月份": "2008年01月份",
    "当月出口额": {
        "金额(亿美元)": 1096.4,
        "同比增长": 0.266,
        "环比增长": -0.0417
    },
    "当月进口额": {
        "金额(亿美元)": 901.74,
        "同比增长": 0.276,
        "环比增长": -0.0169
    },
    "累计出口额": {
        "金额(亿美元)": 1096.4,
        "同比增长": 0.266
    },
    "累计进口额": {
        "金额(亿美元)": 901.74,
        "同比增长": 0.276
    }
}
```

### 消费者信心指数

> 代码

`ICS`

> 描述

消费者信心指数是反映消费者信心强弱的指标，是综合反映并量化消费者对当前经济形势评价和对经济前景、收入水平、收入预期以及消费心理状态的主观感受，是预测经济走势和消费趋向的一个先行指标，是监测经济周期变化不可缺少的依据。

> 格式

```
{
    "月份": "2007年01月份",
    "消费者信心指数": {
        "指数值": 112.4,
        "同比增长": 0.019,
        "环比增长": -0.0062
    },
    "消费者满意指数": {
        "指数值": 109.5,
        "同比增长": -0.0054,
        "环比增长": -0.0073
    },
    "消费者预期指数": {
        "指数值": 114.2,
        "同比增长": 0.0344,
        "环比增长": -0.0061
    }
}
```

### 贷款市场报价利率

> 代码

`LRP`

> 描述

贷款市场报价利率是由具有代表性的报价行，根据本行对最优质客户的贷款利率，以公开市场操作利率加点形成的方式报价，由中国人民银行授权全国银行间同业拆借中心计算并公布的基础性的贷款参考利率，各金融机构应主要参考 LPR 进行贷款定价。

> 格式

```
{
    "日期": "2015-08-31",
    "LPR_1Y利率(%)": 4.55,
    "LPR_5Y利率(%)": 0,
    "中长期贷款利率:5年以上(%)": 5.15,
    "短期贷款利率:6个月至1年(含)(%)": 4.6
}
```

### 新房价指数

> 代码

`NREPI`

> 描述

房屋销售价格指数是反映一定时期房屋销售价格变动程度和趋势的相对数，它通过百分数的形式来反映房价在不同时期的涨跌幅度。包括商品房、公有房屋和私有房屋各大类房屋的销售价格的变动情况。

> 格式

```
{
    "日期": "2011年01月01日",
    "上海": {
        "二手住宅价格指数": {
            "环比": 100.5,
            "同比": 101.7,
            "定基": 100.6
        },
        "新建住宅价格指数": {
            "环比": 100.9,
            "同比": 101.5,
            "定基": 100.8
        },
        "新建商品住宅价格指数": {
            "环比": 101.1,
            "同比": 101.8,
            "定基": 101
        }
    },
    "北京": {
        "二手住宅价格指数": {
            "环比": 100.3,
            "同比": 102.6,
            "定基": 101.2
        },
        "新建住宅价格指数": {
            "环比": 100.8,
            "同比": 106.8,
            "定基": 102.4
        },
        "新建商品住宅价格指数": {
            "环比": 101,
            "同比": 109.1,
            "定基": 103
        }
    }
}
```

### 汽柴油价格

> 代码

`OILPRICE`

> 描述

汽柴油历史价格信息

> 格式

```
{
    "日期": "2000-6-6",
    "柴油(元/吨)": 2430,
    "汽油(元/吨)": 2935
}
```

### 旧房价指数

> 代码

`OREPI`

> 描述

08年~10年房地产价格指数

> 格式

```
{
    "月份": "2008年02月份",
    "国房景气指数": {
        "指数值": 105.55,
        "同比增长": 0.037
    },
    "土地开发面积指数": {
        "指数值": 99.34,
        "同比增长": 0.0671
    },
    "销售价格指数": {
        "指数值": 111.52,
        "同比增长": 0.0656
    }
}
```

### 采购经理人指数

> 代码

`PMI`

> 描述

采购经理人指数是统计制造业在生产、新订单、商品价格、存货、雇员、订单交货、新出口订单和进口等八个方面状况。具有其高度的时效性，是经济先行指标中一项非常重要的附属指标。

> 格式

```
{
    "月份": "2008年01月份",
    "制造业同比增长": -0.0381,
    "制造业指数": 53,
    "非制造业同比增长": -0.0033,
    "非制造业指数": 60.2
}
```

### 工业品出厂价格指数

> 代码

`PPI`

> 描述

工业品出厂价格指数是衡量工业企业产品出厂价格变动趋势和变动程度的指数，是反映全部工业产品出厂价格总水平的变动趋势和程度的相对数，也是制定有关经济政策和国民经济核算的重要依据。

> 格式

```
{
    "月份": "2006年01月份",
    "当月": 103.1,
    "当月同比增长": 0.0305,
    "累计": 103.05
}
```

### 全国税收收入

> 代码

`QGSSSR`

> 描述

税收是指国家为了向社会提供公共产品、满足社会共同需要、按照法律的规定，参与社会产品的分配、强制、无偿取得财政收入的一种规范形式。税收是一种非常重要的政策工具。

> 格式

```
{
    "季度": "2020年第1季度", 
    "税收收入合计(亿元)": 39029
}
```

### 企业商品价格指数

> 代码

`QYSPJG`

> 描述

CGPI 的前身是国内批发物价指数(Wholesale Price Index，简称 WPI)，指数编制始于 1994 年 1 月。是反映国内企业之间物质商品集中交易价格变动的统计指标，是比较全面的测度通货膨胀水平和反映经济波动的综合价格指数。CGPI 调查是经国家统计局批准、由中国人民银行建立并组织实施的一项调查统计制度。

> 格式

```
{
    "月份": "2005年01月份", 
    "农产品": {
        "同比增长": -0.0386, 
        "指数值": 106.22, 
        "环比增长": -0.0002
    }, 
    "总指数": {
        "同比增长": -0.0196, 
        "指数值": 104.67, 
        "环比增长": -0.0063
    }, 
    "煤油电": {
        "同比增长": 0.089, 
        "指数值": 115.83, 
        "环比增长": -0.0181
    }, 
    "矿产品": {
        "同比增长": 0.0623, 
        "指数值": 115.83, 
        "环比增长": 0.0117
    }
}
```

### 现货价格

> 代码

`SPOTPRICE`

> 描述

现货价格是指商品在现货交易中的成交价格。现货交易是一经成交立即交换的买卖行为，一般是买主即时付款，但也可以采取分期付款和延期交付的方式。由于付款方式的不同，同一现货在同一时期往往可能出现不同的价格。

> 格式

```
{
    "日期": "2017-08-30", 
    "棉花": 15895.4, 
    "棕榈油": 5715, 
    "油菜籽": 5210, 
    "焦炭": 2043.33
}
```

### 社会消费品零售总额

> 代码

`TRSCG`

> 描述

社会消费品零售总额是指批发和零售业、住宿和餐饮业以及其他行业直接售给城乡居民和社会集团的消费品零售额。

> 格式

```
{
    "月份": "2008年01月份",
    "同比增长": 0.212,
    "当月(亿元)": 9077.3,
    "环比增长": 0.0069,
    "累计(亿元)": 9077.3,
    "累计同比增长": 0.212
}
```

### 城镇固定资产投资

> 代码

`UIFA`

> 描述

固定资产投资是建造和购置固定资产的经济活动，即固定资产再生产活动。固定资产再生产过程包括固定资产更新(局部和全部更新)、改建、扩建、新建等活动。新的企业财务会计制度规定：固定资产局部更新的大修理作为日常生产活动的一部分，发生的大修理费用直接在成本中列支。

> 格式

```
{
    "月份": "2008年02月份", 
    "同比增长": 0, 
    "当月(亿元)": 0, 
    "环比增长": 0, 
    "自年初累计(亿元)": 8121
}
```

### 期货标准仓单

> 代码

`WHR`

> 描述

期货标准仓单是由期货交易所指定交割仓库按照交易所规定的程序签发的符合合约规定质量的实物提货凭证。由于期货标准仓单可以作为一种流通工具，因此它可以用作借款的质押品或用于期货合约的交割。

> 格式

```
{
    "日期": "2017-08-31", 
    "一号棉": {
        "仓库数量": 161, 
        "总仓单": 1245, 
        "平均仓单": 7
    }, 
    "动力煤": {
        "仓库数量": 0, 
        "总仓单": 0, 
        "平均仓单": 0
    }, 
    "天然橡胶": {
        "仓库数量": 21, 
        "总仓单": 358160, 
        "平均仓单": 17055
    }, 
    "普麦": {
        "仓库数量": 0, 
        "总仓单": 0, 
        "平均仓单": 0
    }, 
    "燃料油": {
        "仓库数量": 8, 
        "总仓单": 0, 
        "平均仓单": 0
    }, 
    "玉米淀粉": {
        "仓库数量": 1, 
        "总仓单": 500, 
        "平均仓单": 500
    }, 
    "聚氯乙烯": {
        "仓库数量": 1, 
        "总仓单": 920, 
        "平均仓单": 920
    }
}
```

### 本外币存款

> 代码

`WBCK`

> 描述

人民币是本位币，其他国家货币的都是外币。本外币存款就是人民币与外币的存款总和。它反映一个城市对资金的吸附能力，是1653衡量金融机构发展的重要指标。

> 格式

```
{
    "月份": "2008年02月份", 
    "同比增长": 1.5267, 
    "当月(亿元)": 13370.18, 
    "环比增长": -0.9668, 
    "累计(亿元)": 415859.25
}
```

### 外汇贷款数据

> 代码

`WHXD`

> 描述

外汇贷款是银行以外币为计算单位向企业发放的贷款。外汇贷款有广义和狭义之分，狭义的外汇贷款，仅指我国银行运用从境内企业、个人吸收的外汇资金，贷放于境内企业的贷款；广义的外汇贷款，还包括国际融资转贷款，即包括我国从国外借人，通过国内外汇指定银行转贷于境内企业的贷款。

> 格式

```
{
    "月份": "2008年02月份", 
    "同比增长": 7.5475, 
    "当月(亿元)": 217.02, 
    "环比增长": -0.9083, 
    "累计(亿元)": 2584.33
}
```


### 新增信贷数据

> 代码

`XZXD`

> 描述

借款企业第一次向这家银行贷款叫新增贷款。假如贷款到期了，企业正常偿还了这笔贷款后，再次向银行申请贷款，这样还叫新增贷款。假如贷款到期了，企业不能正常偿还这笔贷款，先银行提出再借第二笔贷款用以偿还第一笔贷款就叫借新还旧。

> 格式

```
{
    "月份": "2008年01月份", 
    "当月(亿元)": 8058, 
    "当月同比增长": 0.4229, 
    "环比增长": 15.6144, 
    "累计(亿元)": 8058, 
    "累计同比增长": 0.4229
}
```


### 银行利率调整

> 代码

`YHLL`

> 描述

表示一定时期内利息量与本金的比率，通常用百分比表示，按年计算则称为年利率。

其计算公式是：利息率= 利息量 ÷ 本金 ÷ 时间 ×100%

> 格式

```
{
    "生效时间": "2006-04-28", 
    "存款基准利率": {
        "调整前": 0.025, 
        "调整后": 0.0225, 
        "调整幅度": -0.0025
    }, 
    "消息公布次日指数涨跌": {
        "上证": 0.0166, 
        "深证": 0.0016
    }, 
    "贷款基准利率": {
        "调整前": 0.0556, 
        "调整后": 0.0585, 
        "调整幅度": 0.0029
    }
}
```


### 交易所会员成交量及持仓明细

> 代码

`DTP`

> 描述

当期货合约持仓量达到规定条件时，交易所将公布该月份合约前20名期货公司会员的成交量、买持仓量和卖持仓量，以及该合约所属期货品种期货公司会员、非期货公司会员的总成交量、总买持仓量和总卖持仓量。

> 格式

```
{
    "日期": "2020-05-28", 
    "cu2006": {
        "五矿经易": {
            "成交量": 10763, 
            "成交量增减": 2440, 
            "持卖单量": 5935, 
            "持卖单量增减": 29, 
            "持买单量": 1823, 
            "持买单量增减": -1326
        }, 
        "金瑞期货": {
            "持买单量": 15581, 
            "持买单量增减": -1529, 
            "持卖单量": 4827, 
            "持卖单量增减": -980, 
            "成交量": 5265, 
            "成交量增减": 664
        }
    }
}
```


### 交易所会员持仓盈亏

> 代码

`FCPP`

> 描述

根据交易所公布的持买单量、持卖单量、结算价、开盘价等，分别计算出交易所会员每个合约的盈亏状态。

> 格式

```
{
    "日期": "2020-05-28", 
    "cu2006": {
        "五矿经易": {
            "持买单盈亏": 729200, 
            "持卖单盈亏": -2374000, 
            "净持仓盈亏": -1644800
        }, 
        "金瑞期货": {
            "持买单盈亏": 6232400, 
            "持卖单盈亏": -1930800, 
            "净持仓盈亏": 4301600
        }
    }
}
```


### 中信期货研究报告

> 代码

`RECH`

> 描述

中信期货提供金融期货、宏观研究、黑色建材、有色金属、能源、化工、策略研究、农产品、量化研究等最新期货分析数据报告。

> 格式

```
{
    'date': '2021-08-19',
    'title': '【中信期货黑色】交易需求走弱，钢价震荡下行——日报20210819',
    'url': 'https://www.citicsf.com/e-futures/content/0001010101/762853'
}
```


### 全球经济数据

> 代码

`GLAL`

> 描述

全球经济数据汇总，全球主要国家和地区的宏观经济数据。

> 格式

```
{
    'date': '2021-09-06',
    '美国': {
        'GDP(十亿美元)': 20937,
        'GDP同比': 0.122,
        'GDP环比': 0.066,
        '利率': 0.0025,
        '通胀率': 0.054,
        '失业率': 0.052,
        '政府预算': -0.149,
        '负债/GDP': 1.076,
        '经常账户余额/GDP': -3.1,
        '人口(百万人)': 329.48,
        '人均GDP(美元)': 63546
    },
    '中国': {
        'GDP(十亿美元)': 14723,
        'GDP同比': 0.079,
        'GDP环比': 0.013,
        '利率': 0.0385,
        '通胀率': 0.01,
        '失业率': 0.0509,
        '政府预算': -0.037,
        '负债/GDP': 0.668,
        '经常账户余额/GDP': 1.9,
        '人口(百万人)': 1443.5,
        '人均GDP(美元)': 10200
    },
}
```


### 同花顺期货快讯

> 代码

`ALTS`

> 描述

提供专业、全面、准确的7X24小时期货资讯及期货行情报价服务，内容覆盖国内、国际主要市场期货品种，帮助投资者把握期货市场投资先机。

> 格式

```
{
    'date': '2021年09月06日 09:10',
    'title': '【大商所焦煤期货主力合约大涨4%】',
    'url': 'http://goodsfu.10jqka.com.cn/20210906/c632467955.shtml',
    'content': '大商所焦煤期货主力合约上涨4.03%，报2722.5元/吨。'
}
```


### 商品指数

> 代码

`INDEX`

> 描述

中证商品期货综合性指数系列包括1条综合指数、4条主要类别综合指数（农产品、金属、化工材料、能源）和4条细分类别综合指数（粮食、油脂、工业金属、纺织），以多维度反映国内商品期货市场表现。

> 格式

```
{
    'date': '2021-09-03',
    'index_name': '原油CFI',
    'index_code': '931337',
    'yesterday_close': '741.50',
    'today_close': '755.48'
}
```
