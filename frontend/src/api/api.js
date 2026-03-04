const BASE_URL = 'http://127.0.0.1:8000';

async function request(path) {
  const response = await fetch(`${BASE_URL}${path}`);

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json();
}

export function getLatestNews() {
  return request('/news/latest');
}

export function getCategoryNews(category) {
  return request(`/news/category/${encodeURIComponent(category)}`);
}
