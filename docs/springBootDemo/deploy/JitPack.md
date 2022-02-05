> 只要代码仓库是使用 GitHub，或者 其他几种常见的 Git 仓库托管服务，就可以立即接入 JitPack，完成jar包的发布。

以 [https://github.com/UnknownInTheDream/genCode](https://github.com/UnknownInTheDream/genCode ':target=_blank') 仓库为例，只需要在 [https://jitpack.io/](https://jitpack.io/ ':target=_blank')
页面输入框中，填写 `UnknownInTheDream/genCode`(github的网址前缀可省略，其他的需要完整网址) 并点击Look up按钮，即可完成接入.在 JitPack 完成构建之后，可通过 Release、Branch 甚至 Commit 获得不同版本的 jar 包，页面上提供了各种构建工具的接入方式，照着一顿操作就好了。

## 如何从 JitPack 下载依赖
以maven为例，首先加入JitPack网址地址
```xml
    <repositories>
		<repository>
		    <id>jitpack.io</id>
		    <url>https://jitpack.io</url>
		</repository>
	</repositories>
```

## 能否从没主动接入的 Git 库直接下载依赖
按照 JitPack 支持的版本规则（Release、Commit、Branch），可直接获得任意公开库的 jar 包，无论该仓库是否进行过主动接入。

## 关于 tag 中的 v 前缀
有一个需要注意的点是，在 GitHub 上，推荐使用的 tag 为使用 v 前缀的形式：
```markdown
Tagging suggestions

It’s common practice to prefix your version names with the letter v. Some good tag names might be v1.0 or v2.3.4.
```

但在版本号中，一般都使用不带 v 的形式。

当未主动在 JitPack 网站上面点击过 Release 版本的 Get it 按钮之前，在依赖时，version 只能使用带 v 前缀的形式。

如果想要使用不带 v 前缀的格式作为 version，可以找到相应版本，并点击 Get it 按钮之后，等待 JitPack 的构建完成（可以从 Log 中查看构建日志）。
