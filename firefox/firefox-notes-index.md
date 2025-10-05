Firefox
=======

# Оглавление

- [Синхронизация настроек между разными ПК](#синхронизация-настроек-между-разными-пк)


# Синхронизация настроек между разными ПК

Конфигурацию Firefox можно синхронизировать между разными пк используя подход [dotfiles](../macos/macos-notes-index.md#Хранение-конфигов-системы-в-git).
Для того чтобы это реализовать, нам нужно добавить под версионный контроль следующие файлы:

- `~/Library/Application Support/Firefox/installs.ini`
- `~/Library/Application Support/Firefox/profiles.ini`

Они описывают, какие профили существуют и какой профиль будет загружаться по умолчанию при открытии Firefox.

После этого добавьте в каталог `~/Library/Application Support/Firefox/Profiles/<profile-name>/` файл `user.js` и 
поместите его под версионный контроль. Пример содержимого файла:

```js
// =============================================================================
// Firefox User Configuration
// =============================================================================

// Startup
user_pref("browser.startup.page", 3);  // General -> Startup -> Open previous windows and tabs

// Language
user_pref("intl.locale.requested", "en-US,ru");  // General -> Language -> Set Alternatives...

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

// Other
user_pref("accessibility.typeaheadfind.prefillwithselection", true);  // by default, insert selected text from page into search field
```

Данный файл автоматически загружается при каждом запуске и в нем мы через вызов `user_pref` задаем нужные нам настройки.
При работающем Firefox текущие значения настроек можно просмотреть, перейдя на страницу `about:config`.

После настройки синхронизации dotfiles вы будете автоматически получать актуальную конфигурацию Firefox на всех 
устройствах.

**Сценарии использования**

Новый компьютер (Firefox ещё не установлен или установлен, но не запускался ни разу):

1. загрузите конфигурацию из dotfiles
2. запустите Firefox
3. профиль автоматически инициализируется с нужными настройками

Существующая установка Firefox:

- переименуйте старую папку профиля (`~/Library/Application Support/Firefox/Profiles/<profile-name>/`) в соответствии 
  с названием профиля по умолчанию из файла `profiles.ini`

