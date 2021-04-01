## 创建数据模型

```javascript
		Ext.regModel('PostInfo', {
		    fields: [{name: 'province'},{name: 'post'}]
		});
```

## 定义数据源

```javascript
		//定义组合框中显示的数据源
		var postStore = Ext.create('Ext.data.Store',{
			model : 'PostInfo',
			data : [
				{province:'北京',post:'100000'},
				{province:'通县',post:'101100'},
				{province:'昌平',post:'102200'},
				{province:'大兴',post:'102600'},
				{province:'密云',post:'101500'},
				{province:'延庆',post:'102100'},
				{province:'顺义',post:'101300'},
				{province:'怀柔',post:'101400'}
			]
		});
//注册store
Ext.data.StoreManager.register(postStore);
```