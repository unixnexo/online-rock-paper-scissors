history.replaceState({}, '', '/');

/**
 * theme from local storage
 */
const themeColor = localStorage.getItem('theme-color') || 'pussy-theme';
document.body.classList.add(themeColor);

/**
 * theme switcher
 */
const toggleTheme = (theme) => {

  const body = document.body;
  const themes = ['pussy-theme', 'blue-theme', 'green-theme'];

  if (!body.classList.contains(theme)) {
    body.classList.remove(...themes);
    body.classList.add(theme);
    localStorage.setItem('theme-color', theme);
  }

}


/**
 * copy to clipboard
 */
const copyText = document.getElementById('room-name').innerText;

document.getElementById('copy-ic').addEventListener('click', () => copyToClipboard(copyText))

const showCopied = () => {
  const el = document.getElementById('img-con');
    el.classList.add('copied');
    setTimeout(() => {
      el.classList.remove('copied');
    }, 2000);
}

// main functionality - cross browser
function copyToClipboard(string) {
  let textarea;
  let result;

  try {
    textarea = document.createElement('textarea');
    textarea.setAttribute('readonly', true);
    textarea.setAttribute('contenteditable', true);
    textarea.style.position = 'fixed';
    textarea.value = string;

    document.body.appendChild(textarea);

    textarea.focus();
    textarea.select();

    const range = document.createRange();
    range.selectNodeContents(textarea);

    const sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);

    textarea.setSelectionRange(0, textarea.value.length);
    result = document.execCommand('copy');
  } catch (err) {
    console.error(err);
    result = null;
  } finally {
    document.body.removeChild(textarea);
  }

  // manual copy fallback using prompt
  if (!result) {
    const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
    const copyHotkey = isMac ? '⌘C' : 'CTRL+C';
    result = prompt(`Press ${copyHotkey}`, string);
    if (!result) {
      return false;
    }
  }

  showCopied();
  return true;
}

