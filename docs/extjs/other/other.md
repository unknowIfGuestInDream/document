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