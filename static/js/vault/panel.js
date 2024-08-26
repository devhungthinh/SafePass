function togglePanel() {
  const panel = document.getElementById('action-panel');
  panel.classList.toggle('d-none');
  panel.classList.toggle('d-block');
}

// Drag and Drop Functionality
const panel = document.getElementById('action-panel');
const header = document.getElementById('actionPanelHeader');
let offsetX = 0, offsetY = 0, mouseX = 0, mouseY = 0;


function dragMouseDown(e) {
  e.preventDefault();
  mouseX = e.clientX;
  mouseY = e.clientY;
  document.onmousemove = elementDrag;
  document.onmouseup = stopDragging;
}

panel.onmousedown = dragMouseDown;

function elementDrag(e) {
  e.preventDefault();
  offsetX = mouseX - e.clientX;
  offsetY = mouseY - e.clientY;
  mouseX = e.clientX;
  mouseY = e.clientY;
  panel.style.top = (panel.offsetTop - offsetY) + "px";
  panel.style.left = (panel.offsetLeft - offsetX) + "px";
}

function stopDragging() {
  document.onmouseup = null;
  document.onmousemove = null;
}

function toggleVisible(ele) {
  if (ele.classList.contains('content-visible')) {
    ele.classList.remove('content-visible');
    ele.classList.add('content-invisible');
  }

  if (ele.classList.contains('content-invisible')) {
    ele.classList.remove('content-invisible');
    ele.classList.add('content-visible');
  }
}

let selectedVaultCount = 0;
const vaultCountSpan = document.querySelector('div.action-panel-body span');
const selectAllCheckbox = document.querySelector('input#select-all');
const selectCheckboxes = document.querySelectorAll('.row-select');
const closePanel = document.querySelector('button#action-panel-close');

function updateActionPanel() {
  if (selectedVaultCount > 1)
    vaultCountSpan.textContent = `${selectedVaultCount} items selected`;
  else
    vaultCountSpan.textContent = `${selectedVaultCount} item selected`;
}
updateActionPanel();

function showEle(ele) {
  ele.classList.remove('content-invisible');
  ele.classList.add('content-visible');
}

function hideEle(ele) {
  ele.classList.remove('content-visible');
  ele.classList.add('content-invisible');
}

function showPanel() {
  const actionPanel = document.getElementById('action-panel');
  actionPanel.classList.remove('d-none');
  actionPanel.classList.add('d-block');
}

function hidePanel() {
  const actionPanel = document.getElementById('action-panel');
  actionPanel.classList.remove('d-block');
  actionPanel.classList.add('d-none');
}

/* When click the select all checkbox, it will select all existing rows. */
selectAllCheckbox.addEventListener('change', (evt) => {
  const target = evt.target;
  if (target.checked) {
    selectedVaultCount = MAX_VAULT_COUNT;
    showEle(target);
    showPanel();
  } else {
    selectedVaultCount = 0;
    hideEle(target);
    hidePanel();
  }

  selectCheckboxes.forEach((checkbox) => {
    if (target.checked && !checkbox.checked) {
      checkbox.checked = true;
      showEle(checkbox);
    }

    if (!target.checked && checkbox.checked) {
      checkbox.checked = false;
      hideEle(checkbox);
    }
  });
  updateActionPanel();
});

selectCheckboxes.forEach((checkbox) => {
  checkbox.addEventListener('click', (evt) => {
    evt.stopPropagation();
  });

  checkbox.addEventListener('change', (evt) => {
    const target = evt.target;
    if (target.checked) {
      showPanel();
      selectedVaultCount += 1;
      showEle(target);
    } else {
      selectedVaultCount -= 1;
      if (selectedVaultCount == 0) {
        selectAllCheckbox.checked = false;
        hideEle(selectAllCheckbox);
        hidePanel();
      }
      hideEle(target);
    }
    updateActionPanel();
  });
});

document.querySelector('button#select-all-vaults').addEventListener('click', (evt) => {
  if (!selectAllCheckbox.checked) {
    selectAllCheckbox.checked = true;
    showEle(selectAllCheckbox);
    selectCheckboxes.forEach((checkbox) => {
      checkbox.checked = true;
      showEle(checkbox);
    });
  } else {
    selectAllCheckbox.checked = false;
    hideEle(selectAllCheckbox);
    selectCheckboxes.forEach((checkbox) => {
      checkbox.checked = false;
      hideEle(checkbox);
    });
  }
});

document.querySelector('button#action-panel-close').addEventListener('click', (evt) => {
  selectedVaultCount = 0;
  selectAllCheckbox.checked = false;
  hideEle(selectAllCheckbox);
  selectCheckboxes.forEach((checkbox) => {
    checkbox.checked = false;
    hideEle(checkbox);
    togglePanel();
  });
});