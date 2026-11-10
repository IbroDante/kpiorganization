// A static frontend can point at the separately deployed Flask service.
// Without an override, keep the existing same-origin/proxy behavior.
export function inquiryUrl(baseUrl = '') {
  const base = baseUrl.trim();
  if (!base) return '/api/training-inquiry';
  const url = new URL(base);
  if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password ||
      (url.pathname !== '/' && url.pathname !== '') || url.search || url.hash) {
    throw new Error('VITE_API_BASE_URL must be an HTTP(S) origin without a path.');
  }
  return `${url.origin}/api/training-inquiry`;
}
