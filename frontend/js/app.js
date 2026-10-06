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
  const pattern = /^(https?:\/\/)?(www\.)?(tiktok\.com)(\/.*)?$/i;
  return pattern.test(url.trim());
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

function showBackendNotConnected(operationName) {
  const message = `Backend not connected yet. The ${operationName} endpoint is not available until the backend is implemented.`;

  setProgress('Waiting for backend connectivity.');
  setStatus('neutral', 'Backend not connected yet.');
  setError('Backend not connected yet.');
  ui.videoInfo.textContent = message;
  ui.videoInfo.classList.remove('empty-state');
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
    ['Author', videoData.author || 'Unknown'],
    ['URL', videoData.url || 'Not provided'],
    ['Duration', videoData.duration || 'Not provided'],
    ['Status', videoData.status || 'Ready']
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
  const items = Array.isArray(formats) && formats.length ? formats : [];

  if (!items.length) {
    ui.formatList.innerHTML = '<li class="empty-item">No formats available yet.<\/li>';
    return;
  }

  const listItems = items.map((format) => {
    const item = document.createElement('li');
    item.className = 'format-item';

    const quality = document.createElement('strong');
    quality.textContent = format.quality || 'Unknown quality';

    const details = document.createElement('span');
    details.textContent = format.label || format.type || 'Format information unavailable';

    item.append(quality, details);
    return item;
  });

  ui.formatList.innerHTML = '';
  listItems.forEach((element) => ui.formatList.appendChild(element));
}

async function inspectVideoInfo() {
  const url = ui.videoUrl.value.trim();

  if (!url) {
    setError('Please enter a TikTok URL.');
    setStatus('neutral', 'A URL is required.');
    return;
  }

  if (!validateInput(url)) {
    setError('Please enter a valid TikTok URL.');
    setStatus('neutral', 'URL validation failed.');
    return;
  }

  if (!API_CONFIG.baseUrl) {
    updateViewState('inspect', true);
    showBackendNotConnected('inspect');
    updateViewState('inspect', false);
    return;
  }

  updateViewState('inspect', true);
  setError('');
  setStatus('neutral', 'Connecting to backend for metadata...');
  setProgress('Waiting for backend metadata response.');

  try {
    const response = await fetch(`${API_CONFIG.baseUrl}${API_CONFIG.endpoints.inspect}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url })
    });

    if (!response.ok) {
      throw new Error('The backend responded with an error while fetching video info.');
    }

    const payload = await response.json();
    renderVideoInfo(payload.video || payload);
    renderFormats(payload.formats || []);
    setStatus('success', 'Video information loaded successfully.');
    setProgress('Metadata received from the backend.');
    setError('');
  } catch (error) {
    renderVideoInfo(null);
    renderFormats([]);
    setStatus('neutral', 'Backend not connected yet.');
    setError(error.message || 'Unable to inspect the video right now.');
    setProgress('The backend is not available yet.');
  } finally {
    updateViewState('inspect', false);
  }
}

async function downloadVideo() {
  const url = ui.videoUrl.value.trim();

  if (!url) {
    setError('Please enter a TikTok URL before downloading.');
    setStatus('neutral', 'A URL is required.');
    return;
  }

  if (!validateInput(url)) {
    setError('Please enter a valid TikTok URL.');
    setStatus('neutral', 'URL validation failed.');
    return;
  }

  if (!API_CONFIG.baseUrl) {
    updateViewState('download', true);
    showBackendNotConnected('download');
    updateViewState('download', false);
    return;
  }

  updateViewState('download', true);
  setError('');
  setStatus('neutral', 'Preparing download request...');
  setProgress('Waiting for backend confirmation before starting a download.');

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

    if (!payload || payload.status !== 'ready') {
      throw new Error('The backend did not confirm a valid download.');
    }

    setStatus('success', 'Download request accepted by the backend.');
    setProgress('The backend confirmed readiness. Real download handling will occur after backend implementation.');
    setError('');
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
setStatus('neutral', 'Ready for a TikTok URL.');
setError('');
setProgress('No active progress. Progress will appear when the future backend is connected.');