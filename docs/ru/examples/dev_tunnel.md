# Пример Dev Tunnel

Используйте xClouds dev tunnel, когда внешний сервис должен вызвать приложение, которое пока запущено на вашем ноутбуке. Это подходит для webhooks, callbacks, демо и браузерных тестов локального сервера.

## Что получится

Вы откроете локальное приложение на порту `8080` через публичный HTTPS URL xClouds.

## 1. Скачайте CLI

Выберите архив для своей платформы в приложении xClouds.

- macOS Apple Silicon: `xclouds-darwin-arm64.zip`
- macOS Intel: `xclouds-darwin-amd64.zip`
- Linux x86-64: `xclouds-linux-amd64.tar.gz`
- Linux ARM64: `xclouds-linux-arm64.tar.gz`
- Windows x86-64: `xclouds-windows-amd64.zip`
- Windows ARM64: `xclouds-windows-arm64.zip`

## 2. Установка на macOS

```bash
unzip ~/Downloads/xclouds-darwin-arm64.zip
chmod +x ~/Downloads/dist/xclouds-darwin-arm64
xattr -d com.apple.quarantine ~/Downloads/dist/xclouds-darwin-arm64 2>/dev/null || true
sudo mv ~/Downloads/dist/xclouds-darwin-arm64 /usr/local/bin/xclouds
```

## 3. Установка на Linux

```bash
tar -xvzf ~/Downloads/xclouds-linux-amd64.tar.gz
chmod +x ~/Downloads/dist/xclouds-linux-amd64
sudo mv ~/Downloads/dist/xclouds-linux-amd64 /usr/local/bin/xclouds
```

## 4. Установка на Windows

```powershell
unzip C:\Users\YourName\Downloads\xclouds-windows-amd64.zip
move "C:\Users\YourName\Downloads\dist\xclouds-windows-amd64.exe" "C:\Program Files\MyApp\xclouds.exe"
```

## 5. Запустите локальное приложение

Запустите любой локальный сервер на порту `8080`.

```bash
python -m http.server 8080
```

Ожидаемый локальный URL:

```text
http://localhost:8080
```

## 6. Запустите tunnel

```bash
xclouds tunnel start --authtoken YOUR_TUNNEL_TOKEN --port 8080
```

Если бинарный файл не добавлен в `PATH`, запустите его по полному пути:

```bash
~/Downloads/dist/xclouds-darwin-arm64 tunnel start --authtoken YOUR_TUNNEL_TOKEN --port 8080
```

На Windows:

```powershell
xclouds tunnel start --authtoken YOUR_TUNNEL_TOKEN --port 8080
C:\Users\YourName\Downloads\dist\xclouds-windows-amd64.exe tunnel start --authtoken YOUR_TUNNEL_TOKEN --port 8080
```

## 7. Проверьте

Откройте назначенный tunnel URL в браузере или вставьте его в настройки webhook сервиса, который вы тестируете.

Ожидаемый результат:

```text
Внешний запрос приходит на ваш локальный сервер на порту 8080.
```

## Частые ошибки

| Симптом | Возможная причина | Как исправить |
| --- | --- | --- |
| URL не отвечает | Локальное приложение не запущено | Сначала проверьте `http://localhost:8080` |
| Отвечает не то приложение | Неверный порт | Запустите tunnel с тем же портом, где работает приложение |
| `command not found` | CLI не добавлен в `PATH` | Запустите бинарник по полному пути или перенесите его в `/usr/local/bin` |
| macOS блокирует бинарник | Остался quarantine flag | Выполните `xattr -d com.apple.quarantine ...` |
| Внешний сервис не принимает URL | Ему нужен HTTPS | Используйте публичный HTTPS URL xClouds, а не `localhost` |

## Для production

Dev tunnel предназначен для разработки и тестирования. Для production callbacks используйте стабильный production URL и проверяйте каждый входящий запрос по документации внешнего сервиса.
