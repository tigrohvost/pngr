Basic flask web page which allows you to ping an internet address: IP or FQDN.

Часть про написание кода фронта и бэка допишем потом, а сейчас, когда у нас уже есть докерфайл для бэка, построим пайплайн с помощью GitHub Actions. Пойдем по вот этому гайду:
https://docs.docker.com/guides/gha/
Первое, что там надо сделать - это открыть следующий гайд, про Personal Access Tokens:
https://docs.docker.com/security/for-developers/access-tokens/
логинимся на DockerHub и идем в соответствующий раздел:
https://app.docker.com/settings/personal-access-tokens
где генерим токен и сохраняем его.

Затем добавляем креды в репозиторий:
add the credentials to your GitHub repository so you can use them in GitHub Actions:
Settings > Security, go to Secrets and variables > Actions.
Создаем repository secret с нашм PAT и variable c логином.

Создаем  в .github/workflows/docker-ci.yml
