document.addEventListener("DOMContentLoaded", () => {
  const burgerBtn = document.getElementById("burgerBtn");
  const overlayMenu = document.getElementById("overlayMenu");

  burgerBtn.addEventListener("click", () => {
    burgerBtn.classList.toggle("open");
    overlayMenu.classList.toggle("open");
  });
});


// Optional: Time updating
function updateTime() {
  const options = {
    timeZone: "Asia/Tokyo",
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  };

  const formatter = new Intl.DateTimeFormat("en-US", options);
  const japanTime = formatter.format(new Date());

  const timeEl = document.getElementById("current-time");
  if (timeEl) timeEl.textContent = japanTime;
}

updateTime();
setInterval(updateTime, 60000);
