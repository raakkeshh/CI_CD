/**
 * CloudBuild Pro - Enterprise CI/CD Pipeline & DevOps Dashboard JavaScript
 * Handles:
 * 1. Theme Management (Dark / Light toggle with localStorage)
 * 2. Chart.js Dashboard Visualizations
 * 3. Interactive Manual Approval Gate state machine
 * 4. Interactive 9-Step Pipeline Runner & Step Inspector
 * 5. Build History Table filtering, live search & pagination
 * 6. Build Log Modal viewer
 * 7. Toast Notifications
 */

document.addEventListener('DOMContentLoaded', () => {
  initThemeToggle();
  initCharts();
  initApprovalGate();
  initPipelineInteractions();
  initBuildHistory();
  initTooltips();
});

/* ==========================================================================
   1. Theme Management
   ========================================================================== */
function initThemeToggle() {
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const themeIcon = document.getElementById('themeIcon');
  if (!themeToggleBtn) return;

  const savedTheme = localStorage.getItem('cloudbuild_theme') || 'dark';
  applyTheme(savedTheme);

  themeToggleBtn.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
    localStorage.setItem('cloudbuild_theme', newTheme);
    showToast('Theme Updated', `Switched to ${newTheme.toUpperCase()} enterprise mode.`, 'info');
  });

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    if (themeIcon) {
      if (theme === 'light') {
        themeIcon.className = 'fa-solid fa-moon text-primary';
      } else {
        themeIcon.className = 'fa-solid fa-sun text-warning';
      }
    }
  }
}

/* ==========================================================================
   2. Chart.js Visualizations
   ========================================================================== */
function initCharts() {
  const isDarkMode = document.documentElement.getAttribute('data-theme') !== 'light';
  const textColor = isDarkMode ? '#9ca3af' : '#4b5563';
  const gridColor = isDarkMode ? 'rgba(255, 255, 255, 0.06)' : 'rgba(0, 0, 0, 0.06)';

  // Chart 1: Weekly Build Chart
  const weeklyCtx = document.getElementById('weeklyBuildChart');
  if (weeklyCtx) {
    new Chart(weeklyCtx, {
      type: 'bar',
      data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [
          {
            label: 'Successful Builds',
            data: [28, 34, 42, 38, 45, 18, 14],
            backgroundColor: 'rgba(52, 168, 83, 0.85)',
            borderRadius: 6
          },
          {
            label: 'Failed Builds',
            data: [2, 1, 3, 0, 2, 0, 1],
            backgroundColor: 'rgba(234, 67, 53, 0.85)',
            borderRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { color: textColor, font: { weight: 600 } } }
        },
        scales: {
          x: { stacked: true, grid: { color: gridColor }, ticks: { color: textColor } },
          y: { stacked: true, grid: { color: gridColor }, ticks: { color: textColor } }
        }
      }
    });
  }

  // Chart 2: Deployment Trend
  const deployCtx = document.getElementById('deploymentTrendChart');
  if (deployCtx) {
    new Chart(deployCtx, {
      type: 'line',
      data: {
        labels: ['Oct 4', 'Oct 5', 'Oct 6', 'Oct 7', 'Oct 8', 'Oct 9', 'Oct 10'],
        datasets: [
          {
            label: 'Staging Deployments',
            data: [8, 12, 14, 11, 16, 13, 10],
            borderColor: '#4285F4',
            backgroundColor: 'rgba(66, 133, 244, 0.15)',
            fill: true,
            tension: 0.35,
            borderWidth: 2.5
          },
          {
            label: 'Production Rollouts',
            data: [3, 4, 5, 2, 6, 4, 4],
            borderColor: '#34A853',
            backgroundColor: 'rgba(52, 168, 83, 0.15)',
            fill: true,
            tension: 0.35,
            borderWidth: 2.5
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { color: textColor, font: { weight: 600 } } }
        },
        scales: {
          x: { grid: { color: gridColor }, ticks: { color: textColor } },
          y: { grid: { color: gridColor }, ticks: { color: textColor } }
        }
      }
    });
  }

  // Chart 3: Build Success Pie Chart
  const pieCtx = document.getElementById('buildSuccessPieChart');
  if (pieCtx) {
    new Chart(pieCtx, {
      type: 'doughnut',
      data: {
        labels: ['Success (93.8%)', 'Failed (3.2%)', 'Cancelled (2.1%)', 'Timeout (0.9%)'],
        datasets: [{
          data: [215, 7, 5, 2],
          backgroundColor: [
            '#34A853', // Green
            '#EA4335', // Red
            '#9ca3af', // Grey
            '#FBBC05'  // Amber
          ],
          borderWidth: 0,
          hoverOffset: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom', labels: { color: textColor, padding: 14 } }
        },
        cutout: '72%'
      }
    });
  }

  // Chart 4: Approval Statistics
  const approvalCtx = document.getElementById('approvalStatsChart');
  if (approvalCtx) {
    new Chart(approvalCtx, {
      type: 'bar',
      data: {
        labels: ['Prod API', 'Prod Web', 'Worker Service', 'Auth Service', 'Gateway'],
        datasets: [
          {
            label: 'Approved by Manager',
            data: [32, 28, 19, 24, 15],
            backgroundColor: '#4285F4',
            borderRadius: 6
          },
          {
            label: 'Rejected',
            data: [2, 1, 0, 3, 1],
            backgroundColor: '#EA4335',
            borderRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: 'y',
        plugins: {
          legend: { position: 'top', labels: { color: textColor } }
        },
        scales: {
          x: { grid: { color: gridColor }, ticks: { color: textColor } },
          y: { grid: { color: gridColor }, ticks: { color: textColor } }
        }
      }
    });
  }
}

/* ==========================================================================
   3. Interactive Approval Gate
   ========================================================================== */
function initApprovalGate() {
  const approveBtns = document.querySelectorAll('.btn-approve-gate');
  const rejectBtns = document.querySelectorAll('.btn-reject-gate');
  const gateStatusBadges = document.querySelectorAll('.gate-status-text');
  const gateBanners = document.querySelectorAll('.approval-gate-banner');
  const deployStatusBadges = document.querySelectorAll('.deploy-status-text');

  approveBtns.forEach(btn => {
    btn.addEventListener('click', async () => {
      // Step 1: Change to Approved
      updateGateUI('Approved', 'Deployment Started...', 'approved');
      showToast('Approval Granted', 'Manager signed off. Initiating Cloud Run deployment...', 'success');

      // Call API asynchronously
      try {
        await fetch('/api/pipeline/approve', { method: 'POST' });
      } catch (e) {
        console.warn('Simulated offline mode for approve API');
      }

      // Step 2: Simulate deployment progress in UI
      setTimeout(() => {
        updateDeployUI('Routing 100% Traffic to Cloud Run Revision');
      }, 1200);

      // Step 3: Complete deployment
      setTimeout(() => {
        updateGateUI('Approved', 'Deployment Completed', 'approved');
        updateDeployUI('Deployment Completed (Revision Active)');
        showToast('Production Live', 'Cloud Run service is now live and healthy at 100% traffic.', 'success');
        
        // Also update stage 7, 8, 9 if on pipeline page
        markPipelineStageDone(7);
        markPipelineStageDone(8);
        markPipelineStageDone(9);
      }, 2500);
    });
  });

  rejectBtns.forEach(btn => {
    btn.addEventListener('click', async () => {
      updateGateUI('Rejected', 'Deployment Cancelled', 'rejected');
      updateDeployUI('Deployment Cancelled (Safety Rollback)');
      showToast('Deployment Rejected', 'Manager rejected release. Deployment safely cancelled.', 'danger');

      try {
        await fetch('/api/pipeline/reject', { method: 'POST' });
      } catch (e) {
        console.warn('Simulated offline mode for reject API');
      }

      markPipelineStageRejected(7);
    });
  });

  function updateGateUI(statusText, deployText, bannerClass) {
    gateStatusBadges.forEach(el => {
      el.textContent = statusText;
      el.className = `badge ${statusText === 'Approved' ? 'bg-success' : 'bg-danger'} gate-status-text`;
    });

    gateBanners.forEach(banner => {
      banner.classList.remove('approved', 'rejected');
      if (bannerClass) banner.classList.add(bannerClass);
    });

    // Disable action buttons once resolved
    approveBtns.forEach(b => b.disabled = true);
    rejectBtns.forEach(b => b.disabled = true);
  }

  function updateDeployUI(deployText) {
    deployStatusBadges.forEach(el => {
      el.textContent = deployText;
    });
  }
}

function markPipelineStageDone(stageId) {
  const node = document.querySelector(`.pipeline-node[data-stage-id="${stageId}"]`);
  if (!node) return;
  node.classList.remove('active-stage', 'pending-stage');
  node.classList.add('completed-stage');
  const badge = node.querySelector('.stage-status-badge');
  if (badge) {
    badge.className = 'stage-status-badge badge-completed';
    badge.textContent = 'COMPLETED';
  }
}

function markPipelineStageRejected(stageId) {
  const node = document.querySelector(`.pipeline-node[data-stage-id="${stageId}"]`);
  if (!node) return;
  node.classList.remove('active-stage', 'completed-stage');
  node.classList.add('active-stage');
  const badge = node.querySelector('.stage-status-badge');
  if (badge) {
    badge.className = 'stage-status-badge badge-failed';
    badge.textContent = 'REJECTED';
  }
}

/* ==========================================================================
   4. Pipeline Page Interactions & Simulation Runner
   ========================================================================== */
function initPipelineInteractions() {
  const nodes = document.querySelectorAll('.pipeline-node');
  const detailModal = document.getElementById('stageDetailModal');
  const modalObj = detailModal ? new bootstrap.Modal(detailModal) : null;
  const runSimBtn = document.getElementById('runPipelineSimulationBtn');

  // Clicking any step opens realistic details
  nodes.forEach(node => {
    node.addEventListener('click', () => {
      const stageName = node.getAttribute('data-stage-name');
      const stageGcp = node.getAttribute('data-stage-gcp');
      const stageDesc = node.getAttribute('data-stage-desc');
      const stageDuration = node.getAttribute('data-stage-duration');
      const stageStatus = node.getAttribute('data-stage-status');
      const stageLogs = node.getAttribute('data-stage-logs');

      // Populate Modal
      document.getElementById('modalStageName').textContent = stageName;
      document.getElementById('modalStageGcp').textContent = stageGcp;
      document.getElementById('modalStageDesc').textContent = stageDesc;
      document.getElementById('modalStageDuration').textContent = stageDuration;
      document.getElementById('modalStageStatus').textContent = stageStatus;
      
      const logsContainer = document.getElementById('modalStageLogs');
      if (logsContainer) {
        logsContainer.textContent = stageLogs || `[INFO] Initializing ${stageName}...\n[SUCCESS] Completed in ${stageDuration}\n[AUDIT] Authenticated via Google Service Account`;
      }

      if (modalObj) modalObj.show();
    });
  });

  // Run Pipeline Simulation button
  if (runSimBtn) {
    runSimBtn.addEventListener('click', async () => {
      runSimBtn.disabled = true;
      runSimBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Simulating Pipeline...';
      showToast('Pipeline Triggered', 'Cloud Build trigger started in us-central1 (private worker pool)...', 'info');

      // Reset all nodes
      nodes.forEach((n, idx) => {
        n.classList.remove('completed-stage', 'active-stage');
        n.classList.add('pending-stage');
        const badge = n.querySelector('.stage-status-badge');
        if (badge) {
          badge.className = 'stage-status-badge badge-pending';
          badge.textContent = 'PENDING';
        }
      });

      // Step sequentially from 1 to 6
      for (let i = 1; i <= 6; i++) {
        await simulateStep(i);
      }

      // Step 7: Manual Approval Gate waiting
      const gateNode = document.querySelector('.pipeline-node[data-stage-id="7"]');
      if (gateNode) {
        gateNode.classList.remove('pending-stage');
        gateNode.classList.add('active-stage');
        const badge = gateNode.querySelector('.stage-status-badge');
        if (badge) {
          badge.className = 'stage-status-badge badge-waiting';
          badge.textContent = 'WAITING APPROVAL';
        }
      }

      showToast('Approval Gate Reached', 'Pipeline paused. Manager authorization required for Cloud Run production release.', 'warning');
      runSimBtn.disabled = false;
      runSimBtn.innerHTML = '<i class="fa-solid fa-play me-2"></i>Run Pipeline Simulation';

      // Re-enable approve/reject buttons
      document.querySelectorAll('.btn-approve-gate').forEach(b => b.disabled = false);
      document.querySelectorAll('.btn-reject-gate').forEach(b => b.disabled = false);
    });
  }

  function simulateStep(stepNumber) {
    return new Promise(resolve => {
      const node = document.querySelector(`.pipeline-node[data-stage-id="${stepNumber}"]`);
      if (!node) {
        resolve();
        return;
      }

      node.classList.remove('pending-stage');
      node.classList.add('active-stage');
      const badge = node.querySelector('.stage-status-badge');
      if (badge) {
        badge.className = 'stage-status-badge badge-running';
        badge.textContent = 'RUNNING';
      }

      setTimeout(() => {
        node.classList.remove('active-stage');
        node.classList.add('completed-stage');
        if (badge) {
          badge.className = 'stage-status-badge badge-completed';
          badge.textContent = 'COMPLETED';
        }
        resolve();
      }, 700);
    });
  }
}

/* ==========================================================================
   5. Build History Table Filtering, Live Search & Pagination
   ========================================================================== */
function initBuildHistory() {
  const searchInput = document.getElementById('buildSearchInput');
  const envFilter = document.getElementById('envFilterSelect');
  const statusFilter = document.getElementById('statusFilterSelect');
  const tableRows = document.querySelectorAll('.build-history-row');
  const recordCountBadge = document.getElementById('recordCountBadge');
  const logModalEl = document.getElementById('buildLogModal');
  const logModal = logModalEl ? new bootstrap.Modal(logModalEl) : null;

  function filterRows() {
    const q = (searchInput?.value || '').toLowerCase().trim();
    const env = (envFilter?.value || 'all').toLowerCase();
    const status = (statusFilter?.value || 'all').toLowerCase();
    let visibleCount = 0;

    tableRows.forEach(row => {
      const rowId = (row.getAttribute('data-build-id') || '').toLowerCase();
      const rowCommit = (row.getAttribute('data-commit') || '').toLowerCase();
      const rowDev = (row.getAttribute('data-dev') || '').toLowerCase();
      const rowEnv = (row.getAttribute('data-env') || '').toLowerCase();
      const rowStatus = (row.getAttribute('data-status') || '').toLowerCase();
      const rowMsg = (row.getAttribute('data-msg') || '').toLowerCase();

      const matchesSearch = !q || rowId.includes(q) || rowCommit.includes(q) || rowDev.includes(q) || rowMsg.includes(q);
      const matchesEnv = env === 'all' || rowEnv === env;
      const matchesStatus = status === 'all' || rowStatus === status;

      if (matchesSearch && matchesEnv && matchesStatus) {
        row.style.display = '';
        visibleCount++;
      } else {
        row.style.display = 'none';
      }
    });

    if (recordCountBadge) {
      recordCountBadge.textContent = `${visibleCount} records`;
    }
  }

  if (searchInput) searchInput.addEventListener('input', filterRows);
  if (envFilter) envFilter.addEventListener('change', filterRows);
  if (statusFilter) statusFilter.addEventListener('change', filterRows);

  // View Log Modal Handler
  document.querySelectorAll('.btn-view-logs').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const row = btn.closest('.build-history-row');
      if (!row) return;

      const buildId = row.getAttribute('data-build-id');
      const commit = row.getAttribute('data-commit');
      const env = row.getAttribute('data-env');
      const status = row.getAttribute('data-status');
      const logsRaw = row.getAttribute('data-logs');

      document.getElementById('logModalBuildId').textContent = buildId;
      document.getElementById('logModalCommit').textContent = commit;
      document.getElementById('logModalEnv').textContent = env;
      document.getElementById('logModalStatus').textContent = status;

      const terminalEl = document.getElementById('logModalTerminalContent');
      if (terminalEl) {
        if (logsRaw) {
          try {
            const logsArray = JSON.parse(logsRaw);
            terminalEl.innerHTML = logsArray.map(l => `<div><span class="log-timestamp">[${new Date().toLocaleTimeString()}]</span> ${escapeHtml(l)}</div>`).join('');
          } catch {
            terminalEl.textContent = logsRaw;
          }
        } else {
          terminalEl.textContent = `[INFO] Build ${buildId} completed successfully on Cloud Build private worker pool.`;
        }
      }

      if (logModal) logModal.show();
    });
  });
}

/* ==========================================================================
   6. Toast Notifications Helper
   ========================================================================== */
function showToast(title, message, type = 'info') {
  const toastContainer = document.getElementById('toastContainer');
  if (!toastContainer) return;

  const bgClass = type === 'success' ? 'border-success' : type === 'danger' ? 'border-danger' : type === 'warning' ? 'border-warning' : 'border-primary';
  const iconClass = type === 'success' ? 'fa-circle-check text-success' : type === 'danger' ? 'fa-triangle-exclamation text-danger' : type === 'warning' ? 'fa-shield-halved text-warning' : 'fa-circle-info text-primary';

  const toastEl = document.createElement('div');
  toastEl.className = `toast align-items-center gcp-card ${bgClass} border-1 text-white`;
  toastEl.setAttribute('role', 'alert');
  toastEl.setAttribute('aria-live', 'assertive');
  toastEl.setAttribute('aria-atomic', 'true');
  toastEl.innerHTML = `
    <div class="toast-header bg-transparent border-bottom-0 text-white pb-1">
      <i class="fa-solid ${iconClass} me-2"></i>
      <strong class="me-auto text-white">${escapeHtml(title)}</strong>
      <small class="text-muted">just now</small>
      <button type="button" class="btn-close btn-close-white ms-2" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast-body pt-0 text-secondary">
      ${escapeHtml(message)}
    </div>
  `;

  toastContainer.appendChild(toastEl);
  const toast = new bootstrap.Toast(toastEl, { delay: 4000 });
  toast.show();
  toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
}

/* ==========================================================================
   7. Utilities & Tooltips
   ========================================================================== */
function initTooltips() {
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(el => new bootstrap.Tooltip(el));
}

function copyToClipboard(text, msg = 'Copied to clipboard!') {
  navigator.clipboard.writeText(text).then(() => {
    showToast('Copied', msg, 'info');
  }).catch(() => {
    showToast('Copy Error', text, 'warning');
  });
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
