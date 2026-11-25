// ========================================
// MOBILE MENU
// ========================================

const menuButton = document.getElementById("menuButton");
const mainNav = document.getElementById("mainNav");

if (menuButton && mainNav) {

    function openMenu() {
        mainNav.classList.add("is-open");
        menuButton.classList.add("is-active");

        menuButton.setAttribute("aria-expanded", "true");
        menuButton.setAttribute("aria-label", "بستن منو");

        document.body.classList.add("menu-open");
    }

    function closeMenu() {
        mainNav.classList.remove("is-open");
        menuButton.classList.remove("is-active");

        menuButton.setAttribute("aria-expanded", "false");
        menuButton.setAttribute("aria-label", "باز کردن منو");

        document.body.classList.remove("menu-open");
    }

    menuButton.addEventListener("click", function () {

        const isOpen = mainNav.classList.contains("is-open");

        if (isOpen) {
            closeMenu();
        } else {
            openMenu();
        }

    });

    const navLinks = mainNav.querySelectorAll("a");

    navLinks.forEach(function (link) {

        link.addEventListener("click", closeMenu);

    });

    document.addEventListener("click", function (event) {

        const clickedInsideNav = mainNav.contains(event.target);
        const clickedMenuButton = menuButton.contains(event.target);

        if (!clickedInsideNav && !clickedMenuButton) {
            closeMenu();
        }

    });

    document.addEventListener("keydown", function (event) {

        if (event.key === "Escape") {
            closeMenu();
        }

    });

    window.addEventListener("resize", function () {

        if (window.innerWidth > 768) {
            closeMenu();
        }

    });

}


// ========================================
// SCROLL REVEAL ANIMATION
// ========================================

const revealElements = document.querySelectorAll(
    ".about-section, .categories-section, .featured-products, .product-card, .category-card, .about-card"
);

if ("IntersectionObserver" in window) {

    const observer = new IntersectionObserver(

        function (entries, observer) {

            entries.forEach(function (entry) {

                if (entry.isIntersecting) {

                    entry.target.classList.add("is-visible");

                    observer.unobserve(entry.target);

                }

            });

        },

        {
            threshold: 0.12,
            rootMargin: "0px 0px -40px 0px"
        }

    );

    revealElements.forEach(function (element) {

        element.classList.add("reveal");

        observer.observe(element);

    });

} else {

    revealElements.forEach(function (element) {

        element.classList.add("is-visible");

    });

}