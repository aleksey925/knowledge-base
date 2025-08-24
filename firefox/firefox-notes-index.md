Firefox
=======

# Оглавление

- [Синхронизация настроек между разными ПК](#синхронизация-настроек-между-разными-пк)


# Синхронизация настроек между разными ПК

Конфигурацию Firefox можно синхронизировать между разными пк используя подход [dotfiles](../macos/macos-notes-index.md#Хранение-конфигов-системы-в-git).
Для того чтобы это реализовать, нам нужно добавить под версионный контроль следующие файлы:

- `~/Library/Application Support/Firefox/installs.ini`
- `~/Library/Application Support/Firefox/profiles.ini`

Эти файлы описывают какие профили есть и какой профиль будет загружаться по умолчанию при открытии Firefox.

После этого нужно добавить в `~/Library/Application Support/Firefox/Profiles/<profile-name>/` файл `user.js` примерно 
следующего содержания (и так же добавить его под версионный контроль):

```js
// =============================================================================
// Firefox User Configuration
// =============================================================================

// Startup
user_pref("browser.startup.page", 3);  // General -> Startup -> Open previous windows and tabs

// Language
user_pref("intl.locale.requested", "en-US,ru"); // General -> Language -> Set Alternatives...

// Tabs
user_pref("browser.tabs.tabMinWidth", 100);
user_pref("browser.tabs.insertAfterCurrent", true);
user_pref("browser.warnOnQuitShortcut", true);  // General -> Tabs -> Ask before quitting with *Q
user_pref("browser.tabs.warnOnClose", true);  // General -> Tabs -> Ask before closing multiple tabs

// Homepage
user_pref("browser.newtabpage.activity-stream.topSitesRows", 1);  // Home -> Firefox Home Content -> Shortcuts
user_pref("browser.newtabpage.activity-stream.feeds.section.highlights", false);  // Home -> Firefox Home Content -> Recent activity
user_pref("browser.newtabpage.activity-stream.showSponsored", false);
user_pref("browser.newtabpage.activity-stream.showSponsoredCheckboxes", false);  // Home -> Firefox Home Content -> Support Firefox
user_pref("browser.newtabpage.activity-stream.showSponsoredTopSites", false);  // Home -> Firefox Home Content -> Support Firefox
```

Здесь мы через вызов `user_pref` определяем настройки, которые будут синхронизироваться и которые теперь задаются через
код. При запущенном Firefox значения настроек можно смотреть через посещение `about:config`.

Готово. Теперь при синхронизации dotfiles вы всегда будете получать актуальную конфигурацию Firefox. Если на новом ПК 
вы сначала загрузите конфигурацию, а потом впервые установите и запустите Firefox, у вас сразу инициализируется нужный 
профиль с нужными настройками. В случае если Firefox уже использовался, нужно будет либо удалить вручную старую папку с 
профилем, либо переименовать её (если нужно сохранить открытые вкладки и т. д.).
