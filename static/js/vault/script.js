function copyTextToClipboard({
  'name': name,
  'value': value,
}) {
  navigator.clipboard.writeText(value)
    .then(() => {
      Toast.fire({
        icon: 'success',
        title: 'Copy To Clipboard',
        text: `Copy ${name} to clipboard successfully!`,
      });
    })
    .catch((err) => {
      Toast.fire({
        icon: 'error',
        title: 'Copy To Clipboard',
        text: `Copy ${name} to clipboard failed!`,
      });
    });
}

const searchInput = document.querySelector('input[role="search-input');
if (searchInput) {
  /* Refresh vault search results when clear search input value using Ctrl+Delete. */
  searchInput.addEventListener('keydown', function (evt) {
    if (evt.ctrlKey && evt.key === 'Delete') { // Ctrl+Delete
      evt.preventDefault();
      this.setAttribute('hx-trigger', 'true')
      htmx.trigger(this, 'htmx:trigger');
    }
  });
}


const searchClearBtn = document.getElementById('search-clear');
if (searchClearBtn) {
  searchClearBtn.addEventListener('click', (evt) => {
    const searchInput = document.querySelector('input[role="search-input');
    searchInput.value = "";
    searchInput.setAttribute('hx-trigger', 'true');
    htmx.trigger(searchInput, 'htmx:trigger');
  });
}
