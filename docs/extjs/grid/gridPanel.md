## 自动序号

```javascript
 columns: [new Ext.grid.RowNumberer(), {
                header: '序号',
                xtype: 'rownumberer',
                width: 60,
                align: 'center',
                sortable: false
            }]
```

## 表格换行

### grid单列自动换行

方式一: 

```javascript
                renderer : function(value, meta, record) {
					meta.style = 'overflow:auto;padding: 3px 6px;text-overflow: ellipsis;white-space: nowrap;white-space:normal;line-height:20px;';
					return value;
				}
```

方式二: 

```javascript
var renderAutoNewLine = function(v) {
		    return "<div style='white-space:normal;'>" + v + "</div>";
		    }
	
	renderer:renderAutoNewLine
```

方式三: 

```javascript
renderer : function(value, metaData, record, rowIndex, colIndex, store, view) {
                    metaData.style = 'white-space: normal;';
                    return value;
                }
	     metaData.style = 'white-space: normal; word-break: break-all;';//纯英文，数字不换行问题处理
```

### 表头自动换行

```javascript
listeners : {
				'afterrender' : function(grid) {
					var elments = Ext.select(".x-column-header-text");//.x-grid3-hd
					elments.each(function(el) {
						var id = el.dom.id;
						var column = document.getElementById(id);
						if (column) {
							column.style.whiteSpace = "normal";
							column.style.lineHeight = "15px"
						}
					}, this);
				}
			}
```

### grid全列自动换行

```html
	<style>
 		.x-grid-cell-inner {
		white-space: nowrap;
		white-space:normal;
		} 
	</style>
```

## 单元格合并

```javascript
    /**
     * 合并Grid的数据列
     * @param grid {Ext.Grid.Panel} 需要合并的Grid
     * @param colIndexArray {Array} 需要合并列的Index(序号)数组；从0开始计数，序号也包含。
     */
function _mergeGrid(grid, colIndexArray) {
        // 1.是否含有数据
        var gridView = document.getElementById(grid.getView().getId() + '-body');
        if (gridView == null) {
            return;
        }

        // 2.获取Grid的所有tr
        var trArray = [];
        if (grid.layout.type == 'table') { // 若是table部署方式，获取的tr方式如下
            trArray = gridView.childNodes;
        } else {
            trArray = gridView.getElementsByTagName('tr');
        }

        // 3逐个列合并：每个列在前面列合并的前提下可分别合并
        // 1)遍历列的序号数组
        for (var i = 0, colArrayLength = colIndexArray.length; i < colArrayLength; i++) {
            var colIndex = colIndexArray[i];
            var lastTr = trArray[0]; // 合并tr，默认为第一行数据
            // 2)遍历grid的tr，从第二个数据行开始
            for (var j = 1, trLength = trArray.length; j < trLength; j++) {
                var thisTr = trArray[j];
                // 3)2个tr的td内容一样
                if (lastTr.childNodes[colIndex].innerText == thisTr.childNodes[colIndex].innerText) {
                    // 4)若前面的td未合并，后面的td都不进行合并操作
                    if (i > 0 && thisTr.childNodes[colIndexArray[i - 1]].style.display != 'none') {
                        lastTr = thisTr;
                        continue;
                    } else {
                        // 5)符合条件合并td
                        if (lastTr.childNodes[colIndex].hasAttribute('rowspan')) {
                            var rowspan = lastTr.childNodes[colIndex].getAttribute('rowspan') - 0;
                            rowspan++;
                            lastTr.childNodes[colIndex].setAttribute('rowspan', rowspan);
                        } else {
                            lastTr.childNodes[colIndex].setAttribute('rowspan', '2');
                        }
                        lastTr.childNodes[colIndex].style['vertical-align'] = 'middle';
                        // 纵向居中
                        thisTr.childNodes[colIndex].style.display = 'none'; // 当前行隐藏
                    }
                } else {
                    // 5)2个tr的td内容不一样
                    lastTr = thisTr;
                }
            }
        }
    }
```

## 图片展示以及双击展示图片

```javascript
{
                xtype: 'actioncolumn',
                width: 280,
                dataIndex: 'child',
                text: '图片',
                align: 'center',
                renderer: function (value, metaData, record) {
                    var str = record.get('child').substring(record.get('child').length - 3, record.get('child').length);
                    if (str == 'jpg' || str == 'png') {
                        var id = metaData.record.id;
                        Ext.defer(function () {
                            Ext.create('Ext.Img', {
                                height: 140,
                                width: 250,
                                src: 'downloadRider.json?child=' + value + '&parent=' + record.get('parent') + '&random=' + Math.random(),
                                renderTo: id,
                                listeners: {
                                    scope: this,
                                    el: {
                                        dblclick: function (e, a) {
                                            var winViewImage = Ext.create('Ext.Window', {
                                                width: 750,
                                                height: 500,
                                                maximizable: true,//窗体最大化按钮
                                                title: '图片',
                                                layout: "fit", //窗口布局类型
                                                modal: true, //是否模态窗口，默认为false
                                                resizable: false,//调整窗体大小
                                                closeAction: 'hide', //关闭窗体实际上是隐藏窗体并未关闭销毁此窗体对象(节约资源)
                                                plain: true,//窗体主体部分背景颜色透明
                                                draggable: true,//充许拖动窗体
                                                border: false,
                                                items: [Ext.create('Ext.Img', {
                                                    width: 750,
                                                    height: 500,
                                                    src: 'downloadRider.json?child=' + record.get('child') + '&parent=' + record.get('parent')
                                                })]
                                            });
                                            winViewImage.show();
                                        }
                                    }
                                }

                            })
                        }, 50);

                        return Ext.String.format('<div id="{0}"></div>', id);
                    }
                }
            }
```

## 修改行背景色

```html
    <style type="text/css">
        tr.x-grid-record-pink .x-grid-td {
            background: pink !important;
        }
    </style>


	
            viewConfig: {
                getRowClass: function (record, rowIndex, rowParams, store) {
                    if (record.data.SUBMIT_STATUS_ == '1') {
                        return 'x-grid-record-pink';
                    }
                }
            },
```

## 翻页保留选中

```javascript
Ext.onReady(function () {
    var supplierStore = Ext.create("Ext.data.Store", {
        fields: [
            { name: "Name", type: "string" },
            { name: "Phone", type: "string" },
            { name: "Address", type: "string" }
        ],
        autoLoad: true,
        pageSize: 3,
        listeners: {
            load: function (me, records, success, opts) {
                if (!success || !records || records.length == 0)
                    return;

                //根据全局的选择，初始化选中的列
                var selModel = grid.getSelectionModel();
                Ext.Array.each(AllSelectedRecords, function () {
                    for (var i = 0; i < records.length; i++) {
                        var record = records[i];
                        if (record.get("Name") == this.get("Name"//选中record，并且保持现有的选择，不触发选中事件
                        }
                    }
                });
            }
        },
        proxy: {
            type: "ajax",
            url: rootUrl + "Grid/FetchPageData",
            actionMethods: { read: "POST" },
            reader: {
                type: "json",
                root: "data.records",
                totalProperty: "data.total"
            }
        }
    });

var AllSelectedRecords = [];

    var grid = Ext.create("Ext.grid.GridPanel", {
        border: true,
        width: 600,
        height: 200,
        store: supplierStore,
        columnLines: true,
        enableColumnHide: false,
        enableColumnMove: false,
        enableLocking: true,
        selModel: Ext.create("Ext.selection.CheckboxModel", {
            mode: "MULTI",
            listeners: {
                deselect: function (me, record, index, opts) {

                    AllSelectedRecords = Ext.Array.filter(AllSelectedRecords, function (item) {
                        return item.get("Name") != record.get("Name");
                    });
                },
                select: function (me, record, index, opts) {
                    AllSelectedRecords.push(record);
                }
            }
        }),
        columns: [
            { text: "名称", dataIndex: "Name", width: 150, sortable: false },
            { text: "电话", dataIndex: "Phone", width: 150, sortable: false },
            { text: "地址", dataIndex: "Address", width: 260, sortable: false }
        ],
        bbar: { xtype: "pagingtoolbar", store: supplierStore, displayInfo: true },
        renderTo: Ext.getBody()
    });
});
```

## 鼠标焦点显示全部内容

```javascript
Ext.QuickTips.init();
renderer: function (value, metaData, record, rowIndex, colIndex) {
                    metaData.tdAttr = 'qclass="x-tip" data-qwidth="200" data-qtip="'
                        + value + '"';
                    return value;
                }
```

## 显示总和平均数

```
Ext.onReady(function(){
		//创建表格数据
		var datas = [
			['张三',2500],
			['李四',1500]
		];
		//创建Grid表格组件
		Ext.create('Ext.grid.Panel',{
			title : 'Ext.grid.feature.Summary示例',
			renderTo: Ext.getBody(),
			width:300,
			height:150,
			frame:true,
			store: {
		        fields: ['name','salary','introduce'],
		        proxy: {
		            type: 'memory',
		            data : datas,
		            reader : 'array'//Ext.data.reader.Array解析器
		        },
		        autoLoad: true
		    },
		    features: [{
		    	ftype: 'summary'//Ext.grid.feature.Summary表格汇总特性
		    }],
			columns: [//配置表格列
				{header: "姓名", flex: 1, dataIndex: 'name', 
					summaryType: 'count',//求数量
					summaryRenderer: function(value){
						return '员工总数：'+value
					}
				},
				{header: "薪资", flex: 1, dataIndex: 'salary', 
					summaryType: 'average',//求平均值
					summaryRenderer: function(value){
						return '平均薪资：'+value
					}
				}
			]
		});
	});
```

## grid不让取消选中

```html
SIMPLE
1.
                'itemclick': function (view, record, item, index, e, eOpts) {
                    this.selModel.locked = false;
                    var rowStore = workTicketDetailPanel.getStore();
                    for (var i = 0, leng = rowStore.getCount(); i < leng; i++) {
                        if (rowStore.getAt(i).get("WORK_TICKET_NUM_") == record.data.WORK_TICKET_NUM_) {
                            workTicketDetailPanel.getSelectionModel().select(i, true);
                        } else {
                            workTicketDetailPanel.getSelectionModel().deselect(i);
                        }
                    }
                    this.selModel.locked = true;
                    _setButtonStatus(record.get('SUBMIT_STATUS_'));
                },

2.
'select': function (selModel, record, row) {
                    var rowStore = workTicketDetailPanel.getStore();
                    for (var i = 0, leng = rowStore.getCount(); i < leng; i++) {
                        if (rowStore.getAt(i).get("WORK_TICKET_NUM_") == record.data.WORK_TICKET_NUM_) {
                            workTicketDetailPanel.getSelectionModel().select(i, true);
                        } else {
                            workTicketDetailPanel.getSelectionModel().deselect(i);
                        }
                    }
                },
                'deselect': function () {
                    return false;
                },
```

## 切换单选多选
`Ext.getCmp('checkStepPanel').selModel.selectionMode = 'SINGLE';`

## 表格展示图片

```
        var riderPanel = Ext.create('Ext.grid.Panel', {
            id: 'riderPanel',
            store: riderStore,
            //title: '文件表单',
            columnLines: true,
            frame: true,
            selModel: {
                selType: 'checkboxmodel',
                mode: 'SINGLE'
            },
            columns: [{
                xtype: 'actioncolumn',
                width: 280,
                dataIndex: 'fileName',
                text: '图片',
                align: 'center',
                renderer: function (value, metaData, record) {
                    if (record.get('fileType') == '.jpg' || record.get('fileType') == '.png') {
                        var id = metaData.record.id;

                        Ext.defer(function () {
                            Ext.create('Ext.Img', {
                                height: 140,
                                width: 250,
                                src: 'downloadRider.json?fileName=' + value + '&bizCode=' + P_BILLCODE + '&random=' + Math.random(),
                                renderTo: id,
                                listeners: {
                                    scope: this,
                                    el: {
                                        dblclick: function (e, a) {
                                            var winViewImage = Ext.create('Ext.Window', {
                                                width: 750,
                                                height: 500,
                                                maximizable: true,//窗体最大化按钮
                                                title: '图片',
                                                layout: "fit", //窗口布局类型
                                                modal: true, //是否模态窗口，默认为false
                                                resizable: false,//调整窗体大小
                                                closeAction: 'hide', //关闭窗体实际上是隐藏窗体并未关闭销毁此窗体对象(节约资源)
                                                plain: true,//窗体主体部分背景颜色透明
                                                draggable: true,//充许拖动窗体
                                                border: false,
                                                items: [Ext.create('Ext.Img', {
                                                    width: 750,
                                                    height: 500,
                                                    src: 'downloadRider.json?fileName=' + record.get('fileName') + '&bizCode=' + P_BILLCODE
                                                })]
                                            });
                                            winViewImage.show();
                                        }
                                    }
                                }

                            })
                        }, 50);

                        return Ext.String.format('<div id="{0}"></div>', id);
                    }
                }
            }, {
                text: '文件名',
                dataIndex: 'fileName',
                style: 'text-align: center;',
                flex: 1
            }, {
                text: '操作',
                style: 'text-align: center;',
                width: 100,
                renderer: function (value, metaData, record, rowIndex, colIndex, store, view) {
                    return '<a href=javascript:_downloadRider()>下载</a>' + '&nbsp&nbsp&nbsp' + '<a href=javascript:_deleteRider()>删除</a>'
                }
            }],
            viewConfig: {
                emptyText: '<div style="text-align: center; padding-top: 50px; font: italic bold 20px Microsoft YaHei;">没有附件</div>',
                enableTextSelection: true
            },
            dockedItems: [{
                xtype: 'pagingtoolbar',
                store: riderStore,
                dock: 'bottom',
                displayInfo: true
            }]
        });
```