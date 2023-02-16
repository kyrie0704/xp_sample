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

回退本地最近一次提交
 $ git reset --soft HEAD~1

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

8、将代码提交到远程分支
git push -u origin 远程仓库分支名
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

#### 四、git常用撤销命令

```
1、撤销add操作
恢复到上次add操作之前：git reset HEAD
仅恢复某个文件：git reset HEAD 文件名

2、撤销commit操作
不删除工作空间改动代码，撤销commit，并且撤销add操作：git reset HEAD^
不删除工作空间改动代码，撤销commit，不撤销add操作：git reset --soft HEAD^
删除工作空间改动代码，撤销commit，撤销add操作： git reset --hard HEAD^

3、撤销上次git操作
比如使用了git reset --hard HEAD^命令，将改动的代码也删除了，需要恢复改动的代码，可以先使用git log查看操作记录，然后使用git reset commit_id回滚到对应节点
```
#### 五、远程仓库

```
1、添加远程仓库
git remote add origin(远程仓库名称) 远程仓库地址

2、删除远程仓库连接
git remote rm origin(远程仓库名称)

3、更改远程仓库连接
git remote set-url origin(远程仓库名称) 远程仓库地址

4、修改远程仓库名称（也可以先删除再添加）
git remote rename <old-remote-name> <new-remote-name>
```

