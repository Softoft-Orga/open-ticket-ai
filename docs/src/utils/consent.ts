/**
 * Cookie consent management utilities
 *
 * Provides functions to check and manage user consent for cookies and analytics.
 * Works both in browser environments and during SSR.
 */

export const CONSENT_STORAGE_KEY = 'cookie-consent';
export const CONSENT_ACCEPTED = 'accepted';
export const CONSENT_DECLINED = 'declined';

/**
 * Get the current consent status from localStorage
 * @returns The consent status ('accepted', 'declined', or null if not set)
 */
export function getConsent(): string | null {
  if (typeof window === 'undefined') return null;
  try {
    return localStorage.getItem(CONSENT_STORAGE_KEY);
  } catch {
    return null;
  }
}

/**
 * Check if analytics consent has been granted
 * @returns true if user has accepted cookies, false otherwise
 */
export function hasAnalyticsConsent(): boolean {
  return getConsent() === CONSENT_ACCEPTED;
}

/**
 * Set the consent status
 * @param value The consent value to set ('accepted' or 'declined')
 */
export function setConsent(value: string): void {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(CONSENT_STORAGE_KEY, value);
    window.dispatchEvent(
      new CustomEvent('cookie-consent-changed', {
        detail: { consent: value },
      })
    );
  } catch (error) {
    console.error('Failed to save cookie consent:', error);
  }
}

/**
 * Listen for consent changes
 * @param callback Function to call when consent changes
 * @returns Cleanup function to remove the listener
 */
export function onConsentChange(callback: (consent: string) => void): () => void {
  if (typeof window === 'undefined') {
    return () => {};
  }

  const handler = (event: Event) => {
    const customEvent = event as CustomEvent<{ consent: string }>;
    callback(customEvent.detail.consent);
  };

  window.addEventListener('cookie-consent-changed', handler);
  return () => window.removeEventListener('cookie-consent-changed', handler);
}
