sudo adduser deployer  # Создаём отдельного пользователя
sudo usermod -aG sudo deployer  # Даём права sudo
su - deployer  # Переключаемся на него
