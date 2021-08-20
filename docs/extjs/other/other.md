## 提示框悬浮提示

```
Ext.QuickTips.init();
```

```html
<a href="javascript:void(0);" qclass="x-tip" data-qtip="提示信息" style="color: red">文本</a>
```

## Ext数组操作

```
Ext.onReady(function(){  
    var array = ['1','2','3','4','1','6','7'];  
    Ext.Array.clean(array);  //['1','2','3','4','6','7'];  
    Ext.Array.clone(array); // 克隆数组  
    Ext.Array.contains(array,'1');  //返回true 检查数组内是否包含指定元素  
    var array2 = ['1','2','3','4','5','6'];  
    Ext.Array.difference(array,array2); //返回 存在于 array中而不存在array2中的元素 ['','7']   
    Ext.Array.every(array,function(str,index,array){ //遍历数组  第二个参数执行回调函数 (当前元素,当前索引,当前数组(array)) 指定作用域 返回false 立即返回  
        //alert(str);  
        return true;  
    });  
    Ext.Array.filter(array,function(str,index,array){ //遍历数组  第二个参数执行回调函数 (当前元素,当前索引,当前数组(array)) 指定作用域  返回值： 返回true的元素组成新数组  
        //alert(str);  
        return true;  
    });  
    var array3 = ['1','2','3','4',['1','2','3'],'6','7'];  
    Ext.Array.flatten(array3);  //返回值：将多维数组 平铺成一维数组  
    Ext.Array.forEach(array,function(str,index,array){ //单纯的遍历数组    
        //alert(str);  
    });  
    Ext.Array.from(array,true);  //转换给定值为数组 如果为undefined 或 null 则返回空数组 本身为数组返回数组 可迭代返回数组拷贝 单值返回值包含该值的数组  
    Ext.Array.include(array,'100');  //向array末尾插入100 前提是array中不存在为100的值  
    Ext.Array.indexOf(array,'100',0);  //在数组内寻找指定值  第三个参数为起始位置 返回值：所在位置  
    alert(Ext.Array.intersect([array,array2])); //合并多个数组 数组元素唯一  
    Ext.Array.map(array,function(str,index,array){ //根据返回值组成数组  
        return str;  
    });  
    Ext.Array.max(array,function(s1,s2){ //返回数组中最大值 使用比较函数时返回值为负数时 小 0为相等  正数为大  
        return 0;  
    });  
       
    Ext.Array.mean([1,2,3,4,5]); //返回平均值  
    Ext.Array.min(array,function(s1,s2){ //返回数组中最小值 可使用比较函数  
        return 0;  
    });  
    var array4 = [{'a1':'a1'},{'a1':'a2'},{'a3':'a3'}];  
    Ext.Array.pluck(array4,'a1');   //在数组json数据中查找键为a1的值返回数组 （不改变数组大小）  
    Ext.Array.remove(array,'1'); //删除数组中指定元素 注意：只删除一项  
    Ext.Array.some(array,function(s1,s2){  //遍历数组 返回true立即返回  
        return false;  
    });  
    var array5=['s','a','z','c'];  
    Ext.Array.sort(array5); //排序数组 默认以字符排序 可选排序函数  
    var array6=[1,2,3,4,5];  
    Ext.Array.sum(array6);   //求和  
    Ext.Array.toArray(array6,2,4); //转换任何可迭代的值为数组 参数 1 iterable 2 start 3 end  
    Ext.Array.merge(array,array6); //组合数组  
    Ext.Array.unique(array,array6); //组合数组 merge的别名  
    Ext.Array.unique(array); //获取具有唯一元素的新数组  
      
})
```

## Ext生成uuid

```
Ext.data.IdGenerator.get('uuid').generate().replace(/-/g, "")
```

## 数字格式化

```
                renderer: function (value, metaData, record, rowIndex, colIndex, store, view) {
                    return Ext.util.Format.number(value, '0.00');
                }
```

## 数字千分位格式化

```
Ext.util.Format.number(21000000,Ext.util.Format.thousandSeparator)
```

extjs的千分位格式化不会保留小数，如需保留小数采用如下方法

```javascript
function moneyformat(num) {
    return (num.toFixed(2) + '').replace(/(\d{1,3})(?=(\d{3})+(?:$|\.))/g, '$1,');
}
```

## 数组去重

```javascript
function unique(arr) {
        var array = [];
        var ids = [];
        for (var i = 0; i < arr.length; i++) {
            if (ids.indexOf(arr[i].data.I_ID) === -1) {
                ids.push(arr[i].data.I_ID);
                array.push(arr[i]);
            }
        }
        return array;
    }
```

## 消息框

```javascript
//消息框
Toast = function () {
    var toastContainer;

    function createMessageBar(title, msg) {
        return '<div class="x-message-box" style="text-align: center; color: #666;"><div class="x-box-tl"><div class="x-box-tr"><div class="x-box-tc"></div></div></div><div class="x-box-ml"><div class="x-box-mr"><div class="x-box-mc" style="font: bold 15px Microsoft YaHei;">' + title + ' : ' + msg + '</div></div></div><div class="x-box-bl"><div class="x-box-br"><div class="x-box-bc"></div></div></div></div>';
    }

    return {
        alert: function (title, msg, delay) {
            if (!toastContainer) {
                toastContainer = Ext.DomHelper.insertFirst(document.body, {
                    id: 'toastContainer',
                    style: 'position: absolute; left: 0; right: 0; margin: auto; width: 360px; z-index: 20000; background: #87CEFA; '
                }, true);
            }

            var message = Ext.DomHelper.append(toastContainer, createMessageBar(title, msg), true);
            message.hide();
            message.slideIn('t').ghost("t", {
                delay: delay,
                remove: true
            });
        }
    };
}();
```

使用 `Toast.alert('信息', '新增成功', 2000);`

## 下载

1、js写法
```javascript
document.location.href = '/download'
```

2、extjs写法
```javascript
    function _downloadCode(procedureNameList) {
        var params = {
            'moduleName': Ext.getCmp('moduleName').getValue()
        };

        var body = Ext.getBody();
        var form = body.createChild({
            tag: 'form',
            cls: 'x-hidden',
            action: "/gen/downloadCode",
            method: "get",
            target: '_blank'
        });

        for (var key in params) {
            if (!Ext.isArray(params[key])) {
                form.createChild({
                    tag: 'input',
                    type: 'text',
                    cls: 'x-hidden',
                    name: key,
                    value: params[key]
                });
            } else {
                for (var i = 0; i < params[key].length; i++) {
                    form.createChild({
                        tag: 'input',
                        type: 'text',
                        cls: 'x-hidden',
                        name: key,
                        value: params[key][i]
                    });
                }
            }
        }

        form.dom.submit();
    }
```

## 打印
<details>
  <summary>展开</summary>
  
```javascript
//打印
    function _printWorkTicketDetail(preview) {//打印
        Ext.Ajax.request({
            url: '/er/printWorkTicketDetail',
            async: false,
            params: {
                'FTY_CODE_': Ext.getCmp('FTY_CODE_').getValue(),
                'START_DATE_': Ext.getCmp('START_DATE_').getSubmitValue(),
                'END_DATE_': Ext.getCmp('END_DATE_').getSubmitValue(),
                'DEPT_CODE_': Ext.isEmpty(Ext.getCmp('DEPT_CODE_').getValue()) ? '' : Ext.getCmp('DEPT_CODE_').getValue(),
                'GROUP_CODE_': Ext.isEmpty(Ext.getCmp('GROUP_CODE_').getValue()) ? '' : Ext.getCmp('GROUP_CODE_').getValue()
            },
            callback: function (options, success, response) {
                if (success) {
                    var data = Ext.decode(response.responseText);
                    if (data.success) {
                        //html文本
                        workOrderDetailExcel = data.workOrderDetailExcel;
                    }
                }
            }
        });

        var printContent = workOrderDetailExcel;//获得需要打印内容的HTML代码
        _pageSetupNull();//把页眉页脚设置为空
        printWindow = window.open('', '_blank');
        //这里是向新建的窗口写入HTML的head信息，可引入自己的js和css
        printWindow.document.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> <title></title><style type="text/css">@page{size:landscape;margin: 20mm 10mm 0mm 20mm;}</style></head><body>');
        //这里向新建的窗体中写入BODY的内容，注意，外边加的额外DIV是有必要的，它里面CSS可以控制打印时不会出现空白页
        printWindow.document.write('<div style="width:100%; height:100%; font-size:10px">' + printContent + "</div>");
        printWindow.document.write("</body></html>");//这里向新建的窗体写入HTML的结束标记

        //printWindow.document.getElementById("mytable").rows[0].cells[0].style.fontSize = "24px";

        printWindow.document.close();//关闭新建窗口的文档输出流，否则下面的打印语句无效
        printWindow.print();//打印当前新建窗口中的内容
        printWindow.close();//关闭新建的窗口
        _pageSetupDefault();//把页眉页脚恢复为默认
    }

    //设置网页打印的页眉页脚为空
    function _pageSetupNull() {
        var HKEY_Root, HKEY_Path, HKEY_Key;
        HKEY_Root = "HKEY_CURRENT_USER";
        HKEY_Path = "\\Software\\Microsoft\\Internet Explorer\\PageSetup\\";
        try {
            var Wsh = new ActiveXObject("WScript.Shell");
            HKEY_Key = "header";
            Wsh.RegWrite(HKEY_Root + HKEY_Path + HKEY_Key, "");
            HKEY_Key = "footer";
            Wsh.RegWrite(HKEY_Root + HKEY_Path + HKEY_Key, "");
        } catch (e) {
        }

    }

    //设置网页打印的页眉页脚为默认值
    function _pageSetupDefault() {
        var HKEY_Root, HKEY_Path, HKEY_Key;
        HKEY_Root = "HKEY_CURRENT_USER";
        HKEY_Path = "\\Software\\Microsoft\\Internet Explorer\\PageSetup\\";
        try {
            var Wsh = new ActiveXObject("WScript.Shell");
            HKEY_Key = "header";
            Wsh.RegWrite(HKEY_Root + HKEY_Path + HKEY_Key, "&w&b页码，&p/&P");
            HKEY_Key = "footer";
            Wsh.RegWrite(HKEY_Root + HKEY_Path + HKEY_Key, "&u&b&d");
        } catch (e) {
        }
    }
```  
  
</details>