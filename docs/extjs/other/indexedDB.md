## 介绍
IndexedDB是为了能够在客户端存储大量的结构化数据，并且使用索引高效检索的API。

## LocalStorage 与 IndexedDB 区别与适用场景
LocalStorage 是用 key-value 键值模式存储数据，它存储的数据都是字符串形式。如果你想让 LocalStorage存储对象，你需要借助 JSON.stringify()能将对象变成字符串形式，再用 JSON.parse()将字符串还原成对象,就是专门为小数量数据设计的，所以它的 api 设计为同步的。

IndexedDB 很适合存储大量数据，它的 API 是异步调用的。IndexedDB 使用索引存储数据，各种数据库操作放在事务中执行。IndexedDB 甚至还支持简单的数据类型。IndexedDB 比 localstorage 强大得多，但它的 API 也相对复杂。对于简单的数据，你应该继续使用 localstorage，但当你希望存储大量数据时，IndexedDB 会明显的更适合，IndexedDB 能提供你更为复杂的查询数据的方式。

## 特性
* 对象仓库

有了数据库后我们自然希望创建一个表用来存储数据，但 indexedDB 中没有表的概念，而是 objectStore，
一个数据库中可以包含多个 objectStore，objectStore 是一个灵活的数据结构，可以存放多种类型数据。
也就是说一个 objectStore 相当于一张表，里面存储的每条数据和一个键相关联。
我们可以使用每条记录中的某个指定字段作为键值（keyPath），也可以使用自动生成的递增数字作为键值（keyGenerator），
也可以不指定。选择键的类型不同，objectStore 可以存储的数据结构也有差异。

* 事务性

在 indexedDB 中，每一个对数据库操作是在一个事务的上下文中执行的。事务范围一次影响一个或多个 object stores，
你通过传入一个 object store 名字的数组到创建事务范围的函数来定义。
例如：db.transaction(storeName, 'readwrite')，创建事务的第二个参数是事务模式。
当请求一个事务时,必须决定是按照只读还是读写模式请求访问。

* 基于请求

对 indexedDB 数据库的每次操作，描述为通过一个请求打开数据库,访问一个 object store，再继续。
IndexedDB API 天生是基于请求的,这也是 API 异步本性指示。对于你在数据库执行的每次操作,
你必须首先为这个操作创建一个请求。当请求完成,你可以响应由请求结果产生的事件和错误。

* 异步

在 IndexedDB 大部分操作并不是我们常用的调用方法，返回结果的模式，而是请求—响应的模式，
所谓异步 API 是指并不是这条指令执行完毕，我们就可以使用 request.result 来获取 indexedDB 对象了，
就像使用 ajax 一样，语句执行完并不代表已经获取到了对象，所以我们一般在其回调函数中处理。

除了result，IDBOpenDBRequest接口定义了几个重要属性

* onerror: 请求失败的回调函数句柄
* onsuccess:请求成功的回调函数句柄
* onupgradeneeded:请求数据库版本变化句柄

## 使用
### 创建数据库
调用indexedDB.open方法就可以创建或者打开一个indexedDB
```javascript
function openDB (name) {
            var request=window.indexedDB.open(name);
            request.onerror=function(e){
                console.log('OPen Error!');
            };
            request.onsuccess=function(e){
                myDB.db=e.target.result;
            };
        }

        var myDB={
            name:'test',
            version:1,
            db:null
        };
        openDB(myDB.name);
```
代码中定义了一个myDB对象，在创建indexedDB request的成功毁掉函数中，
把request获取的DB对象赋值给了myDB的db属性，这样就可以使用myDB.db来访问创建的indexedDB了。

onupgradeneeded。这个句柄在我们请求打开的数据库的版本号和已经存在的数据库版本号不一致的时候调用。

indexedDB.open()方法还有第二个可选参数，数据库版本号，数据库创建的时候默认版本号为1，
当我们传入的版本号和数据库当前版本号不一致的时候onupgradeneeded就会被调用，
当然我们不能试图打开比当前数据库版本低的version，否则调用的就是onerror了，修改一下刚才例子

```javascript
function openDB (name,version) {
            var version=version || 1;
            var request=window.indexedDB.open(name,version);
            request.onerror=function(e){
                console.log(e.currentTarget.error.message);
            };
            request.onsuccess=function(e){
                myDB.db=e.target.result;
            };
            request.onupgradeneeded=function(e){
                console.log('DB version changed to '+version);
            };
        }

        var myDB={
            name:'test',
            version:3,
            db:null
        };
        openDB(myDB.name,myDB.version);
```

由于刚才已经创建了版本为1的数据库，打开版本为3的时候，会在控制台输出：DB version changed to 3

### 关闭与删除数据库
关闭数据库可以直接调用数据库对象的close方法
```javascript
function closeDB(db){
            db.close();
        }
```

删除数据库使用indexedDB对象的deleteDatabase方法
```javascript
function deleteDB(name){
            indexedDB.deleteDatabase(name);
        }
```

简单调用
```javascript
var myDB={
            name:'test',
            version:3,
            db:null
        };
        openDB(myDB.name,myDB.version);
        setTimeout(function(){
            closeDB(myDB.db);
            deleteDB(myDB.name);
        },500);
```

由于异步API原因，不能保证能够在closeDB方法调用前获取db对象（实际上获取db对象也比执行一条语句慢得多），
所以用了setTimeout延迟了一下。当然我们注意到每个indexedDB实例都有onclose回调函数句柄，
用以数据库关闭的时候处理，有兴趣可以试试，原理很简单，不演示了。

### object store
有了数据库后我们自然希望创建一个表用来存储数据，但indexedDB中没有表的概念，而是objectStore，
一个数据库中可以包含多个objectStore，objectStore是一个灵活的数据结构，可以存放多种类型数据。
也就是说一个objectStore相当于一张表，里面存储的每条数据和一个键相关联。

我们可以使用每条记录中的某个指定字段作为键值（keyPath），也可以使用自动生成的递增数字作为键值（keyGenerator），
也可以不指定。选择键的类型不同，objectStore可以存储的数据结构也有差异

### 事务
在对新数据库做任何事情之前，需要开始一个事务。事务中需要指定该事务跨越哪些object store。

事务具有三种模式
1. 只读：read，不能修改数据库数据，可以并发执行
2. 读写：readwrite，可以进行读写操作
3. 版本变更：verionchange

```javascript
var transaction=db.transaction([students','taecher']);  //打开一个事务，使用students 和teacher object store
var objectStore=transaction.objectStore('students'); //获取students object store
```

### 给object store添加数据
调用数据库实例的createObjectStore方法可以创建object store，方法有两个参数：store name和键类型。
调用store的add方法添加数据。有了上面知识，我们可以向object store内添加数据了

#### keyPath

因为对新数据的操作都需要在transaction中进行，而transaction又要求指定object store，
所以我们只能在创建数据库的时候初始化object store以供后面使用，这正是onupgradeneeded的一个重要作用，
修改一下之前代码

```javascript
function openDB (name,version) {
            var version=version || 1;
            var request=window.indexedDB.open(name,version);
            request.onerror=function(e){
                console.log(e.currentTarget.error.message);
            };
            request.onsuccess=function(e){
                myDB.db=e.target.result;
            };
            request.onupgradeneeded=function(e){
                var db=e.target.result;
                if(!db.objectStoreNames.contains('students')){
                    db.createObjectStore('students',{keyPath:"id"});
                }
                console.log('DB version changed to '+version);
            };
        }
```

这样在创建数据库的时候我们就为其添加了一个名为students的object store，准备一些数据以供添加

```javascript
var students=[{ 
            id:1001, 
            name:"Byron", 
            age:24 
        },{ 
            id:1002, 
            name:"Frank", 
            age:30 
        },{ 
            id:1003, 
            name:"Aaron", 
            age:26 
        }];
```

```javascript
function addData(db,storeName){
            var transaction=db.transaction(storeName,'readwrite'); 
            var store=transaction.objectStore(storeName); 

            for(var i=0;i<students.length;i++){
                store.add(students[i]);
            }
        }


openDB(myDB.name,myDB.version);
        setTimeout(function(){
            addData(myDB.db,'students');
        },1000);
```

这样我们就在students object store里添加了三条记录，以id为键

#### keyGenerate
```javascript
function openDB (name,version) {
            var version=version || 1;
            var request=window.indexedDB.open(name,version);
            request.onerror=function(e){
                console.log(e.currentTarget.error.message);
            };
            request.onsuccess=function(e){
                myDB.db=e.target.result;
            };
            request.onupgradeneeded=function(e){
                var db=e.target.result;
                if(!db.objectStoreNames.contains('students')){
                    db.createObjectStore('students',{autoIncrement: true});
                }
                console.log('DB version changed to '+version);
            };
        }
```

再有就是都使用和都不使用key, 可以自行摸索

### 查找数据
可以调用object store的get方法通过键获取数据，以使用keyPath做键为例

```javascript
function getDataByKey(db,storeName,value){
            var transaction=db.transaction(storeName,'readwrite'); 
            var store=transaction.objectStore(storeName); 
            var request=store.get(value); 
            request.onsuccess=function(e){ 
                var student=e.target.result; 
                console.log(student.name); 
            };
}
```

### 更新数据
可以调用object store的put方法更新数据，会自动替换键值相同的记录，达到更新目的，没有相同的则添加，
以使用keyPath做键为例

```javascript
function updateDataByKey(db,storeName,value){
            var transaction=db.transaction(storeName,'readwrite'); 
            var store=transaction.objectStore(storeName); 
            var request=store.get(value); 
            request.onsuccess=function(e){ 
                var student=e.target.result; 
                student.age=35;
                store.put(student); 
            };
}
```

### 删除数据及object store
调用object store的delete方法根据键值删除记录
```javascript
function deleteDataByKey(db,storeName,value){
            var transaction=db.transaction(storeName,'readwrite'); 
            var store=transaction.objectStore(storeName); 
            store.delete(value); 
        }
```

调用object store的clear方法可以清空object store
```javascript
function clearObjectStore(db,storeName){
            var transaction=db.transaction(storeName,'readwrite'); 
            var store=transaction.objectStore(storeName); 
            store.clear();
}
```

调用数据库实例的deleteObjectStore方法可以删除一个object store，这个就得在onupgradeneeded里面调用了
```javascript
if(db.objectStoreNames.contains('students')){ 
                    db.deleteObjectStore('students'); 
}
```

## 索引
索引的一个好处就是可以迅速定位数据，提高搜索速度，在indexedDB中有两种索引，一种是自增长的int值，一种是keyPath：自己指定索引列，
我们重点来看看keyPath方式的索引使用.

### 创建索引
我们可以在创建object store的时候指明索引，使用object store的createIndex创建索引，方法有三个参数
* 索引名称
* 索引属性字段名
* 索引属性值是否唯一

```javascript
function openDB (name,version) {
            var version=version || 1;
            var request=window.indexedDB.open(name,version);
            request.onerror=function(e){
                console.log(e.currentTarget.error.message);
            };
            request.onsuccess=function(e){
                myDB.db=e.target.result;
            };
            request.onupgradeneeded=function(e){
                var db=e.target.result;
                if(!db.objectStoreNames.contains('students')){
                    var store=db.createObjectStore('students',{keyPath: 'id'});
                    store.createIndex('nameIndex','name',{unique:true}); 
                    store.createIndex('ageIndex','age',{unique:false}); 
                }
                console.log('DB version changed to '+version);
            };
        }
```

这样我们在students 上创建了两个索引

### 利用索引获取数据
```javascript
function getDataByIndex(db,storeName){
            var transaction=db.transaction(storeName);
            var store=transaction.objectStore(storeName);
            var index = store.index("nameIndex");
            index.get('Byron').onsuccess=function(e){
                var student=e.target.result;
                console.log(student.id);
            }
        }
```

这样我们可以利用索引快速获取数据，name的索引是唯一的没问题，但是对于age索引只会取到第一个匹配值，
要想得到所有age符合条件的值就需要使用游标了

### 游标
在indexedDB中使用索引和游标是分不开的，对数据库熟悉的话很好理解游标是什么，有了数据库object store的游标，
我们就可以利用游标遍历object store了。

使用object store的openCursor()方法打开游标
```javascript
function fetchStoreByCursor(db,storeName){
            var transaction=db.transaction(storeName);
            var store=transaction.objectStore(storeName);
            var request=store.openCursor();
            request.onsuccess=function(e){
                var cursor=e.target.result;
                if(cursor){
                    console.log(cursor.key);
                    var currentStudent=cursor.value;
                    console.log(currentStudent.name);
                    cursor.continue();
                }
            };
        }
```

curson.contine()会使游标下移，知道没有数据返回undefined

### index与游标结合
要想获取age为26的student，可以结合游标使用索引

```javascript
function getMultipleData(db,storeName){
            var transaction=db.transaction(storeName);
            var store=transaction.objectStore(storeName);
            var index = store.index("ageIndex");
            var request=index.openCursor(IDBKeyRange.only(26))
            request.onsuccess=function(e){
                var cursor=e.target.result;
                if(cursor){
                    var student=cursor.value;
                    console.log(student.id);
                    cursor.continue();
                }
            }
        }
```

这样我们可是使用索引打开一个游标，参数下面会讲到，在成功的句柄内获得游标便利age为26的student，也可以通过  
index.openKeyCursor()方法只获取每个对象的key值。

### 指定游标范围
```javascript
index.openCursor()/
index.openKeyCursor()方法在不传递参数的时候会获取object store所有记录，像上面例子一样我们可以对搜索进行筛选
```

可以使用key range 限制游标中值的范围，把它作为第一个参数传给 
```javascript
openCursor() 或是 openKeyCursor()
```

IDBKeyRange.only(value):只获取指定数据  
IDBKeyRange.lowerBound(value,isOpen)：获取最小是value的数据，第二个参数用来指示是否排除value值本身，也就是数学中的是否是开区间  
IDBKeyRange.upperBound(value,isOpen)：和上面类似，用于获取最大值是value的数据  
IDBKeyRange.bound(value1,value2,isOpen1,isOpen2)

获取名字首字母在B-E的student
```javascript
function getMultipleData(db,storeName){
            var transaction=db.transaction(storeName);
            var store=transaction.objectStore(storeName);
            var index = store.index("nameIndex");
            var request=index.openCursor(IDBKeyRange.bound('B','F',false,
true
));
            request.onsuccess=function(e){
                var cursor=e.target.result;
                if(cursor){
                    var student=cursor.value;
                    console.log(student.name);
                    cursor.continue();
                }
            }
        }
```

## 示例

<details>
  <summary>入门 demo</summary>
  
打开数据库实例
```javascript
var db; // 全局的indexedDB数据库实例。

//1\. 获取IDBFactory接口实例（文档地址： https://developer.mozilla.org/en-US/docs/Web/API/IDBFactory）
var indexedDB =
  window.indexedDB ||
  window.webkitIndexedDB ||
  window.mozIndexedDB ||
  window.msIndexedDB;

if (!indexedDB) {
  console.log('你的浏览器不支持IndexedDB');
}

// 2\. 通过IDBFactory接口的open方法打开一个indexedDB的数据库实例
// 第一个参数： 数据库的名字，第二个参数：数据库的版本。返回值是一个：IDBRequest实例,此实例有onerror和onsuccess事件。
var IDBOpenDBRequest = indexedDB.open('demoDB', 1);

// 3\. 对打开数据库的事件进行处理

// 打开数据库成功后，自动调用onsuccess事件回调。
IDBOpenDBRequest.onsuccess = function(e) {};

// 打开数据库失败
IDBOpenDBRequest.onerror = function(e) {
  console.log(e.currentTarget.error.message);
};

// 第一次打开成功后或者版本有变化自动执行以下事件：一般用于初始化数据库。
IDBOpenDBRequest.onupgradeneeded = function(e) {
  db = e.target.result; // 获取到 demoDB对应的 IDBDatabase实例,也就是我们的数据库。

  if (!db.objectStoreNames.contains(personStore)) {
    //如果表格不存在，创建一个新的表格（keyPath，主键 ； autoIncrement,是否自增），会返回一个对象（objectStore）
    // objectStore就相当于数据库中的一张表。IDBObjectStore类型。
    var objectStore = db.createObjectStore(personStore, {
      keyPath: 'id',
      autoIncrement: true
    });

    //指定可以被索引的字段，unique字段是否唯一。类型： IDBIndex
    objectStore.createIndex('name', 'name', {
      unique: true
    });
    objectStore.createIndex('phone', 'phone', {
      unique: false
    });
  }
  console.log('数据库版本更改为： ' + dbVersion);
};
```

数据库的 objectStore 添加  
indexedDB 的增删改查的操作需要放到一个事务中进行（推荐）
```javascript
// 创建一个事务，类型：IDBTransaction，文档地址： https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction
var transaction = db.transaction(personStore, 'readwrite');

// 通过事务来获取IDBObjectStore
var store = transaction.objectStore(personStore);

// 往store表中添加数据
var addPersonRequest = store.add({
  name: '老马',
  phone: '189111833',
  address: 'aicoder.com'
});

// 监听添加成功事件
addPersonRequest.onsuccess = function(e) {
  console.log(e.target.result); // 打印添加成功数据的 主键（id）
};

// 监听失败事件
addPersonRequest.onerror = function(e) {
  console.log(e.target.error);
};
```

数据库的 objectStore 修改
```javascript
// 创建一个事务，类型：IDBTransaction，文档地址： https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction
var transaction = db.transaction(personStore, 'readwrite');

// 通过事务来获取IDBObjectStore
var store = transaction.objectStore(personStore);
var person = {
  id: 6,
  name: 'lama',
  phone: '515154084',
  address: 'aicoder.com'
};

// 修改或者添加数据。 第一参数是要修改的数据，第二个参数是主键（可省略)
var updatePersonRequest = store.get(6);

// 监听添加成功事件
updatePersonRequest.onsuccess = function(e) {
  // var p = e.target.result;  // 要修改的原对象
  store.put(person);
};

// 监听失败事件
updatePersonRequest.onerror = function(e) {
  console.log(e.target.error);
};
```

数据库的 objectStore 删除
```javascript
// 创建一个事务，类型：IDBTransaction，文档地址： https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction
var transaction = db.transaction(personStore, 'readwrite');

// 通过事务来获取IDBObjectStore
var store = transaction.objectStore(personStore);
store.delete(6).onsuccess = function(e) {
  console.log(删除成功！)
};
```

根据 id 获取数据
```javascript
// 创建一个事务，类型：IDBTransaction，文档地址： https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction
var transaction = db.transaction(personStore, 'readwrite');

// 通过事务来获取IDBObjectStore
var store = transaction.objectStore(personStore);
store.get(6).onsuccess = function(e) {
  console.log(删除成功！)
};
```

数据库的 objectStore 游标查询
```javascript
var trans = db.transaction(personStore, 'readwrite');
var store = trans.objectStore(personStore);
var cursorRequest = store.openCursor();
cursorRequest.onsuccess = function(e) {
  var cursor = e.target.result;
  if (cursor) {
    var html = template('tbTmpl', cursor.value);
    document.getElementById('tbd').innerHTML += html;
    cursor.continue(); // 游标继续往下 搜索，重复触发 onsuccess方法，如果到最后返回null
  }
};
```
  
</details>

<details>
  <summary>完整示例1</summary>
  
```javascript
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Document</title>
  <script src="./lib/art_template.js"></script>
</head>
<body>
  <table>
    <tr>
      <td>
        <label for="name">用户名</label>
      </td>
      <td>
        <input type="text" name="name" id="name">
      </td>
    </tr>
    <tr>
      <td>
        <label for="phone">电话</label>
      </td>
      <td>
        <input type="text" name="phone" id="phone">
      </td>
    </tr>
    <tr>
      <td>
        <label for="address">地址</label>
      </td>
      <td>
        <input type="text" name="address" id="address">
      </td>
    </tr>
  </table>
  <input type="button" value="添加用户" id="btnAdd" onclick="addPerson()">
  <table>
    <thead>
      <tr>
        <th>id</th>
        <th>name</th>
        <th>address</th>
        <th>phone</th>
        <th>编辑</th>
      </tr>
    </thead>
    <tbody id="tbd">
    </tbody>
  </table>
  <script id="tbTmpl" type="text/html">
    <tr>
      <td>{{id}}</td>
      <td>{{name}}</td>
      <td>{{phone}}</td>
      <td>{{address}}</td>
      <td><a href="#">修改</a>
      <a href="#" onclick="delById({{id}})">删除</a></td>
    </tr>
  </script>
  <script>
    var db, dbName = 'demoDb', dbVersion = 1, personStore = 'person';
    // 创建indexedDB对象，兼容各种浏览器
    var indexedDB = window.indexedDB || window.webkitIndexedDB || window.mozIndexedDB || window.msIndexedDB;
    if (!indexedDB) {
      console.log("你的浏览器不支持IndexedDB");
    }

    openIndexedDB(loadTableData);

    // 配合游标遍历表中数据，并配合art-template生成html
    function loadTableData() {
      document.getElementById('tbd').innerHTML = "";
      var trans = db.transaction(personStore, 'readwrite');
      var store = trans.objectStore(personStore);
      var cursorRequest = store.openCursor();
      cursorRequest.onsuccess = function (e) {
        var cursor = e.target.result;
        if (cursor) {
          var html = template('tbTmpl', cursor.value);
          document.getElementById('tbd').innerHTML += html;
          cursor.continue(); // 游标继续往下 搜索，重复触发 onsuccess方法，如果到到返回null
        }
      }
    }

    function delById(id) {
      if (!db || !id) {
        return;
      }
      // 创建一个事务
      var transaction = db.transaction(personStore, 'readwrite');

      // 通过事务来获取store
      var store = transaction.objectStore(personStore);

      // 删除请求
      var delPersonRequest = store.delete(id);
      delPersonRequest.onsuccess = function (e) {
        loadTableData(); // 删除成功后，重新加载数据
      }
      delPersonRequest.onerror = function (e) {
        console.log(e.target.error);
      }
    }

    // 添加用户
    function addPerson() {
      if (!db) {
        return;
      }
      var pName = document.getElementById('name').value;
      var pPhone = document.getElementById('phone').value;
      var pAddress = document.getElementById('address').value;
      // 创建一个事务
      var transaction = db.transaction(personStore, 'readwrite');

      // 通过事务来获取store
      var store = transaction.objectStore(personStore);

      var addPersonRequest = store.add({ name: pName, phone: pPhone, address: pAddress });
      addPersonRequest.onsuccess = function (e) {
        console.log(e.target);
        loadTableData(); // 添加成功后重新加载数据
      }
      addPersonRequest.onerror = function (e) {
        console.log(e.target.error);
      }
    }

    // 打开数据库
    function openIndexedDB(callback) {
      // 打开一个数据库
      var request = indexedDB.open(dbName, dbVersion);

      // 打开失败
      request.onerror = function (e) {
        console.log(e.currentTarget.error.message);
      };

      // 打开成功！
      request.onsuccess = function (e) {
        db = e.target.result;
        console.log('成功打开DB');
        callback();
      };

      // 打开成功后，如果版本有变化自动执行以下事件
      request.onupgradeneeded = function (e) {
        var db = e.target.result;
        if (!db.objectStoreNames.contains(personStore)) {
          console.log("我需要创建一个新的存储对象");
          //如果表格不存在，创建一个新的表格（keyPath，主键 ； autoIncrement,是否自增），会返回一个对象（objectStore）
          var objectStore = db.createObjectStore(personStore, {
            keyPath: "id",
            autoIncrement: true
          });

          //指定可以被索引的字段，unique字段是否唯一, 指定索引可以加快搜索效率。
          objectStore.createIndex("name", "name", {
            unique: true
          });
          objectStore.createIndex("phone", "phone", {
            unique: false
          });
        }
        console.log('数据库版本更改为： ' + dbVersion);
      };
    }
  </script>
</body>
</html>
```

</details>

<details>
  <summary>完整示例2</summary>

```html
<!DOCTYPE HTML>
<html>
<head>
    <title>IndexedDB</title>
</head>
<body>
    <script type="text/javascript">
        function openDB (name,version) {
            var version=version || 1;
            var request=window.indexedDB.open(name,version);
            request.onerror=function(e){
                console.log(e.currentTarget.error.message);
            };
            request.onsuccess=function(e){
                myDB.db=e.target.result;
            };
            request.onupgradeneeded=function(e){
                var db=e.target.result;
                if(!db.objectStoreNames.contains('students')){
                    var store=db.createObjectStore('students',{keyPath: 'id'});
                    store.createIndex('nameIndex','name',{unique:true});
                    store.createIndex('ageIndex','age',{unique:false});
                }
                console.log('DB version changed to '+version);
            };
        }

        function closeDB(db){
            db.close();
        }

        function deleteDB(name){
            indexedDB.deleteDatabase(name);
        }

        function addData(db,storeName){
            var transaction=db.transaction(storeName,'readwrite');
            var store=transaction.objectStore(storeName);

            for(var i=0;i<students.length;i++){
                store.add(students[i]);
            }
        }

        function getDataByKey(db,storeName,value){
            var transaction=db.transaction(storeName,'readwrite');
            var store=transaction.objectStore(storeName);
            var request=store.get(value);
            request.onsuccess=function(e){
                var student=e.target.result;
                console.log(student.name);
            };
        }

        function updateDataByKey(db,storeName,value){
            var transaction=db.transaction(storeName,'readwrite');
            var store=transaction.objectStore(storeName);
            var request=store.get(value);
            request.onsuccess=function(e){
                var student=e.target.result;
                student.age=35;
                store.put(student);
            };
        }

        function deleteDataByKey(db,storeName,value){
            var transaction=db.transaction(storeName,'readwrite');
            var store=transaction.objectStore(storeName);
            store.delete(value);
        }

        function clearObjectStore(db,storeName){
            var transaction=db.transaction(storeName,'readwrite');
            var store=transaction.objectStore(storeName);
            store.clear();
        }

        function deleteObjectStore(db,storeName){
            var transaction=db.transaction(storeName,'versionchange');
            db.deleteObjectStore(storeName);
        }

        function fetchStoreByCursor(db,storeName){
            var transaction=db.transaction(storeName);
            var store=transaction.objectStore(storeName);
            var request=store.openCursor();
            request.onsuccess=function(e){
                var cursor=e.target.result;
                if(cursor){
                    console.log(cursor.key);
                    var currentStudent=cursor.value;
                    console.log(currentStudent.name);
                    cursor.continue();
                }
            };
        }

        function getDataByIndex(db,storeName){
            var transaction=db.transaction(storeName);
            var store=transaction.objectStore(storeName);
            var index = store.index("ageIndex");
            index.get(26).onsuccess=function(e){
                var student=e.target.result;
                console.log(student.id);
            }
        }

        function getMultipleData(db,storeName){
            var transaction=db.transaction(storeName);
            var store=transaction.objectStore(storeName);
            var index = store.index("nameIndex");
            var request=index.openCursor(null,IDBCursor.prev);
            request.onsuccess=function(e){
                var cursor=e.target.result;
                if(cursor){
                    var student=cursor.value;
                    console.log(student.name);
                    cursor.continue();
                }
            }
        }

        var myDB={
            name:'test',
            version:1,
            db:null
        };

        var students=[{
            id:1001,
            name:"Byron",
            age:24
        },{
            id:1002,
            name:"Frank",
            age:30
        },{
            id:1003,
            name:"Aaron",
            age:26
        },{
            id:1004,
            name:"Casper",
            age:26
        }];
    </script>
</body>
</html>
```

</details>
