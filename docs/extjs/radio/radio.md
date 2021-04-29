## radioGroup

```javascript
var formPanel = Ext.create('Ext.form.Panel', {
            id: 'formPanel',
            layout: 'column',
            frame: true,
            autoScroll: true,
            border: false,
            validateOnChange: true,
            defaults: {
                labelAlign: 'right',
                labelWidth: 100,
                inputWidth: 140,
                margin: '5,5,5,5'
            },
            items: [{
                xtype: 'radiogroup',
                id: 'rb',
                layout: 'hbox',
                defaults: {
                    boxLabelAlign: 'before',
                    width: 120
                },
                items: [{
                    boxLabel: '1',
                    name: 'rb',
                    checked: true,
                    inputValue: 1
                }, {
                    boxLabel: '2',
                    name: 'rb',
                    inputValue: 2
                }],
                listeners: {
                    'change': function () {
                         var value = Ext.getCmp('rb').getChecked()[0].inputValue;
                    }
                }
            }]
        });
```

## radiofield
```javascript
var formPanel = Ext.create('Ext.form.Panel', {
            id: 'formPanel',
            layout: 'column',
            frame: true,
            border: false,
            defaults: {
                labelAlign: 'right',
                labelWidth: 100,
                inputWidth: 140,
                margin: '4,0,0,0'
            },
            items: [{
                xtype: 'fieldcontainer',
                fieldLabel: '验收结果',
                defaultType: 'radiofield',
                allowBlank: false,
                defaults: {
                    width: 120
                },
                layout: 'hbox',
                items: [{
                    boxLabel: '合格',
                    name: 'result',
                    id: 'radio1',
                    inputValue: '合格'
                }, {
                    boxLabel: '不合格',
                    name: 'result',
                    id: 'radio2',
                    inputValue: '不合格'
                }]
            }]
        });
```