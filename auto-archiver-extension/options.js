document.addEventListener("DOMContentLoaded", function () {
  function saveOptions() {
    const endpointUrl = document.getElementById("endpointUrl").value;
    const apiKey = document.getElementById("apiKey").value;
    browser.storage.local.set({ endpointUrl, apiKey });
  }

  function restoreOptions() {
    browser.storage.local.get(["endpointUrl", "apiKey"]).then((result) => {
      document.getElementById("endpointUrl").value = result.endpointUrl || "";
      document.getElementById("apiKey").value = result.apiKey || "";
    });
  }

  document.getElementById("saveButton").addEventListener("click", saveOptions);
  restoreOptions();
});
