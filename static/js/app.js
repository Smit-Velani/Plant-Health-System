/* app.js — PlantScan AI Frontend Logic */

const dropZone    = document.getElementById("dropZone");
const fileInput   = document.getElementById("fileInput");
const previewWrap = document.getElementById("previewWrap");
const previewImg  = document.getElementById("previewImg");
const previewName = document.getElementById("previewName");
const previewSize = document.getElementById("previewSize");
const analyseBtn  = document.getElementById("analyseBtn");
const resetBtn    = document.getElementById("resetBtn");
const btnText     = document.getElementById("btnText");
const btnSpinner  = document.getElementById("btnSpinner");
const resultsPanel= document.getElementById("resultsPanel");

let selectedFile = null;

// ── Drag & drop ────────────────────────────────────────────────────────────────
dropZone.addEventListener("dragover",  e => { e.preventDefault(); dropZone.classList.add("drag-over"); });
dropZone.addEventListener("dragleave", () => dropZone.classList.remove("drag-over"));
dropZone.addEventListener("drop", e => {
  e.preventDefault();
  dropZone.classList.remove("drag-over");
  const file = e.dataTransfer.files[0];
  if (file) handleFile(file);
});
fileInput.addEventListener("change", () => { if (fileInput.files[0]) handleFile(fileInput.files[0]); });

// ── Handle file selection ──────────────────────────────────────────────────────
function handleFile(file) {
  if (!["image/jpeg", "image/png"].includes(file.type)) {
    alert("Please upload a JPG or PNG image."); return;
  }
  selectedFile = file;
  const reader = new FileReader();
  reader.onload = e => {
    previewImg.src = e.target.result;
    previewName.textContent = file.name;
    previewSize.textContent = formatSize(file.size);
    dropZone.classList.add("hidden");
    previewWrap.classList.remove("hidden");
    resultsPanel.classList.add("hidden");
  };
  reader.readAsDataURL(file);
}

function formatSize(bytes) {
  if (bytes < 1024)       return bytes + " B";
  if (bytes < 1024*1024)  return (bytes/1024).toFixed(1) + " KB";
  return (bytes/1024/1024).toFixed(1) + " MB";
}

// ── Reset ──────────────────────────────────────────────────────────────────────
resetBtn.addEventListener("click", () => {
  selectedFile = null;
  fileInput.value = "";
  previewWrap.classList.add("hidden");
  dropZone.classList.remove("hidden");
  resultsPanel.classList.add("hidden");
});

// ── Analyse ────────────────────────────────────────────────────────────────────
analyseBtn.addEventListener("click", async () => {
  if (!selectedFile) return;
  setLoading(true);

  const form = new FormData();
  form.append("file", selectedFile);

  try {
    const res  = await fetch("/predict", { method: "POST", body: form });
    const data = await res.json();
    if (data.error) { alert("Error: " + data.error); return; }
    renderResults(data);
  } catch (err) {
    alert("Network error: " + err.message);
  } finally {
    setLoading(false);
  }
});

function setLoading(on) {
  analyseBtn.disabled = on;
  btnText.classList.toggle("hidden", on);
  btnSpinner.classList.toggle("hidden", !on);
}

// ── Render results ─────────────────────────────────────────────────────────────
function renderResults(d) {
  // Status
  const statusMap = { healthy: "✅ Healthy", diseased: "⚠️ Diseased", uncertain: "❓ Uncertain" };
  const card = document.getElementById("resultCard");
  card.className = "result-card " + d.status;

  document.getElementById("resultPlant").textContent   = "🌱 " + d.plant;
  document.getElementById("resultDisease").textContent  = d.disease;
  document.getElementById("resultBadge").textContent    = statusMap[d.status] || d.status;
  document.getElementById("resultBadge").className      = "result-badge " + d.status;

  // Confidence bar
  document.getElementById("confidenceVal").textContent  = d.confidence + "%";
  document.getElementById("confidenceFill").style.width = Math.min(d.confidence, 100) + "%";

  // Info
  document.getElementById("infoSeverity").textContent   = d.severity;
  document.getElementById("infoTreatment").textContent  = d.treatment;
  document.getElementById("infoPrevention").textContent = d.prevention;

  // Features
  const fGrid = document.getElementById("featuresGrid");
  fGrid.innerHTML = "";
  const featLabels = {
    green_coverage  : ["Green Coverage", "%"],
    lesion_coverage : ["Lesion Coverage", "%"],
    brightness      : ["Brightness", "/255"],
    contrast        : ["Contrast", "σ"],
    texture_score   : ["Texture Score", ""],
    edge_density    : ["Edge Density", "%"],
  };
  for (const [key, [label, unit]] of Object.entries(featLabels)) {
    if (d.features[key] !== undefined) {
      fGrid.innerHTML += `
        <div class="feature-item">
          <span class="feature-val">${d.features[key]}${unit}</span>
          <span class="feature-lbl">${label}</span>
        </div>`;
    }
  }

  // Top 5
  const top5 = document.getElementById("top5List");
  top5.innerHTML = "";
  d.top5.forEach((item, i) => {
    top5.innerHTML += `
      <div class="top5-item">
        <span class="top5-rank">${i+1}</span>
        <span class="top5-name" title="${item.class}">${item.class}</span>
        <div class="top5-bar-wrap"><div class="top5-bar" style="width:${item.confidence}%"></div></div>
        <span class="top5-pct">${item.confidence}%</span>
      </div>`;
  });

  // Uploaded image
  document.getElementById("uploadedImg").src = d.image_url;

  // Show results
  resultsPanel.classList.remove("hidden");
  setTimeout(() => resultsPanel.scrollIntoView({ behavior: "smooth", block: "start" }), 100);
}
