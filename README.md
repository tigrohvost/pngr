Basic flask web page which allows you to ping an internet address: IP or FQDN.

Часть про написание кода фронта и бэка допишу потом, а сейчас построим пайплайн с помощью GitHub Actions.
Для начала сделаем так, чтобы при коммите в мастер ветку или пулл реквестах образ пересобирался и пушился в докерхаб регистри.
Пойдем по вот этому гайду: https://docs.docker.com/guides/gha/
Первое, что там надо сделать - это открыть следующий гайд, про Personal Access Tokens:
https://docs.docker.com/security/for-developers/access-tokens/
логинимся на DockerHub и идем в соответствующий раздел:
https://app.docker.com/settings/personal-access-tokens
где генерим токен и сохраняем его.

Затем добавляем креды в репозиторий: Settings > Security, go to Secrets and variables > Actions.
Создаем repository secret с нашм PAT и variable c логином. Теперь воркер github actions может логиниться в наш регистри и пушить туда собранные образы.

Создаем  в .github/workflows/docker-ci.yml
Получаем ошибку, потому что по гайду мы работаем в корневом каталоге, а в нашем проекте два сервиса, каждый в своем подкаталоге.
Так что нам надо добавить явное указание поддиректории, поэтому в секции build and push в блоке with добавляем:
context: ./back
И сборка работает ^_^ Правда, в докерхабе она кладется в репозитарий my-image, что тоже надо поправить. 
Для начала просто заменим my-image на pngr - образы теперь летят в репозитарий pngr, правда, все равно под неправильным тегом.
Пока что заменим pngr на back, останется поменять тег)
