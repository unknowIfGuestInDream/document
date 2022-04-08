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

```typescript
{
    title: (
      <>
        创建时间
        <Tooltip placement="top" title="这是一段描述">
          <QuestionCircleOutlined style={{ marginLeft: 4 }} />
        </Tooltip>
      </>
    ),
    width: 140,
    key: 'since',
    dataIndex: 'createdAt',
    valueType: 'date',
    sorter: (a, b) => a.createdAt - b.createdAt,
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

## 根据名称判断是否是图片
```typescript
          {(/(?:jpg|gif|png|jpeg)$/i.test(record.V_FILENAME)) &&
          (<>
              <Divider type="vertical"/>
              <a key={record.I_ID} onClick={() => {
                setImageUrl(getDownloadUrl('/api/contract-system/downloadContractRider', {
                  I_ID: record.I_ID,
                  V_FILEPATH: record.V_FILEPATH,
                  V_FILENAME: record.V_FILENAME
                }));
                setVisible(true);
              }}>预览</a>
            </>
          )}
```