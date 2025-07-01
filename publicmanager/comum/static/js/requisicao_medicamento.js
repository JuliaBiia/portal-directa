Array.from(document.querySelectorAll("#status_1")).forEach(
    element => {
        element.classList.add("badge")
        element.classList.add("rounded-pill")
        element.classList.add("bg-primary")
    }
)

Array.from(document.querySelectorAll("#status_2")).forEach(
    element => {
        element.classList.add("badge")
        element.classList.add("rounded-pill")
        element.classList.add("bg-warning")
    }
)

Array.from(document.querySelectorAll("#status_3")).forEach(
    element => {
        element.classList.add("badge")
        element.classList.add("rounded-pill")
        element.classList.add("bg-success")
    }
)

Array.from(document.querySelectorAll("#status_3")).forEach(
    element => {
        element.classList.add("badge")
        element.classList.add("rounded-pill")
        element.classList.add("bg-danger")
    }
)