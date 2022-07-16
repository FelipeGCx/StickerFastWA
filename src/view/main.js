'use strict'

let lang;
let theme;
let animatedIsShow;
let language;
let directory;
const appVersion = '1.3.0';

async function init() {
    await getUserPreferences();
    await setLanguage(lang);
    loadLanguage(language);
    setLangCbx(lang);
    changeIconLang(lang);
    setThemeMode(theme);
    setThemeCbx(theme);
}

async function getUserPreferences() {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            pywebview.api.getUserPreferences().then((response) => {
                lang = response.lang;
                theme = response.theme;
                animatedIsShow = response.animatedIsShow;
                directory = response.directory;
                resolve();
            }).catch((error) => { reject(error) });
        }, 250);
    })

}

function setLanguage(iso) {
    lang = iso;
    return new Promise((resolve, reject) => {
        pywebview.api.getLanguageJson(iso).then((response) => {
            language = response;
            resolve();
        }).catch((error) => { reject(error) });
    })
}

function loadLanguage(language) {
    document.getElementById('textAnimated').dataset.tooltip = language.animated;
    document.getElementById('textNamePack').dataset.placeholder = language.namePack;
    document.getElementById('textNameAuthor').dataset.placeholder = language.nameAuthor;
    document.getElementById('textMaxImgs').textContent = language.maxImgs;
    document.getElementById('textOpenFolder').dataset.tooltip = language.openFolder
    document.getElementById('textBrowseFolder').dataset.tooltip = language.browseFolder;
    document.getElementById('textSelectIcon').dataset.tooltip = language.selectIcon;
    document.getElementById('textConserveImgs').textContent = language.conserveImgs;
    document.getElementById('textCreatePack').textContent = language.createPack;
    document.getElementById('textSettings').dataset.tooltip = language.settings;
    document.getElementById('textInfo').dataset.tooltip = language.info;
    document.getElementById('textThemeMode').textContent = language.themeMode;
    document.getElementById('textLanguage').textContent = language.language;
    document.getElementById('textLicense').textContent = language.license;
    document.getElementById('textTerms').textContent = language.terms;
    document.getElementById('textWarningTitle').textContent = language.warningTitle;
    document.getElementById('textWarningDescription').textContent = language.warningDescription;
    document.getElementById('textMaxSize').textContent = language.maxSize;
    document.getElementById('textMaxWeight').textContent = language.maxWeight;
    document.getElementById('textFormat').textContent = language.warningFormat;
    document.getElementById('textNoShowMore').textContent = language.noShowMore;
    document.getElementById('textAccept').textContent = language.acept;
    document.getElementById("requiredMsgNamePack").textContent = language.requiredMsgNamePack;
    document.getElementById("requiredMsgAuthor").textContent = language.requiredMsgAuthor;
    document.getElementById("requiredMsgDir").textContent = language.requiredMsgDir;
    document.getElementById("requiredMsgIcon").textContent = language.requiredMsgIcon;
    document.getElementById("textReady").textContent = language.successReady;
    document.getElementById("textSuccessCreate").textContent = language.successCreate;
    document.getElementById("textSuccessAccept").textContent = language.acept;
    let version = document.getElementsByClassName("textVersion")
    let versionText = `${language.version} ${appVersion}`;
    version[0].textContent = versionText;
    version[1].textContent = versionText;
}
function setThemeCbx(theme) {
    let checkbox = document.getElementById('checkboxTheme');
    if (theme == 'dark') {
        checkbox.checked = true;
    } else {
        checkbox.checked = false;
    }

}
function setLangCbx(lang) {
    switch (lang) {
        case 'es':
            let langEs = document.getElementById('lang-es');
            langEs.checked = true;
            break;
        case 'en':
            let langEn = document.getElementById('lang-en');
            langEn.checked = true;
            break;
        case 'fr':
            let langFr = document.getElementById('lang-fr');
            langFr.checked = true;
            break;
        case 'de':
            let langDe = document.getElementById('lang-de');
            langDe.checked = true;
            break;
        case 'it':
            let langIt = document.getElementById('lang-it');
            langIt.checked = true;
            break;
        case 'pt':
            let langPt = document.getElementById('lang-pt');
            langPt.checked = true;
            break;

        default:
            document.getElementById('lang-es').checked = true;
            break;
    }
}
function setThemeMode(mode) {
    theme = mode;
    if (mode == 'ligth') {
        setLightMode();
    } else {
        setDarkMode();
    }
}
function setThemeModeCbx(event) {
    let state = event.target.checked;
    cleanThemeMode();
    if (state) {
        setThemeMode('dark');
    } else {
        setThemeMode('ligth');
    }
}
function cleanThemeMode() {
    let sheet = document.styleSheets[0];
    sheet.deleteRule(0);
}

async function changeLanguage(lang) {
    await setLanguage(lang);
    setLangCbx(lang);
    loadLanguage(language);
    changeIconLang(lang);
}

function changeIconLang(lang) {
    document.getElementById('iconLang').src = `./assets/icons/countries/${lang}.svg`;
}

function setDarkMode() {
    let sheet = document.styleSheets[0];
    sheet.insertRule(` :root {
        --bg-body: #050d28;
        --bg-header: #071e33;
        --bg-tooltip: #32455d;
        --bg-warning: #e62a0f;
        --color-primary: #64ffda;
        --color-secondary: #071e33;
        --color-tertiary: #cccccc;
        --color-neutral: #050d28;
        --color-neutral-secondary: #f7f7f7;
        --color-text: #f7f7f7;
        --color-loop: #050d28;
        --color-darken: #1a1a1a;
        --color-lighten: #32455d;
        --color-close-hover: #e43131;
        --color-minimize-hover: #32455d;
        --color-button-hover: #14cba8;
        --bd-radius: 5px;
        --size-height: 1.7rem;
        --size-icon: 8rem;
      } `);
}
function setLightMode() {
    let sheet = document.styleSheets[0];
    sheet.insertRule(`:root {
        --bg-body: #f7f7f7;
        --bg-header: #d4d4d4;
        --bg-tooltip: #bdbdbd;
        --bg-warning: #f4723f;
        --color-primary: #16b38c;
        --color-secondary: #d4d4d4;
        --color-tertiary: #cccccc;
        --color-neutral: #f7f7f7;
        --color-neutral-secondary: #1a1a1a;
        --color-text: #1a1a1a;
        --color-loop: #f7f7f7;
        --color-darken: #1a1a1a;
        --color-lighten: #32455d;
        --color-close-hover: #d21538;
        --color-minimize-hover: #c5c5c5;
        --color-button-hover: #058a69;
        --bd-radius: 5px;
        --size-height: 1.7rem;
        --size-icon:8rem;
      } `);
}

function stateSettings(state) {
    let settings = document.getElementById("settings");
    let form = document.getElementById("form");
    if (state) {
        settings.style.display = "flex";
        form.style.filter = "blur(1px)";
    } else {
        settings.style.display = "none";
        form.style.filter = "none";
    }
}

function stateInformation(state) {
    let information = document.getElementById("info");
    let form = document.getElementById("form");
    if (state) {
        information.style.display = "flex";
        form.style.filter = "blur(1px)";
    } else {
        information.style.display = "none";
        form.style.filter = "none";
    }
}
    
function warningAnimated(e) {
    let state = e.target.checked;
    if (state) {
        if (animatedIsShow) {
           stateWarningAnimated(true);
        }
    }
}

function stateWarningAnimated(state) {
    let warningAnimated = document.getElementById("warningAnimated");
    let form = document.getElementById("form");
    if (state) {
        warningAnimated.style.display = "flex";
        form.style.filter = "blur(1px)";
    } else {
        warningAnimated.style.display = "none";
        form.style.filter = "none";
    }
}
    
function setShowWarningAnimated() {
    stateWarningAnimated(false);
    let state = document.getElementById('no-show-more').checked;
    if (state) {
        animatedIsShow = false
    }
}

function openFolder(e) {
    e.preventDefault();
    let dir = document.getElementById('textInputFolder').value;
    if (dir != '' && dir != null) {
        pywebview.api.openFolder(dir);
    }
}

function selectFolder(e) {
    e.preventDefault();
    pywebview.api.selectFolder(directory).then((response) => {
        document.getElementById('textInputFolder').value = response;
    });
}

function selectIcon(e) {
    e.preventDefault();
    pywebview.api.selectIcon().then((response) => {
        let iconFile = base64ToFile(response.encode, 'icon', 'png');
        let icon = URL.createObjectURL(iconFile);
        document.getElementById('imageIcon').src = icon;
        document.getElementById('iconDirectory').value = response.dir
    }).catch((error) => {
        console.error(error);
    });
}

function base64ToFile(base64, fileName, fileExtension) {

    let dataurl = `data:image/${fileExtension};base64,${base64}`;
    fileName = `${fileName}.${fileExtension}`;

    let arr = dataurl.split(','),
        mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]),
        n = bstr.length,
        u8arr = new Uint8Array(n);

    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }

    return new File([u8arr], fileName, { type: mime });
}

function openGithub() {
    pywebview.api.openGithub();
}
function openLicense() {
    pywebview.api.openLicense(lang);
}
function openTerms() {
    pywebview.api.openTerms(lang);
}

function getPackageApp() {
    // let stickerMaker = document.getElementById('stickerMaker').checked;
    let wemoji = document.getElementById('wemoji').checked;
    if (wemoji) {
        return 'wemoji';
    } else {
        return 'stickerMaker';
    }
}

function minimizeApp() {
    pywebview.api.minimizeApp();
}
function closeApp() {
    let userPreferences = {
        theme: theme,
        animatedIsShow: animatedIsShow,
        lang: lang,
        directory: directory,
    }
    pywebview.api.closeApp(userPreferences);
}
async function createPack(e) {
    e.preventDefault();
    let validator = validation();
    if (validator) {
        let packageApp = getPackageApp();
        const formData = {
            package: packageApp,
            animated: document.getElementById('animated').checked,
            namepack: document.getElementById('textNamePack').value,
            author: document.getElementById('textNameAuthor').value,
            directory: document.getElementById('textInputFolder').value,
            icon: document.getElementById('iconDirectory').value,
            conserve: document.getElementById('conserveImgs').checked,
        }
        stateAnimationLoop(true);
        await pywebview.api.createPack(formData).then((response) => {
            console.log(response);
            stateAnimationLoop(false);
            stateSuccess(true);
        });
    }
}

function stateAnimationLoop(state) {
    let animation = document.getElementById('animationLoop');
    let form = document.getElementById('form');
    if (state) {
        form.style.filter = "blur(1px)";
        animation.style.display = "flex";
    }
    else {
        form.style.filter = "none";
        animation.style.display = "none";
    }

};

function stateSuccess(state) {
    let success = document.getElementById('success');
    let form = document.getElementById('form');
    if (state) {
        form.style.filter = "blur(1px)";
        success.style.display = "flex";
    }
    else {
        form.style.filter = "none";
        success.style.display = "none";
    }
}

function validation() {
    let validator = true;
    const namePack = document.getElementById("textNamePack");
    if (!namePack.checkValidity() || namePack.value == '') {
        document.getElementById('requiredNamePack').style.display = "flex";
        validator = false;
        return validator;
    } else {
        document.getElementById('requiredNamePack').style.display = "none";
        validator = true;
    }
    const nameAuthor = document.getElementById("textNameAuthor");
    if (!nameAuthor.checkValidity() || nameAuthor.value == '') {
        document.getElementById('requiredAuthor').style.display = "flex";
        validator = false;
        return validator;
    } else {
        document.getElementById('requiredAuthor').style.display = "none";
        validator = true;
    }
    const folder = document.getElementById("textInputFolder");
    if (!folder.checkValidity() || folder.value == '') {
        document.getElementById('requiredDir').style.display = "flex";
        validator = false;
        return validator;
    }
    else {
        document.getElementById('requiredDir').style.display = "none";
        validator = true;
    }
    const icon = document.getElementById("iconDirectory");
    if (!icon.checkValidity() || icon.value == '') {
        document.getElementById('requiredIcon').style.display = "flex";
        validator = false;
        return validator;
    }
    else {
        document.getElementById('requiredIcon').style.display = "none";
        validator = true;
    }
    return validator;
}

function finish(e) {
    stateSuccess(false);
    openFolder(e);
    setTimeout(() => {
        closeApp();
    }, 1000);
}