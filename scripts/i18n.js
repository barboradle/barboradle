// Detect the browser language or fallback to default
const urlParamsI18n = new URLSearchParams(window.location.search);
const lang = urlParamsI18n.get('lang');

const defaultLang = lang || 'lt';
const userLang = navigator.language.substring(0, 2) || defaultLang;


let cacheTranslations;

fetchData().then(data => {
  cacheTranslations = data;
  applyTranslations(cacheTranslations);
});

// Apply translations to elements with the data-i18n attribute
function applyTranslations(translations) {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const translationKey = el.getAttribute('data-i18n');
    let translatedText = translations[translationKey] || el.innerText;

    // Apply the translated text to the element
    if (el.tagName.toLowerCase() === 'title') {
      document.title = translatedText;  // For <title> tag
    } else {
      el.innerText = translatedText.replace('&lt;', '<').replace('&gt;', '>');  // For other tags
    }

    enter_a_guess = getTranslation("game_enter_a_guess");
    input.setAttribute("placeholder", `${enter_a_guess}`);
  });
}

function getTranslation(key) {
    if (cacheTranslations == undefined) {
      return undefined;
    }
    return cacheTranslations[key];
}

// Load translation JSON based on the selected language
async function fetchData() {
  try {
    const response = await fetch(`i18n/${userLang}.json`, { method: "GET", mode: 'cors', headers: { 'Content-Type': 'application/json'}});
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}
