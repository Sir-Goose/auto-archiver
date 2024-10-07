function archiveVideo(url) {
  browser.storage.local.get(["endpointUrl", "apiKey"]).then((result) => {
    const endpointUrl = result.endpointUrl || "http://100.81.40.2:5000/archive";
    const apiKey = result.apiKey || "";
    const archiveUrl = `${endpointUrl}?url=${encodeURIComponent(url)}&key=${encodeURIComponent(apiKey)}`;
    fetch(archiveUrl)
      .then((response) => {
        console.log("Video archived successfully");
      })
      .catch((error) => {
        console.error("Error archiving video:", error);
      });
  });
}

function extractVideoUrl(tabUrl) {
  const urlParts = tabUrl.split("?");
  if (urlParts.length > 1) {
    const queryParams = new URLSearchParams(urlParts[1]);
    const videoId = queryParams.get("v");
    if (videoId) {
      return `https://www.youtube.com/watch?v=${videoId}`;
    }
  }
  return null;
}

browser.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (
    changeInfo.status === "complete" &&
    tab.url.includes("youtube.com/watch")
  ) {
    const videoUrl = extractVideoUrl(tab.url);
    if (videoUrl) {
      archiveVideo(videoUrl);
    }
  }
});
