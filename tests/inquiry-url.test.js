import test from 'node:test';
import assert from 'node:assert/strict';
import { inquiryUrl } from '../src/inquiry-url.js';

test('uses the same-origin API when no backend URL is configured', () => {
  assert.equal(inquiryUrl(), '/api/training-inquiry');
  assert.equal(inquiryUrl('  '), '/api/training-inquiry');
});

test('targets the configured backend without duplicating slashes', () => {
  assert.equal(inquiryUrl('https://backend.example.com/'), 'https://backend.example.com/api/training-inquiry');
  assert.equal(inquiryUrl(' https://backend.example.com '), 'https://backend.example.com/api/training-inquiry');
});

test('rejects invalid, unsafe or path-bearing backend settings', () => {
  for (const base of ['example.com', 'javascript:alert(1)', 'https://example.com/path', 'https://user:pass@example.com', 'https://example.com/?q=1']) {
    assert.throws(() => inquiryUrl(base));
  }
});
