const tabs = document.querySelectorAll(".tab");
const panels = document.querySelectorAll(".panel");
const jobsEl = document.querySelector("#jobs");
const jobTemplate = document.querySelector("#jobTemplate");
const transcribePath = document.querySelector('#transcribeForm input[name="path"]');

let pollTimer = null;

function switchTab(id) {
  tabs.forEach((tab) => tab.classList.toggle("active", tab.dataset.tab === id));
  panels.forEach((panel) => panel.classList.toggle("active", panel.id === id));
}

tabs.forEach((tab) => {
  tab.addEventListener("click", () => switchTab(tab.dataset.tab));
});

function statusText(status) {
  return {
    queued: "排队中",
    running: "进行中",
    done: "完成",
    failed: "失败",
  }[status] || status;
}

function fileName(path) {
  return path.split(/[\\/]/).pop() || path;
}

function addFileActions(container, job) {
  job.files.forEach((path) => {
    const link = document.createElement("a");
    link.className = "file-action";
    link.href = `/api/file?path=${encodeURIComponent(path)}`;
    link.textContent = `下载 ${fileName(path)}`;
    container.appendChild(link);

    if (job.kind === "download") {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "file-action";
      button.textContent = "转录这个文件";
      button.addEventListener("click", () => {
        transcribePath.value = path;
        switchTab("transcribePanel");
      });
      container.appendChild(button);
    }
  });
}

function renderJobs(jobs) {
  jobsEl.innerHTML = "";
  if (!jobs.length) {
    const empty = document.createElement("div");
    empty.className = "empty";
    empty.textContent = "还没有任务。";
    jobsEl.appendChild(empty);
    return;
  }

  jobs.forEach((job) => {
    const node = jobTemplate.content.firstElementChild.cloneNode(true);
    node.classList.add(job.status);
    node.querySelector(".job-kind").textContent = job.kind;
    node.querySelector("h3").textContent = job.title;
    node.querySelector(".job-status").textContent = statusText(job.status);
    node.querySelector(".progress span").style.width = `${Math.max(0, Math.min(100, job.progress || 0))}%`;
    node.querySelector(".job-message").textContent = job.error || job.message || "";
    node.querySelector("pre").textContent = (job.logs || []).join("\n");
    addFileActions(node.querySelector(".job-files"), job);
    jobsEl.appendChild(node);
  });
}

async function refreshJobs() {
  const response = await fetch("/api/jobs");
  if (!response.ok) throw new Error("无法读取任务列表");
  const jobs = await response.json();
  renderJobs(jobs);
  const active = jobs.some((job) => ["queued", "running"].includes(job.status));
  if (active && !pollTimer) {
    pollTimer = window.setInterval(refreshJobs, 1500);
  }
  if (!active && pollTimer) {
    window.clearInterval(pollTimer);
    pollTimer = null;
  }
}

async function submitDownload(event) {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  const payload = {
    url: form.get("url"),
    mode: form.get("mode"),
    quality: form.get("quality"),
    cookie_source: form.get("cookie_source"),
    cookie_file: form.get("cookie_file"),
  };
  const response = await fetch("/api/download", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) {
    alert(data.error || "创建下载任务失败");
    return;
  }
  switchTab("jobsPanel");
  await refreshJobs();
}

async function submitOneClickTranscribe() {
  const downloadForm = document.querySelector("#downloadForm");
  if (!downloadForm.reportValidity()) return;

  const form = new FormData(downloadForm);
  const payload = {
    url: form.get("url"),
    cookie_source: form.get("cookie_source"),
    cookie_file: form.get("cookie_file"),
  };
  const response = await fetch("/api/one-click-transcribe", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) {
    alert(data.error || "创建一键转录任务失败");
    return;
  }
  switchTab("jobsPanel");
  await refreshJobs();
}

async function submitTranscribe(event) {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  const elements = event.currentTarget.elements;
  form.set("timestamps", elements.timestamps.checked ? "true" : "false");
  form.set("no_vad", elements.no_vad.checked ? "true" : "false");
  const response = await fetch("/api/transcribe", {
    method: "POST",
    body: form,
  });
  const data = await response.json();
  if (!response.ok) {
    alert(data.error || "创建转录任务失败");
    return;
  }
  switchTab("jobsPanel");
  await refreshJobs();
}

document.querySelector("#downloadForm").addEventListener("submit", submitDownload);
document.querySelector("#oneClickTranscribe").addEventListener("click", submitOneClickTranscribe);
document.querySelector("#transcribeForm").addEventListener("submit", submitTranscribe);
document.querySelector("#refreshJobs").addEventListener("click", refreshJobs);

refreshJobs().catch(() => {
  document.querySelector("#serverStatus").textContent = "本地服务未响应";
});

fetch("/api/health")
  .then((response) => response.json())
  .then((data) => {
    if (data.version) {
      document.querySelector("#serverStatus").textContent = `本地服务 ${data.version}`;
    }
  })
  .catch(() => {});
