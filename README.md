# 全国失信人名单-百度公开数据

使用方法：下载`baidu_api.py`并import。

```python
import baidu_api as api

# 根据姓名查询
df_liming = api.get(name="李明")

# 根据地区查询
df_beijing = api.get(name="李明", area="北京")

# 根据身份证号查询
df_card = api.get(name="李明", card_id="1321271976****0013")
```

## 示例

请参考test_notebook。
