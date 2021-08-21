##简介
Web SQL 数据库 API 并不是 HTML5 规范的一部分，但是它是一个独立的规范，引入了一组使用 SQL 操作客户端数据库的 APIs。  
Web SQL 数据库可以在最新版的 Safari, Chrome 和 Opera 浏览器中工作

## 主要方法
1、openDatabase：这个方法使用现有数据库或创建新数据库创建数据库对象。
2、transaction：这个方法允许我们根据情况控制事务提交或回滚。
3、executeSql：这个方法用于执行真实的SQL查询。

## 打开数据库
openDatabasek中五个参数分别为：数据库名、版本号、描述、数据库大小、创建回调。  
创建回调没有也可以创建数据库。

```javascript
var dataBase = window.openDatabase('websql', '1.0', 'Datura练习', 4*1024*1024,function() {});
//                                     var db = openDatabase('mydb', '1.0', 'Test DB', 2 * 1024 * 1024);
```

## 建表
用到transaction方法用以处理事务，当一条语句执行失败的时候，整个事务回滚。方法有三个参数
a). 包含事务内容的一个方法;
b). 执行成功回调函数（可选）;
c). 执行失败回调函数（可选）;

```javascript
var tableName = 'websqlTable';//创建表的名称
//这里定一个变量来存建表相关信息，并声明主键，需要存储的字段及格式（NAME、AGE、HEIGHT、WEIGHT）
var creatTableSQL = 'CREATE TABLE IF  NOT EXISTS '+ tableName + ' (rowid INTEGER PRIMARY KEY AUTOINCREMENT, NAME text,AGE text,HEIGHT text,WEIGTH text)';
    dataBase.transaction(function (ctx,result) {
        ctx.executeSql(creatTableSQL,[],function(ctx,result){
            alert("表创建成功 " + tableName);//建表成功
        },function(tx, error){
            alert('创建表失败:' + tableName + error.message);//建表失败
        });
    });
```

## 向指定表中插入数据
同样用到transaction方法用以处理事务。

```javascript
function websqlInsterDataToTable(tableName,NAME,AGE,HEIGHT,WEIGTH){
    var insterTableSQL = 'INSERT INTO ' + tableName + ' (NAME,AGE,HEIGHT,WEIGTH) VALUES (?,?,?,?)';
    dataBase.transaction(function (ctx) {
        ctx.executeSql(insterTableSQL,[NAME,AGE,HEIGHT,WEIGTH],function (ctx,result){
                console.log("插入" + tableName  + NAME + "成功");
            },
            function (tx, error) {
                alert('插入失败: ' + error.message);
            });
    });
}
            websqlInsterDataToTable(websqlTable,"小红","18","175cm","40kg");                 
            websqlInsterDataToTable(websqlTable,"小黄","17","180cm","45kg");             
            websqlInsterDataToTable(websqlTable,"小蓝","19","185cm","70kg");
            websqlInsterDataToTable(websqlTable,"小绿","19","175cm","60kg");
            websqlInsterDataToTable(websqlTable,"小青","21","162cm","52kg");
            websqlInsterDataToTable(websqlTable,"小紫","25","195cm","80kg");
```

## 指定表中查找所有数据或查找某条数据

同样用到transaction方法用以处理事务。  
a). 查找所有数据
```javascript
function websqlGetAllData(tableName){
    var selectALLSQL = 'SELECT * FROM ' + tableName;
    dataBase.transaction(function (ctx) {
        ctx.executeSql(selectALLSQL,[],function (ctx,result){
                alert('查询成功: ' + tableName + result.rows.length);
                var len = result.rows.length;
                for(var i = 0;i < len;i++) {
                    console.log("NAME = "  + result.rows.item(i).NAME);
                    console.log("AGE = "  + result.rows.item(i).AGE);
                    console.log("HEIGHT = "  + result.rows.item(i).HEIGHT);
                    console.log("WEIGTH = "  + result.rows.item(i).WEIGTH);
                    console.log("-------- 我是分割线 -------");
                }
            },
            function (tx, error) {
                alert('查询失败: ' + error.message);
            });
    });
}
 websqlGetAllData(websqlTable);  
```

b). 查找某条数据

```javascript
function websqlGetAData(tableName,name){
    var selectSQL = 'SELECT * FROM ' + tableName + ' WHERE NAME = ?'
    dataBase.transaction(function (ctx) {
        ctx.executeSql(selectSQL,[name],function (ctx,result){
                alert('查询成功: ' + tableName + result.rows.length);
                var len = result.rows.length;
                for(var i = 0;i < len;i++) {
                    console.log("NAME = "  + result.rows.item(i).NAME);
                    console.log("AGE = "  + result.rows.item(i).AGE);
                    console.log("HEIGHT = "  + result.rows.item(i).HEIGHT);
                    console.log("WEIGTH = "  + result.rows.item(i).WEIGTH);
                }
            },
            function (tx, error) {
                alert('查询失败: ' + error.message);
            });
    });
}
 websqlGetAData(websqlTable,"小紫");   
```

## 删除数据

a). 删除表里的全部数据
```javascript
function websqlDeleteAllDataFromTable(tableName){
    var deleteTableSQL = 'DELETE FROM ' + tableName;
    localStorage.removeItem(tableName);
    dataBase.transaction(function (ctx,result) {
        ctx.executeSql(deleteTableSQL,[],function(ctx,result){
            alert("删除表成功 " + tableName);
        },function(tx, error){
            alert('删除表失败:' + tableName + error.message);
        });
    });
}
 websqlDeleteAllDataFromTable(websqlTable);   
```

b). 删除表里的一条数据
```javascript
function websqlDeleteADataFromTable(tableName,name){
    var deleteDataSQL = 'DELETE FROM ' + tableName + ' WHERE NAME = ?';
    localStorage.removeItem(tableName);
    dataBase.transaction(function (ctx,result) {
        ctx.executeSql(deleteDataSQL,[name],function(ctx,result){
            alert("删除成功 " + tableName + name);
        },function(tx, error){
            alert('删除失败:' + tableName  + name + error.message);
        });
    });
}
 websqlDeleteADataFromTable(websqlTable,"小蓝");   
```

## 修改某条数据
```javascript
function websqlUpdateAData(tableName,name,age){
    var updateDataSQL = 'UPDATE ' + tableName + ' SET AGE = ? WHERE NAME = ?';
    dataBase.transaction(function (ctx,result) {
        ctx.executeSql(updateDataSQL,[age,name],function(ctx,result){
            alert("更新成功 " + tableName + name);
        },function(tx, error){
            alert('更新失败:' + tableName  + name + error.message);
        });
    });
}
websqlUpdateAData(websqlTable,"小红","1000")       
```