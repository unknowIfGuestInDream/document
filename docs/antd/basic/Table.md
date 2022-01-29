> 开发中常用的table功能

## 序号列
```typescript
    {
      title: '序号',
      width: 50,
      hideInSearch: true,
      hideInTable: false,
      render: (text, record, index) => `${index + 1}`,
    },
```

## 列排序
```typescript
    {
      title: '菜单编号',
      dataIndex: 'I_ID',
      width: 80,
      sorter: (a: any, b: any) => a.I_ID.localeCompare(b.I_ID, 'en'),
    },
```

## 单元格弹出全部内容
```typescript
    {
      title: '访问路径',
      dataIndex: 'V_ADDRESS',
      width: 150,
      render: (text) => (
        <span
          style={{
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
            display: 'inline-block',
            width: 250,
          }}
          title={`${text}`}
        >
          {text}
        </span>
      ),
    },
```

## 表格内容完全展开，出现滚动条
```typescript
<ProTable
  scroll={{ x: 'max-content' }}
```

## 超链接
```typescript
{
    title: '应用名称',
    dataIndex: 'name',
    render: (_) => <a>{_}</a>,
  }
```