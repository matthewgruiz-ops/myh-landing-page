(function () {
  const config = window.MYH_GATEWAY_ACCESS || {};
  const storageKey = config.storageKey || 'myh_gateway_access_unlocked';
  const configuredHash = typeof config.hash === 'string' ? config.hash.trim().toLowerCase() : '';
  const hasCrypto = window.crypto && window.crypto.subtle && window.TextEncoder;

  function markUnlocked() {
    document.documentElement.classList.add('access-unlocked');
    document.documentElement.classList.remove('access-locked');
    try { window.sessionStorage.setItem(storageKey, 'true'); } catch (error) {}
  }

  function markLocked() {
    document.documentElement.classList.add('access-locked');
    document.documentElement.classList.remove('access-unlocked');
  }

  function isUnlocked() {
    try { return window.sessionStorage.getItem(storageKey) === 'true'; } catch (error) { return false; }
  }

  async function sha256(value) {
    const buffer = await window.crypto.subtle.digest('SHA-256', new TextEncoder().encode(value));
    return Array.from(new Uint8Array(buffer)).map((byte) => byte.toString(16).padStart(2, '0')).join('');
  }

  function setMessage(form, message, type) {
    const target = form.querySelector('[data-access-message]');
    if (!target) return;
    target.textContent = message;
    target.dataset.state = type || 'neutral';
  }

  async function handleSubmit(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const input = form.querySelector('input[name="access-code"]');
    const value = input ? input.value.trim() : '';

    if (!configuredHash) {
      setMessage(form, 'Access-code validation is not configured in this build. Please request access.', 'error');
      return;
    }

    if (!hasCrypto) {
      setMessage(form, 'This browser cannot validate the access code securely. Please request access.', 'error');
      return;
    }

    const digest = await sha256(value);
    if (digest === configuredHash) {
      markUnlocked();
      setMessage(form, 'Access unlocked for this session.', 'success');
      document.querySelectorAll('[data-gated]').forEach((element) => element.removeAttribute('hidden'));
      document.querySelectorAll('[data-gated-route]').forEach((element) => element.removeAttribute('hidden'));
      document.querySelectorAll('[data-route-gate]').forEach((element) => element.setAttribute('hidden', ''));
      const firstGated = document.querySelector('[data-gated]');
      if (firstGated) firstGated.focus({ preventScroll: false });
    } else {
      markLocked();
      setMessage(form, 'That access code was not recognised. Please check it or request access.', 'error');
    }
  }

  function init() {
    if (isUnlocked()) markUnlocked(); else markLocked();

    document.querySelectorAll('[data-access-form]').forEach((form) => {
      form.addEventListener('submit', handleSubmit);
      if (!configuredHash) setMessage(form, 'Access-code validation has not been configured for this build. Request access to continue.', 'neutral');
    });

    document.querySelectorAll('[data-gated-route]').forEach((route) => {
      if (!isUnlocked()) {
        route.setAttribute('hidden', '');
        const gate = document.querySelector('[data-route-gate]');
        if (gate) gate.removeAttribute('hidden');
      }
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
