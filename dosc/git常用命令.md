#### 一、本地分支

```
1、创建本地分支，然后切换到dev分支
$ git checkout -b dev
git checkout命令加上-b参数表示创建并切换，相当于以下两条命令：
$ git branch dev
$ git checkout dev

2、查看当前分支
$ git branch
* dev
  master
  
3、提交到暂存区
$ git add readme.txt

4、提交到本地仓库
$ git commit -m "feat:add readme.txt"

5、将dev分支的工作内容合并到master分支
先切换到master分支上，后执行合并操作
$ git checkout master
$ git merge dev
* git merge命令用于合并指定分支到当前分支。合并后查看内容是和dev分支一致的

6、删除dev分支
$ git branch -d dev

创建、合并和删除分支非常快，鼓励使用分支来完成某个短期任务，合并后再删掉，比起直接在master上工作过程更安全。

7、查看日志
$ git log/git reflog

8、版本回退
$ git reset --hard 版本号

只做了add操作，还没执行commit的回退(回退到当前版本)
$ git reset HEAD

回退到当前版本后，继续把文件还原
$ git checkout <file>
```

#### 二、远程分支

```
1、查看远程分支
git branch -r

2、更新远程分支列表
git remote update origin --prune

3、拉取远程分支并创建本地分支
git checkout -b 本地分支名 origin/远程分支名

4、远程仓库创建test分支
git checkout -b test
git push origin test

5、查看所有分支
git branch -a

6、清除某一个文件的更改
git checkout -- file

7、删除远程分支
git push origin --delete dev
```

#### 三、git提交规范

```
commit类别

feat：新功能（feature）
fix：修补 bug
delete: 删除功能
style: 样式相关
merge：合并代码
refactor：重构（即不是新增功能，也不是修改 bug 的代码变动）
perf：优化
revert：撤销上一次的 commit
docs：文档（documentation）
test：增加测试
chore：构建过程或辅助工具的变动
build：影响构建系统或外部依赖项的更改（示例范围：gulp、broccoli、npm）
ci：对我们的 CI 配置文件和脚本的更改（示例范围：Travis、Circle、BrowserStack、SauceLabs）
```

