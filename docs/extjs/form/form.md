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

## 多文件跨域上传

有两种方式
1. 使用jqury 将文件数据保存到FormData中上传
2. 修改Ext.form.action.Action.CONNECT_FAILURE异常处理，捕捉到异常后视作成功重新查询

```javascript
function _insertRider() {
        var fileEl = Ext.getCmp('multipartFiles').fileInputEl.dom;
        var fd = new FormData();
        for (var i = 0; i < fileEl.files.length; i++) {
            fd.append("multipartFiles", fileEl.files[i]);
        }
        fd.append("V_PERCODE", Ext.util.Cookies.get('V_PERCODE'));
        fd.append("V_GUID", V_GUID);

        var msg = new Ext.window.MessageBox();
        msg.wait('上传文件中...');
        $.ajax({
            url: gatewayUrl + '/budget/insertRiderList',
            type: 'POST',
            cache: false,
            data: fd,
            processData: false,
            contentType: false,
            dataType: "json",
            beforeSend: function () {
                uploading = true;
            },
            success: function (data) {
                _selectRider();
                Toast.alert('信息', '上传成功', 2000);
                Ext.getCmp('formPanel').getForm().reset();
            },
            error: function (data) {
                Ext.Msg.alert('Fail', 'Upload File failed.');
            },
            complete: function () {
                msg.close();
            }
        });
        // Ext.getCmp('formPanel').getForm().submit({
        //     url: gatewayUrl + '/budget/insertRiderList',
        //     submitEmptyText: false,
        //     waitMsg: '上传中',
        //     success: function (form, action) {
        //         var data = action.result;
        //         // if (data.message === SUCCESS) {
        //         if (data.success === true) {
        //             _selectRider();
        //             Toast.alert('信息', '上传成功', 2000);
        //         } else {
        //             Ext.MessageBox.alert('错误', data.message, Ext.MessageBox.ERROR);
        //         }
        //     },
        //     failure: function (form, action) {
        //         switch (action.failureType) {
        //             case Ext.form.action.Action.CLIENT_INVALID:
        //                 Ext.MessageBox.alert('提醒', "请选择附件");
        //                 break;
        //             case Ext.form.action.Action.SERVER_INVALID:
        //                 Ext.MessageBox.alert('错误', action.result.message, Ext.MessageBox.ERROR);
        //                 break;
        //             case Ext.form.action.Action.CONNECT_FAILURE:
        //                 _selectRider();
        //                 Toast.alert('信息', '上传成功', 2000);
        //             // Ext.MessageBox.alert('错误', Ext.MessageBox.ERROR);
        //         }
        //     }
        // });
    }
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

## 必填项前加红色标识

1、重写allowBlank属性

```javascript
Ext.override(Ext.form.field.Base, {
    initComponent: function () {
        if (this.allowBlank !== undefined && !this.allowBlank) {
            if (this.fieldLabel) {
                this.fieldLabel = '<font color=red>*</font>' + this.fieldLabel;
            }
        }
        this.callParent(arguments);
    }
});
```

2、beforeLabelTextTpl属性

```markdown
var required = '<span style="color:red;font-weight:bold" data-qtip="Required">*</span>';
                {xtype: 'textfield',
                id: 'moduleName',
                beforeLabelTextTpl: required,
                fieldLabel: '模块名称'}
```