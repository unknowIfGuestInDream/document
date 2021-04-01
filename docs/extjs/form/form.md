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