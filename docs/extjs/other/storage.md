## 定义和使用
localstorage 在浏览器的 API 有两个：localStorage 和sessionStorage，存在于 window 对象中，在浏览器中存储 key/value 对的数据  
localStorage 对应 window.localStorage，  
sessionStorage 对应 window.sessionStorage。

localStorage 和 sessionStorage 的区别主要是在于其生存期。  
localStorage只要在相同的协议、相同的主机名、相同的端口下，就能读取/修改到同一份localStorage数据。  
sessionStorage比localStorage更严苛一点，除了协议、主机名、端口外，还要求在同一窗口（也就是浏览器的标签页）下。

## 生存期
localStorage理论上来说是永久有效的，即不主动清空的话就不会消失，即使保存的数据超出了浏览器所规定的大小，也不会把旧数据清空而只会报错。但需要注意的是，在移动设备上的浏览器或各Native App用到的WebView里，localStorage都是不可靠的，可能会因为各种原因（比如说退出App、网络切换、内存不足等原因）被清空。  
sessionStorage的生存期顾名思义，类似于session，只要关闭浏览器（也包括浏览器的标签页），就会被清空。由于sessionStorage的生存期太短，因此应用场景很有限，但从另一方面来看，不容易出现异常情况，比较可靠。

## 数据结构
localstorage为标准的键值对（Key-Value,简称KV）数据类型，简单但也易扩展，只要以某种编码方式把想要存储进localstorage的对象给转化成字符串，就能轻松支持。举点例子：把对象转换成json字符串，就能让存储对象了；把图片转换成DataUrl（base64），就可以存储图片了。另外对于键值对数据类型来说，"键是唯一的"这个特性也是相当重要的，重复以同一个键来赋值的话，会覆盖上次的值。

## 过期时间
localstorage原生是不支持设置过期时间的，想要设置的话，就只能自己来封装一层逻辑来实现：

```javascript
function set(key,value){
  var curtime = new Date().getTime();//获取当前时间
  localStorage.setItem(key,JSON.stringify({val:value,time:curtime}));//转换成json字符串序列
}
function get(key,exp)//exp是设置的过期时间
{
  var val = localStorage.getItem(key);//获取存储的元素
  var dataobj = JSON.parse(val);//解析出json对象
  if(new Date().getTime() - dataobj.time > exp)//如果当前时间-减去存储的元素在创建时候设置的时间 > 过期时间
  {
    console.log("expires");//提示过期
  }
  else{
    console.log("val="+dataobj.val);
  }
}
```

## 容量限制
目前业界基本上统一为5M，已经比cookies的4K要大很多了

## 域名限制
由于浏览器的安全策略，localstorage是无法跨域的，也无法让子域名继承父域名的localstorage数据，这点跟cookies的差别还是蛮大的。

## 异常处理
localstorage在目前的浏览器环境来说，还不是完全稳定的，可能会出现各种各样的bug，一定要考虑好异常处理。
我个人认为localstorage只是资源本地化的一种优化手段，不能因为使用localstorage就降低了程序的可用性，
那种只是在console里输出点错误信息的异常处理我是绝对反对的。localstorage的异常处理一般用try/catch来捕获/处理异常。

## 注意事项
1. localStorage特定于页面的协议，不是同一域名，不能访问。
2. 有长度限制，5M左右，不同浏览器大小会有不同。
3. 生命周期是永久的，但是数据实际是存在浏览器的文件夹下，可能卸载浏览器就会删除。
4. 浏览器可以设置是否可以访问数据，如果设置不允许会访问失败。
5. 兼容IE8以上浏览器
6. 只能存储字符串类型，需要转成字符串存储。

## 使用技巧
1.先判断浏览器是否支持localStorage，通过if(!window.localStorage) return;
2.单词太长，不方便书写，可以利用 var storage=window.localStorage;
3.字符串和原始类型需要通过JSON.stringfy转字符串，通过JSON.parse转成对象
4.通过封装方法实现来回转化

## 使用方法
1.存值共有3种方式，localStorage相当于window对象下面的一个属性，所以有[]和.调用，但也具有自身的setItem方法
```javascript
// 自身方法
localStorage.setItem("name","bonly");
// []方法
localStorage["name"]="bonly";
// .方法
localStorage.name="bonly";
```

2.取值也是如此，自身的方法是getItem
```javascript
// 自身方法
localStorage.getItem("name");
// []方法
localStorage["name"];
// .方法
localStorage.name;
```

3.改变的方式，就是相当于给对应的key重新赋值，就会把原来的值覆盖掉
```javascript
// 自身方法
localStorage.setItem("name","TOM");
// []方法
localStorage["name"]="TOM";
// .方法
localStorage.name="TOM";
```

4.移除某一个值，可以通过对象删除属性的关键字delete也可以用自身的方法removeItem
```javascript
// 自身方法
localStorage.removeItem("name");
// []方法
delete localStorage["name"];
// .方法
delete localStorage.name
```

5.获取所有的key
```javascript
// 通过自身的key
for (var i=0;i<localStorage.length;i++) {
	console.log(localStorage.key(i));
}
```

```javascript
// 通过for in 循环获取
for(var key in localStorage){
	console.log(key);
}
```

6.获取所有的值
```javascript
localStorage.valueOf();取出所有的值
```

7.清除所有的值
```javascript
localStorage.clear()
```

8.判断是否具有某个key，hasOwnProperty方法
```javascript
localStorage.hasOwnProperty("name")
// 如果存在的话返回true，不存在返回false
```