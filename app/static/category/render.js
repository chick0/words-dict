function getArea(category) {
    const li = document.createElement("li")
    li.classList.add("mb-1")

    const textId = `category-text-${category.id}`
    const parentId = `category-text-${category.parent}`
    const isManageMode = window.categoryManage ?? false

    console.log("cat: render->getArea", category)

    if (category.parent == null) {
        const button = document.createElement("button")
        button.classList.add("btn", "btn-toggle", "border", "border-0", "text-black")

        if (!isManageMode) button.setAttribute("data-bs-toggle", "collapse")

        button.setAttribute("data-bs-target", "#" + textId)
        button.setAttribute("aria-expanded", "true")

        button.innerText = category.text

        button.addEventListener("click", () => {
            if (isManageMode) {
                categorySelectForManageTool(category.id)
            }
        })

        li.appendChild(button)

        const text = document.createElement("div")
        text.id = textId
        text.classList.add("collapse", "show")
        text.setAttribute("data-bs-parent", "#display")

        li.appendChild(text)

        const ul = document.createElement("ul")
        ul.classList.add("btn-toggle-nav", "list-unstyled", "fw-normal", "pb-1", "small")

        text.appendChild(ul)
    } else {
        const ul = document.querySelector(`#${parentId} > ul`)

        const li = document.createElement("li")
        ul.appendChild(li)

        const button = document.createElement("button")
        button.innerText = category.text

        button.addEventListener("click", () => {
            if (isManageMode) {
                categorySelectForManageTool(category.id)
            } else {
                alert("페이지 이동")
            }
        })

        li.appendChild(button)
    }

    display.appendChild(li)
}

const display = document.getElementById("display")

document.addEventListener("DOMContentLoaded", () => {
    let style = document.createElement("link")
    style.rel = "stylesheet"
    style.href = "/static/category/style.css"

    document.head.appendChild(style)

    fetch("/category")
        .then((resp) => resp.json())
        .then((json) => {
            // 상위 카테고리 렌더링
            json.filter(x => x.parent == null).forEach((category) => {
                getArea(category)
            })

            // 하위 카테고리 렌더링
            json.filter(x => x.parent != null).forEach((category) => {
                getArea(category)
            })
        })
})
