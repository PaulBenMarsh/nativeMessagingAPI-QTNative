# nativeMessagingAPI-QTNative

<h1>Overview</h1>

QTNative is a simple, native Python application which acts as a host for communicating with a corresponding Google Chrome extension using the Native Messaging API. QTNative is inspired by the [Chromium Native Messaging API example project](https://chromium.googlesource.com/chromium/src/+/master/chrome/common/extensions/docs/examples/api/nativeMessaging). All of the code has been redone.

<p align="center">
<img src="https://github.com/PaulBenMarsh/nativeMessagingAPI-QTNative/blob/master/screenshots/qtnative_screenshot.png?raw=true">
</p>

<h1>Native Messaging API</h1>

[Chrome's developer pages](https://developer.chrome.com/apps/nativeMessaging) have an excellent tutorial for- and description of the Native Messaging API. In a nutshell: The Native Messaging API may be used to communicate between a Google Chrome extension and a native application running in the background. Normally, if you want to develop a Google Chrome extension, you have no choice but to use JavaScript, since the browser supports it natively. Using the Native Messaging API allows you to effectively develop Google Chrome extensions in any language of your chosing - though they will only work in your local environment, or environments which can execute your native application, well, natively.

<h1>Dependencies</h1>
<ul>
  <li><a href="https://www.python.org/downloads/" rel="nofollow">Python 3</a></li>
  <li><a href="https://pypi.org/project/virtualenvwrapper-win/" rel="nofollow">virtualenvwrapper-win==1.2.6</a></li>
  <li><a href="https://pypi.org/project/PyQt5/" rel="nofollow">PyQt5==5.14.2</a></li>
</ul>

This project assumes your operating system is Microsoft Windows, though it wouldn't be too difficult to get it working on MAC OS/Linux. The previously mentioned Chromium Native Messaging API example project is operating system agnostic - if you're interested in porting this to another operating system, that's where I would start looking. None of the Python code would require any changes, it would really just be the batch scripts and JSON/Manifest files. <code>virtualenvwrapper-win</code> isn't strictly required, but it's how I've chosen to organize the project. Any virtual environment manager will do.

<h1>Setup</h1>
<ol>
<li> You will have to modify the <code>host/run.bat</code> to reference your virtual environment. You will also have to modify <code>host/com.google.chrome.qtnative.echo-win.json</code> and enter the absolute path to the <code>run.bat</code> batch script.</li>
<li> Execute <code>host/install.bat</code> to install the necessary registry keys.</li>
<li> In Google Chome, go to <code>chrome://extensions/</code>, click on the <code>Load unpacked</code> button and select the QTNative <code>extension</code> folder in the dialog.</li>
</ol>
