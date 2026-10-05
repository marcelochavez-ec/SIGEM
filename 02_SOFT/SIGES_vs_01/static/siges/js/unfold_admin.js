(function () {
    document.title = "SIGES";

    try {
        localStorage.setItem("adminTheme", JSON.stringify("light"));
    } catch (error) {
        return;
    }

    document.documentElement.classList.remove("dark");
    document.documentElement.classList.add("light");

    document.addEventListener("DOMContentLoaded", function () {
        document.title = "SIGES";
        document.documentElement.classList.remove("dark");
        document.documentElement.classList.add("light");
    });
})();

