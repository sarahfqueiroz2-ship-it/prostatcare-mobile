function showTab(name, el) {
  document.querySelectorAll('.tab').forEach(function (t) { t.classList.remove('active'); });
  document.querySelectorAll('.tab-panel').forEach(function (p) { p.classList.remove('active'); });
  el.classList.add('active');
  document.getElementById('panel-' + name).classList.add('active');
}
