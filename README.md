## Запуск проекта с помощью Docker

1. Убедитесь, что у вас установлены Docker и Docker Compose.

2. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/vyakovlevv/OpenWalletLyceumProject.git
   cd OpenWalletLyceumProject
   ```
   
3. Запустите приложение
	```bash
	docker run -p 8080:8080 ${{ secrets.DOCKER_HUB_USERNAME }}/openwalletlyceumproject:latest
	```
	Приложение будет запущено на 8080 порту.
	