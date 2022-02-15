> antd Tree

## 树单选
```typescript
            <Tree
              treeData={treeData} //树的数据
              checkable={true}
              checkedKeys={checkedKeys}
              defaultExpandAll
              checkStrictly
              multiple={false}
              showLine={true} //文件目录结构展示，true树带线，false树不带线
              onCheck={(checkedKeys: any, e: any) => {
                //单选
                // @ts-ignore
                setCheckedKeys(checkedKeys.checked.length === 0 ? [] : [checkedKeys.checked[checkedKeys.checked.length - 1]]);
              }}
              height={700}
            />
```