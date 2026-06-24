import { chromium } from 'playwright';

const browser = await chromium.connectOverCDP(
    'wss://cdp.xclouds.dev/cdp/?api_key=YOUR_API_KEY',
);

const context = browser.contexts()[0];
const page = await context.newPage();
const client = await context.newCDPSession(page);
await client.send('Animation.enable');
client.on('Animation.animationCreated', () => console.log('Animation created!'));
const response = await client.send('Animation.getPlaybackRate');
console.log('playback rate is ' + response.playbackRate);
await client.send('Animation.setPlaybackRate', {
  playbackRate: response.playbackRate / 2
});
await browser.close();
