function getArea(category) {
    const li = document.createElement("li")
    li.classList.add("mb-1")

    const textId = `category-${category.id}`
    const parentId = `category-${category.parent}`

    if (category.parent == null) {
        const button = document.createElement("button")
        button.classList.add("btn", "btn-toggle", "border", "border-0", "text-black")

        if (!isManageMode) {
            button.setAttribute("data-bs-toggle", "collapse")
        }

        button.setAttribute("data-bs-target", "#" + textId)

        if (isManageMode) {
            button.setAttribute("aria-expanded", "true")
        } else {
            button.setAttribute("aria-expanded", "false")
        }

        button.innerText = category.text

        button.addEventListener("click", () => {
            if (isManageMode) {
                categorySelectForManageTool(category.id)
            }
        })

        li.appendChild(button)

        const text = document.createElement("div")
        text.id = textId
        text.classList.add("collapse")
        text.setAttribute("data-bs-parent", "#display")

        if (isManageMode) {
            text.classList.add("show")
        }

        li.appendChild(text)

        const ul = document.createElement("ul")
        ul.classList.add("btn-toggle-nav", "list-unstyled", "fw-normal", "pb-1", "small")

        text.appendChild(ul)
    } else {
        const ul = document.querySelector(`#${parentId} > ul`)

        const li = document.createElement("li")
        ul.appendChild(li)

        const button = document.createElement("button")
        button.id = `category-${category.id}`
        button.innerText = category.text
        button.dataset.parentId = parentId

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
const isManageMode = window.categoryManage ?? false

document.addEventListener("DOMContentLoaded", () => {
    let style = document.createElement("link")
    style.rel = "stylesheet"
    style.href = "/static/category/style.css"

    document.head.appendChild(style)

    fetch("/category")
        .then((resp) => resp.json())
        .then((json) => {
            // '카테고리 없음' 카테고리 렌더링
            if (!isManageMode) {
                const ul = document.createElement("ul")
                ul.classList.add("btn-toggle-nav", "list-unstyled", "fw-normal", "pb-1", "small")

                const li = document.createElement("li")
                ul.appendChild(li)

                const button = document.createElement("button")
                button.id = "null"
                button.innerText = "카테고리 없음"

                button.addEventListener("click", () => {
                    alert("페이지 이동")
                })

                li.appendChild(button)
                display.appendChild(ul)
            }

            // 상위 카테고리 렌더링
            json.filter((x) => x.parent == null).forEach((category) => {
                getArea(category)
            })

            // 하위 카테고리 렌더링
            json.filter((x) => x.parent != null).forEach((category) => {
                getArea(category)
            })
        })
})
