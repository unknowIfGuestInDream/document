## 多文件上传

```javascript
var formPanel = Ext.create('Ext.form.Panel', {
			id : 'formPanel',
			layout : 'column',
			frame : true,
			autoScroll : true,
			defaults : {
				labelAlign : 'right',
				labelWidth : 100,
				inputWidth : 140,
				margin : '4,0,0,0'
			},
			items : [{
				xtype : 'filefield',
				id : 'RIDER_',
				name : 'RIDER_',
				fieldLabel : '<spring:message code="RIDER.RIDER_" />',
				buttonText : '<spring:message code="pleaseChoose" />',
				inputWidth : 300,
				allowBlank : false,
				multipleFn: function($this){
				         var typeArray = ["application/x-shockwave-flash","audio/MP3","image/*","flv-application/octet-stream"];
				         var fileDom = $this.getEl().down('input[type=file]');
				         fileDom.dom.setAttribute("multiple","multiple");
				         fileDom.dom.setAttribute("accept",typeArray.join(","));
				},
				listeners: {
					afterrender: function(){
						this.multipleFn(this);
						},
					change: function(){
							var fileDom = this.getEl().down('input[type=file]'); 
							var files = fileDom.dom.files; 
							var str = ''; 
							for(var i = 0;  i < files.length;  i++){
							 str += files[i].name;
							 str += ' ';
							} 
							 Ext.getCmp('RIDER_').setRawValue(str);

							 this.multipleFn(this);
							}	
				}
			}]
		});
```

## 生成uuid

```javascript
Ext.data.IdGenerator.get('uuid').generate().replace(/-/g, "")
```

## 自定义电话号码的vtype验证

```javascript
		//自定义电话号码的vtype验证
		Ext.apply(Ext.form.field.VTypes, {
		    phone:  function(v) {
		    	//规则区号（3-4位数字）-电话号码（7-8位数字）
		        return /^(\d{3}-|\d{4}-)?(\d{8}|\d{7})$/.test(v);
		    },
		    phoneText: '请输入有效的电话号码',
		    phoneMask: /[\d-]/i//只允许输入数字和-号
		});

		Ext.QuickTips.init();

        {
				fieldLabel:'住宅号码',
				vtype:'phone'//使用电话类型验证
			}
```

## 自定义日期范围验证示例

```javascript
//自定义VType类型，验证日期选择范围
		Ext.apply(Ext.form.field.VTypes, {
			//验证方法
			dateRange : function(val, field) {
				var beginDate = null,//开始日期
					beginDateCmp = null,//开始日期组件
					endDate = null,//结束日期
					endDateCmp = null,//结束日期组件
					validStatus = true;//验证状态
				if(field.dateRange){
					//获取开始时间
					if(!Ext.isEmpty(field.dateRange.begin)){
						beginDateCmp = Ext.getCmp(field.dateRange.begin);
						beginDate = beginDateCmp.getValue();
					}
					//获取结束时间
					if(!Ext.isEmpty(field.dateRange.end)){
						endDateCmp = Ext.getCmp(field.dateRange.end);
						endDate = endDateCmp.getValue();
					}
				}
				//如果开始日期或结束日期有一个为空则校验通过
				if(!Ext.isEmpty(beginDate) && !Ext.isEmpty(endDate)){
					validStatus =  beginDate <= endDate;
				}
				
				return validStatus;
			},
			//验证提示信息
			dateRangeText : '开始日期不能大于结束日期，请重新选择。'
		});

		Ext.QuickTips.init();//初始化提示;

            {
				id:'beginDate1',
				fieldLabel:'开始日期',
				dateRange:{begin:'beginDate1',end:'endDate1'},//用于vtype类型dateRange
				vtype:'dateRange'
			},{
				id:'endDate1',
				fieldLabel:'结束日期',
				dateRange:{begin:'beginDate1',end:'endDate1'},//用于vtype类型dateRange
				vtype:'dateRange'
			}
```