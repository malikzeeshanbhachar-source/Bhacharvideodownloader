const API_CONFIG = {
  baseUrl: '',
  endpoints: {
    inspect: '/api/videos/info',
    download: '/api/videos/download'
  }
};

const ui = {
  form: document.getElementById('downloadForm'),
  videoUrl: document.getElementById('videoUrl'),
  inspectBtn: document.getElementById('inspectBtn'),
  downloadBtn: document.getElementById('downloadBtn'),
  videoInfo: document.getElementById('videoInfo'),
  formatList: document.getElementById('formatList'),
  progress: document.getElementById('progress'),
  statusMessage: document.getElementById('statusMessage'),
  errorMessage: document.getElementById('errorMessage')
};

function validateInput(url) {
  if (!url || typeof url !== 'string') {
    return false;
  }

  try {
    const parsed = new URL(url.trim());
    return ['http:', 'https:'].includes(parsed.protocol);
  } catch {
    return false;
  }
}

function setStatus(level, message) {
  ui.statusMessage.className = 'status-box';

  if (level === 'success') {
    ui.statusMessage.classList.add('success');
  } else if (level === 'error') {
    ui.statusMessage.classList.add('error');
  } else {
    ui.statusMessage.classList.add('neutral');
  }

  ui.statusMessage.textContent = message;
}

function setError(message) {
  if (!message) {
    ui.errorMessage.textContent = '';
    ui.errorMessage.classList.add('hidden');
    return;
  }

  ui.errorMessage.textContent = message;
  ui.errorMessage.classList.remove('hidden');
}

function setProgress(message) {
  ui.progress.textContent = message;
}

function updateViewState(operation, isRunning) {
  const disabled = Boolean(isRunning);
  const actionButtons = [ui.inspectBtn, ui.downloadBtn];

  actionButtons.forEach((button) => {
    if (!button) {
      return;
    }

    if (operation && button.dataset.action !== operation) {
      button.disabled = disabled;
      return;
    }

    button.disabled = disabled;
  });
}

function resetInfoPanels() {
  ui.videoInfo.textContent = 'No video inspected yet.';
  ui.videoInfo.classList.add('empty-state');
  ui.formatList.innerHTML = '<li class="empty-item">No formats available yet.<\/li>';
}

function renderVideoInfo(videoData) {
  if (!videoData) {
    ui.videoInfo.textContent = 'No video information available.';
    ui.videoInfo.classList.add('empty-state');
    return;
  }

  const rows = [
    ['Title', videoData.title || 'Unknown'],
    ['Uploader', videoData.uploader || 'Unknown'],
    ['URL', videoData.webpage_url || videoData.url || 'Not provided'],
    ['Duration', videoData.duration ?? 'Not provided'],
    ['Extractor', videoData.extractor || 'Unknown']
  ];

  const container = document.createElement('dl');
  container.className = 'video-meta';

  rows.forEach(([label, value]) => {
    const term = document.createElement('dt');
    term.textContent = label;

    const description = document.createElement('dd');
    description.textContent = value;

    container.append(term, description);
  });

  ui.videoInfo.textContent = '';
  ui.videoInfo.classList.remove('empty-state');
  ui.videoInfo.appendChild(container);
}

function renderFormats(formats) {
  const items = Array.isArray(formats) ? formats : [];

  if (!items.length) {
    ui.formatList.innerHTML = '<li class="empty-item">No formats available yet.<\/li>';
    return;
  }

  const listItems = items.map((format) => {
    const item = document.createElement('li');
    item.className = 'format-item';

    const quality = document.createElement('strong');
    quality.textContent = format.resolution || format.ext || format.format_id || 'Unknown quality';

    const details = document.createElement('span');
    const parts = [];
    if (format.ext) parts.push(format.ext);
    if (format.fps) parts.push(`${format.fps}fps`);
    if (format.filesize) parts.push(`${Math.round(format.filesize / 1024)} KB`);
    details.textContent = parts.length ? parts.join(' • ') : 'Format information unavailable';

    item.append(quality, details);
    return item;
  });

  ui.formatList.innerHTML = '';
  listItems.forEach((element) => ui.formatList.appendChild(element));
}

async function inspectVideoInfo() {
  const url = ui.videoUrl.value.trim();

  if (!url) {
    setError('Please enter a URL.');
    setStatus('neutral', 'A URL is required.');
    return;
  }

  if (!validateInput(url)) {
    setError('Please enter a valid http or https URL.');
    setStatus('neutral', 'URL validation failed.');
    return;
  }

  if (!API_CONFIG.baseUrl) {
    updateViewState('inspect', true);
    setProgress('Backend not connected.');
    setStatus('neutral', 'Backend not connected yet.');
    setError('Backend not connected yet.');
    updateViewState('inspect', false);
    return;
  }

  updateViewState('inspect', true);
  setError('');
  setStatus('neutral', 'Connecting to backend for metadata...');
  setProgress('Waiting for backend metadata response.');

  try {
    const response = await fetch(`${API_CONFIG.baseUrl}${API_CONFIG.endpoints.inspect}?url=${encodeURIComponent(url)}`, {
      method: 'GET'
    });

    if (!response.ok) {
      throw new Error('The backend responded with an error while fetching video info.');
    }

    const payload = await response.json();
    if (!payload.success) {
      throw new Error(payload.error?.message || 'Backend returned an error.');
    }

    renderVideoInfo(payload.video || null);
    renderFormats(payload.video?.formats || []);
    setStatus('success', 'Video information loaded successfully.');
    setProgress('Metadata received from the backend.');
    setError('');
  } catch (error) {
    renderVideoInfo(null);
    renderFormats([]);
    setStatus('neutral', 'Backend request failed.');
    setError(error.message || 'Unable to inspect the video right now.');
    setProgress('The backend is not available yet.');
  } finally {
    updateViewState('inspect', false);
  }
}

async function downloadVideo() {
  const url = ui.videoUrl.value.trim();

  if (!url) {
    setError('Please enter a URL before downloading.');
    setStatus('neutral', 'A URL is required.');
    return;
  }

  if (!validateInput(url)) {
    setError('Please enter a valid http or https URL.');
    setStatus('neutral', 'URL validation failed.');
    return;
  }

  if (!API_CONFIG.baseUrl) {
    updateViewState('download', true);
    setProgress('Backend not connected.');
    setStatus('neutral', 'Download is not available yet.');
    setError('Backend not connected yet.');
    updateViewState('download', false);
    return;
  }

  updateViewState('download', true);
  setError('');
  setStatus('neutral', 'Preparing download request...');
  setProgress('Download is intentionally not implemented in Stage 3.');

  try {
    const response = await fetch(`${API_CONFIG.baseUrl}${API_CONFIG.endpoints.download}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url })
    });

    if (!response.ok) {
      throw new Error('The backend rejected the download request.');
    }

    const payload = await response.json();
    if (payload && payload.success === false) {
      setStatus('neutral', 'Download is not available in this stage.');
      setError(payload.error?.message || 'Download is not implemented yet.');
      setProgress('Actual media downloading is intentionally not implemented in Stage 3.');
      return;
    }

    setStatus('neutral', 'Download is not available in this stage.');
    setError('Real download functionality is not yet implemented.');
  } catch (error) {
    setStatus('neutral', 'Download is not available yet.');
    setError(error.message || 'Download is currently unavailable.');
    setProgress('No backend confirmation available yet.');
  } finally {
    updateViewState('download', false);
  }
}

ui.inspectBtn.addEventListener('click', inspectVideoInfo);
ui.downloadBtn.addEventListener('click', downloadVideo);
ui.form.addEventListener('submit', (event) => {
  event.preventDefault();
  inspectVideoInfo();
});

resetInfoPanels();
setStatus('neutral', 'Ready for a URL.');
setError('');
setProgress('No active progress.');
