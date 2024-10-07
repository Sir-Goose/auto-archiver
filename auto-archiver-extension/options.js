document.addEventListener("DOMContentLoaded", function () {
  function saveOptions() {
    const endpointUrl = document.getElementById("endpointUrl").value;
    browser.storage.local.set({ endpointUrl });
  }

  function restoreOptions() {
    browser.storage.local.get("endpointUrl").then((result) => {
      document.getElementById("endpointUrl").value = result.endpointUrl || "";
    });
  }

  document.getElementById("saveButton").addEventListener("click", saveOptions);
  restoreOptions();
});
