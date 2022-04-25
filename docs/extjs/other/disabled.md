## 禁用开发工具,右键菜单和控制台

```javascript
document.oncontextmenu = function () {
        event.returnValue = false;
    };
    //禁用开发者工具F12
    document.onkeydown = document.onkeyup = document.onkeypress = function (event) {
        let e = event || window.event || arguments.callee.caller.arguments[0];
        if (e && e.keyCode === 123) {
            e.returnValue = false;
            return false;
        }
    };
    let userAgent = navigator.userAgent;
    if (userAgent.indexOf("Firefox") > -1) {
        let checkStatus;
        let devtools = /./;
        devtools.toString = function () {
            checkStatus = "on";
        };
        setInterval(function () {
            checkStatus = "off";
            console.log(devtools);
            console.log(checkStatus);
            console.clear();
            if (checkStatus === "on") {
                let target = "";
                try {
                    window.open("about:blank", (target = "_self"));
                } catch (err) {
                    let a = document.createElement("button");
                    a.onclick = function () {
                        window.open("about:blank", (target = "_self"));
                    };
                    a.click();
                }
            }
        }, 200);
    } else {
        //禁用控制台
        let ConsoleManager = {
            onOpen: function () {
                alert("Console is opened");
            },
            onClose: function () {
                alert("Console is closed");
            },
            init: function () {
                let self = this;
                let x = document.createElement("div");
                let isOpening = false,
                    isOpened = false;
                Object.defineProperty(x, "id", {
                    get: function () {
                        if (!isOpening) {
                            self.onOpen();
                            isOpening = true;
                        }
                        isOpened = true;
                        return true;
                    }
                });
                setInterval(function () {
                    isOpened = false;
                    console.info(x);
                    console.clear();
                    if (!isOpened && isOpening) {
                        self.onClose();
                        isOpening = false;
                    }
                }, 200);
            }
        };
        ConsoleManager.onOpen = function () {
            //打开控制台，跳转
            let target = "";
            try {
                window.open("about:blank", (target = "_self"));
            } catch (err) {
                let a = document.createElement("button");
                a.onclick = function () {
                    window.open("about:blank", (target = "_self"));
                };
                a.click();
            }
        };
        ConsoleManager.onClose = function () {
            alert("Console is closed!!!!!");
        };
        ConsoleManager.init();
    }
```

## 消息提示方法

```javascript
    //提示信息 封装
    function Toast(msg, duration) {
        duration = isNaN(duration) ? 3000 : duration;
        var m = document.createElement('div');
        m.innerHTML = msg;
        m.style.cssText = "font-size: .32rem;color: rgb(255, 255, 255);background-color: rgba(0, 0, 0, 0.6);padding: 10px 15px;margin: 0 0 0 -60px;border-radius: 4px;position: fixed;    top: 50%;left: 50%;width: 130px;text-align: center;";
        document.body.appendChild(m);
        setTimeout(function () {
            var d = 0.5;
            m.style.opacity = '0';
            setTimeout(function () {
                document.body.removeChild(m)
            }, d * 1000);
        }, duration);
    }
```

使用： `Toast('开发工具已禁用', 1000);`