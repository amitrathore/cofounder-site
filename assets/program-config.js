window.CofounderProgram = {
  foundingCohortCap: 20,
  enrollmentDeadline: "August 31, 2026",
  giveBackTerms: "Founding members commit to a testimonial, a case-study writeup of their venture, and program feedback."
};

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-cohort-cap]").forEach((node) => {
    node.textContent = window.CofounderProgram.foundingCohortCap;
  });
  document.querySelectorAll("[data-enrollment-deadline]").forEach((node) => {
    node.textContent = window.CofounderProgram.enrollmentDeadline;
  });
  document.querySelectorAll("[data-give-back-terms]").forEach((node) => {
    node.textContent = window.CofounderProgram.giveBackTerms;
  });
});
