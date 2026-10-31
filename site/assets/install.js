/* Progressive enhancement: the sentence remains selectable without JavaScript. */
document.querySelectorAll('.install-card').forEach((card) => {
  const prompt = card.querySelector('.install-prompt');
  const button = card.querySelector('.copy-install');
  const status = card.querySelector('.copy-status');
  const label = button.textContent;
  let reset;
  button.hidden = false;
  prompt.addEventListener('dragstart', (event) => {
    event.dataTransfer.setData('text/plain', prompt.textContent);
    event.dataTransfer.effectAllowed = 'copy';
  });
  button.addEventListener('click', async () => {
    clearTimeout(reset);
    button.textContent = label;
    status.textContent = '';
    try {
      await navigator.clipboard.writeText(prompt.textContent);
      button.textContent = button.dataset.copied;
      status.textContent = button.dataset.copied;
      reset = setTimeout(() => {
        button.textContent = label;
        status.textContent = '';
      }, 2500);
    } catch {
      prompt.focus();
      const range = document.createRange();
      range.selectNodeContents(prompt);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent = button.dataset.failed;
    }
  });
});
