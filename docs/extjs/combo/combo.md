## 下拉框宽度不够时增加滚动条

```css
.x-boundlist-item {
    white-space: nowrap !important;
}
```

## 获取下拉框选中数据store其它参数

```javascript
Ext.getCmp('dataSource').valueModels[0].data.DRIVER
```