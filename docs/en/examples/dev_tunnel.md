# Dev Tunnel Example

Use the xClouds dev tunnel when an external service needs to call an app that is still running on your laptop. This is useful for webhooks, callbacks, demos, and browser tests against a local server.

## What You Will Do

You will expose a local app on port `8080` through an xClouds public HTTPS URL.

## 1. Download The CLI

Choose the archive for your platform from the xClouds app.

- macOS Apple Silicon: `xclouds-darwin-arm64.zip`
- macOS Intel: `xclouds-darwin-amd64.zip`
- Linux x86-64: `xclouds-linux-amd64.tar.gz`
- Linux ARM64: `xclouds-linux-arm64.tar.gz`
- Windows x86-64: `xclouds-windows-amd64.zip`
- Windows ARM64: `xclouds-windows-arm64.zip`

## 2. Install On macOS

```bash
unzip ~/Downloads/xclouds-darwin-arm64.zip
chmod +x ~/Downloads/dist/xclouds-darwin-arm64
xattr -d com.apple.quarantine ~/Downloads/dist/xclouds-darwin-arm64 2>/dev/null || true
sudo mv ~/Downloads/dist/xclouds-darwin-arm64 /usr/local/bin/xclouds
```

## 3. Install On Linux

```bash
tar -xvzf ~/Downloads/xclouds-linux-amd64.tar.gz
chmod +x ~/Downloads/dist/xclouds-linux-amd64
sudo mv ~/Downloads/dist/xclouds-linux-amd64 /usr/local/bin/xclouds
```

## 4. Install On Windows

```powershell
unzip C:\Users\YourName\Downloads\xclouds-windows-amd64.zip
move "C:\Users\YourName\Downloads\dist\xclouds-windows-amd64.exe" "C:\Program Files\MyApp\xclouds.exe"
```

## 5. Start Your Local App

Run any local server on port `8080`.

```bash
python -m http.server 8080
```

Expected local URL:

```text
http://localhost:8080
```

## 6. Start The Tunnel

```bash
xclouds tunnel start --authtoken YOUR_TUNNEL_TOKEN --port 8080
```

If you did not move the binary into your `PATH`, run it by full path:

```bash
~/Downloads/dist/xclouds-darwin-arm64 tunnel start --authtoken YOUR_TUNNEL_TOKEN --port 8080
```

On Windows:

```powershell
xclouds tunnel start --authtoken YOUR_TUNNEL_TOKEN --port 8080
C:\Users\YourName\Downloads\dist\xclouds-windows-amd64.exe tunnel start --authtoken YOUR_TUNNEL_TOKEN --port 8080
```

## 7. Verify

Open your assigned tunnel URL in a browser or put it into the webhook settings of the service you are testing.

Expected result:

```text
The external request reaches your local server on port 8080.
```

## Common Errors

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| The URL does not respond | Local app is not running | Start your app and check `http://localhost:8080` first |
| The wrong local app responds | Wrong port | Start the tunnel with the same port your app uses |
| Command not found | CLI is not in `PATH` | Run the binary by full path or move it into `/usr/local/bin` |
| macOS blocks the binary | Quarantine flag is still present | Run the `xattr -d com.apple.quarantine ...` command |
| External service rejects the URL | It requires HTTPS | Use the xClouds public HTTPS URL, not `localhost` |

## Production Notes

Use the dev tunnel for development and testing. For production callbacks, use a stable production URL and validate every incoming request according to the external service documentation.
