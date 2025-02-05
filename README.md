TL;DR: https://github.com/narmidm/github-actions-kubernetes но на питоне)
В одном бигтехе, в зеленом финтехе жил да был админ и админил он большую систему на кубере, а базовые вещи давно руками не делал. Поэтому пусть у нас будет веб-приложение, которое гипотетически зарабатывает бизнесу деньги тем, что пингует заданные адреса. Состит оно из двух (для начала) микросервисов и написано на питоне: flask, немножко requests и js. Пока что stateless.


Часть про написание кода фронта и бэка допишу потом, а сейчас построим пайплайн с помощью GitHub Actions - нам тут главное быстрее выкатиться в прод, стартап мы или где =^_^=


Для начала сделаем так, чтобы при коммите в мастер ветку или пулл реквестах образ пересобирался и пушился в докерхаб регистри.
Пойдем по вот этому гайду: https://docs.docker.com/guides/gha/


Первое, что там надо сделать - это открыть следующий гайд, про Personal Access Tokens:
https://docs.docker.com/security/for-developers/access-tokens/


Логинимся на DockerHub и идем в соответствующий раздел:
https://app.docker.com/settings/personal-access-tokens
где генерим токен и сохраняем его.


В гитхабе идем в настройки: Settings > Security, go to Secrets and variables > Actions.
Создаем repository secret с нашим PAT - токеном с докерхаба и переменную - variable c логином. Теперь воркер github actions может логиниться в наш регистри и пушить туда собранные образы.


В гитхабе в репозитории создаем файл .github/workflows/docker-ci.yml - наполнение смотри в проекте.

Получаем ошибку, потому что по гайду мы работаем в корневом каталоге, а в нашем проекте два сервиса, каждый в своем подкаталоге.
Так что нам надо добавить явное указание поддиректории, поэтому в секции build and push в блоке with добавляем:
context: ./back и сборка работает ^_^ Правда, в докерхабе она кладется в репозитарий my-image, что тоже надо поправить. 
Для начала просто заменим "my-image" на "pngr" - образы теперь летят в репозитарий pngr, правда, все равно под неправильным тегом "main".
Пока что заменим "pngr" на "back", TBD: поменять тег и добавить файлы типа readme в исключения, чтобы при их изменении не пересобирались образы.


Теперь добавим сборку второго образа - фронта. Можно добавить в том же файле, но могут быть проблемы с переменными, а можно добавить еще один action - так пока что будет проще.
Итак, два образа на докерхабе автоматически пересобираются по изменениям в репозитории. Время откопать наш кластер!


Часть про создание кластера через kubeadm тоже добавлю, а пока что допустим, что он у нас уже есть и состоит из двух нод 4/8: управляющей и рабочей.


Теперь нам надо:
1) подружить github actions с кластером
2) прописать в deployment'ах ссылки на образы в докерхабе
3) а еще при создании деплойментов должен быть доступ до докерхаба из самого кластера.

Github actions будет ходить в наш кластер с помощью https://github.com/tale/kubectl-action. Для этого нужно взять из кластера kubeconfig: берем с мастерноды /etc/kubernetes/admin.conf.

Создаем новый секрет в /settings/secrets/actions/new с именем KUBE_CONFIG и содержимым admin.conf.

Создаем новый action, например, k8s_update.yml рядом с файлами первых action'ов.
Чтобы можно было поотлаживаться руками, условие будет workflow_dispatch. А также не забываем кодировать конфиг куба в base64 если в ямлике так и сказано:      
    
    base64-kube-config: ${{ secrets.KUBE_CONFIG }}


Это стоило мне нескольких часов ^_^

Теперь давайте зедеплоим бэк. Для этого kubectl на раннере (runner - виртуалка гитхаба, которая запускает наш action) должен достучаться в репозиторий на докерхабе. Можно и без атворизации, если образ публичный - давайте начнем с этого варианта, а потом закроем авторизацией, как описано в https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/

По умолчанию kubectl считает, что мы используем dockerhub - и правильно делает :)
