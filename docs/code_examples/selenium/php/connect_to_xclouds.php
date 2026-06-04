<?php

require __DIR__ . '/vendor/autoload.php';

use Facebook\WebDriver\Remote\DesiredCapabilities;
use Facebook\WebDriver\Remote\RemoteWebDriver;

$driver = RemoteWebDriver::create(
    'http://selenium.xclouds.dev/wd/hub?api_key=YOUR_API_KEY',
    DesiredCapabilities::chrome()
);

try {
    $driver->get('https://google.com');
    echo $driver->getPageSource();
} finally {
    $driver->quit();
}
