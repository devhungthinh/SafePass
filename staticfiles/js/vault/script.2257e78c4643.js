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

/* Refresh vault search results when clear search input value using Ctrl+Delete. */
document.querySelector('input[role="search-input').addEventListener('keydown', function (evt) {
  if (evt.ctrlKey && evt.key === 'Delete') { // Ctrl+Delete
    evt.preventDefault();
    this.setAttribute('hx-trigger', 'true')
    htmx.trigger(this, 'htmx:trigger');
  }
});

document.getElementById('search-clear').addEventListener('click', (evt) => {
  const searchInput = document.querySelector('input[role="search-input');
  searchInput.value = "";
  searchInput.setAttribute('hx-trigger', 'true');
  htmx.trigger(searchInput, 'htmx:trigger');
});
