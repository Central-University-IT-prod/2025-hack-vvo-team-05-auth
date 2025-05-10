document.addEventListener("DOMContentLoaded", () => {
  const burgerBtn = document.getElementById("burgerBtn");
  const overlayMenu = document.getElementById("overlayMenu");
  const spans = burgerBtn.querySelectorAll("span");

  // Create icon wrapper
  const iconWrapper = document.createElement("div");
  iconWrapper.classList.add("icon");

  // Move spans to icon wrapper
  spans.forEach((span, i) => {
    if (i < 3) iconWrapper.appendChild(span);
  });

  // Insert icon wrapper before any existing content
  burgerBtn.insertBefore(iconWrapper, burgerBtn.firstChild);

  // Toggle menu
  burgerBtn.addEventListener("click", (e) => {
    e.preventDefault();
    burgerBtn.classList.toggle("open");
    overlayMenu.classList.toggle("open");
    document.body.style.overflow = overlayMenu.classList.contains("open") ? "hidden" : "";
  });
}); 