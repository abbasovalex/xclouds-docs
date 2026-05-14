# Dev Tunnel / Туннель для разработки

Туннель пригодится на этапе разработки и тестирования чат-ботов, платежных сервисов и других API, где вам нужно принимать данные через веб-хуки / webhooks.
На нашей платформе вы за пару секунд получите домен с поддержкой HTTPS вида xxxxx.tunnel.xclouds.dev через который откроется прямой доступ к запущенному сайту или приложению на вашем ПК/ноутбуке.
Таким образом, когда сторонний сервис будет отправлять вам данные на xxxxx.tunnel.xclouds.dev вы будете получать и обрабатывать их прямо на своем localhost.
Это сильно сэкономит вам силы, нервы и избавит от поиска сложных решений.

<p class="tip">
    Обратите внимание на то, что туннель предназначен только для разработки и тестирования.
    Не используйте его в production среде.
</p>

## Установка

#### 1. Скачайте наш клиент на свой ПК / ноутбук

- macOS Apple Silicon: [xclouds-darwin-arm64.zip](https://xclouds.dev/staticfiles/xclouds-cli/releases/xclouds-darwin-arm64.zip)
- macOS Intel: [xclouds-darwin-amd64.zip](https://xclouds.dev/staticfiles/xclouds-cli/releases/xclouds-darwin-amd64.zip)
- Linux x86-64: [xclouds-linux-amd64.tar.gz](https://xclouds.dev/staticfiles/xclouds-cli/releases/xclouds-linux-amd64.tar.gz)
- Linux ARM64: [xclouds-linux-arm64.tar.gz](https://xclouds.dev/staticfiles/xclouds-cli/releases/xclouds-linux-arm64.tar.gz)
- Windows x86-64: [xclouds-windows-amd64.zip](https://xclouds.dev/staticfiles/xclouds-cli/releases/xclouds-windows-amd64.zip)
- Windows ARM64: [xclouds-windows-arm64.zip](https://xclouds.dev/staticfiles/xclouds-cli/releases/xclouds-windows-arm64.zip)

#### 2. Распакуйте и установите клиент

###### macOS

```bash
unzip ~/Downloads/xclouds-darwin-arm64.zip
chmod +x ~/Downloads/dist/xclouds-darwin-arm64
xattr -d com.apple.quarantine ~/Downloads/dist/xclouds-darwin-arm64 2>/dev/null || true
sudo mv ~/Downloads/dist/xclouds-darwin-arm64 /usr/local/bin/xclouds
```

###### Linux

```bash
tar -xvzf ~/Downloads/xclouds-linux-amd64.tar.gz
chmod +x ~/Downloads/dist/xclouds-linux-amd64
sudo mv ~/Downloads/dist/xclouds-linux-amd64 /usr/local/bin/xclouds
```

###### Windows

```powershell
unzip C:\Users\YourName\Downloads\xclouds-windows-amd64.zip
move "C:\Users\YourName\Downloads\dist\xclouds-windows-amd64.exe" "C:\Program Files\MyApp\xclouds.exe"
```

#### 3. Запустите своё локальное приложение или сайт

Если у вас еще нет своего сайта / приложения, для демонстрации возможности запустите в терминале следующую команду:
```bash
python -m http.server 8080
```

После этого вы сможете открыть в своем браузере адрес сайта:

```text
http://localhost:8080
```

## Запуск туннеля
Пока только вы можете видеть то, что открывается по http://localhost:8080. Давайте временно свяжем этот адрес с публичным доменом, тогда 
любой желающий сможет видеть и отправлять данные на этот адрес. Запустите следующую команду. Обратите внимание на то, что вместо 
_YOUR_TUNNEL_TOKEN_ вам надо указать свой ключ. Ключ находится в личном кабинете на xclouds.dev

**macOS/Linux:**

```bash
xclouds tunnel start --authtoken YOUR_TUNNEL_TOKEN --port 8080
```

Если бинарный файл не добавлен в `PATH`, запустите его по полному пути:

```bash
~/Downloads/dist/xclouds-darwin-arm64 tunnel start --authtoken YOUR_TUNNEL_TOKEN --port 8080
```

**Windows:**

```powershell
xclouds tunnel start --authtoken YOUR_TUNNEL_TOKEN --port 8080
C:\Users\YourName\Downloads\dist\xclouds-windows-amd64.exe tunnel start --authtoken YOUR_TUNNEL_TOKEN --port 8080
```

После запуска вы увидите свой публичный домен. Поздравляем, теперь вы можете выслать публичный домен коллегам или указать для приема веб-хуков / webhooks:

```bash
Prepare tunneling ...
✓ Session status: online
✓ Forwarding https://xxxxxxxx-xxxx.tunnel.xclouds.dev → http://localhost:8080

Press Ctrl+C to stop
```

<p class="warn">
    Ваш домен не меняется. Он будет сохраняться при перезапусках. При желании вы можете сменить домен.
</p>


## Возможные ошибки

| Симптом                                                | Возможная причина | Как исправить                                                                                         |
|--------------------------------------------------------| --- |-------------------------------------------------------------------------------------------------------|
| URL не отвечает                                        | Локальное приложение не запущено | Сначала проверьте `http://localhost:8080`                                                             |
| Отвечает не то приложение                              | Неверный порт | Запустите tunnel с тем же портом, где работает приложение                                             |
| `command not found`                                    | CLI не добавлен в `PATH` | Запустите бинарник по полному пути или перенесите его в `/usr/local/bin`                              |
| macOS блокирует бинарник или пугает недоверием к файлу | Остался quarantine flag | Выполните `xattr -d com.apple.quarantine ~/Downloads/dist/xclouds-darwin-arm64 2>/dev/null \|\| true` |
| Внешний сервис не принимает URL                        | Ему нужен HTTPS | Используйте публичный HTTPS URL вида https://xxxxxxxx-xxxx.tunnel.xclouds.dev, а не `localhost:8080`  |
