# Contributing
## Contribute code
### _If you know django, skip this part._
Don't know Django or how to program? Read the docs:
 - [Python(en)](https://docs.python.org/3/tutorial/index.html), [Python(zh-hans)](https://docs.python.org/zh-cn/3/tutorial/index.html)
  - [Django(en)](https://docs.djangoproject.com/en/2.2/intro/), [Django(zh-hans)](https://docs.djangoproject.com/zh-hans/2.2/intro/)


### _If you know Git and GitHub, skip this part._
Don't know how to use Git? Read the docs:
  - [Git(en)](https://git-scm.com/book/en/v2), [Git(zh-hans)](https://git-scm.com/book/zh/v2)
After that, sign in GiHhub.


### _If you know command-line, skip this part._
GitHub is easy to use. To contribute, you may want to `fork this responsitory`. (Do these steps after installing Git and sign in GitHub)
```
Click the fork button on the top.
```
```bash
$ git clone https://github.com/<your-username>/math-competition.git
```
(If you use Windows, run the command above in Git Bash. It should be installed with Git.)

After doing some editing, run this (Do this after installing Python3 and make sure Python is in $PATH.)
```bash
$ pip install -r requirements
$ python manage.py runserver
```
Open your browser and open `localhost:8000` to test your website.

If you're satisfied, use
```bash
$ git add .
$ git commit -m "<Write your commit message here. It should describe what is this commit doing.>"
```
Use the following commands to push to GitHub.
```bash
$ git push origin master
```


### _If you know PR, skip this part_
Time to make your first `Pull Request`!

Click the `Compare & pull request` button, review your changes and write pull request messages.

If I'm satisfied, I'll merge it into my `master branch` from your `master branch`.(Not always `master`) You've done your contributing!

## Report issue
You can also report issue [here](https://github.com/xiaoyu2006/math-competition/issues).
