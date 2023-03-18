function getButton(category) {
    const button = document.createElement("button")

    if (category.id == null) {
        button.id = "null"
    } else {
        button.id = `category-${category.id}`
    }

    button.innerText = category.text
    button.dataset.parentId = `category-${category.parent}`

    button.addEventListener("click", () => {
        if (isManageMode) {
            categorySelectForManageTool(category.id)
        } else {
            let href = "/category/area/"

            if (category.id == null) {
                href += "-"
            } else {
                let parent = document.getElementById(button.dataset.parentId).parentElement.querySelector("button")
                href += parent.innerText

                if (category.id > 0) {
                    href += "/" + category.text
                }
            }

            location.href = href
        }
    })

    return button
}

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

        if (isManageMode) {
            button.addEventListener("click", () => {
                categorySelectForManageTool(category.id)
            })
        }

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

        if (!isManageMode) {
            const li = document.createElement("li")
            ul.appendChild(li)

            li.appendChild(
                getButton({
                    id: -category.id,
                    text: "하위 카테고리 없음",
                    parent: category.id,
                })
            )
        }

        text.appendChild(ul)
    } else {
        const ul = document.querySelector(`#${parentId} > ul`)

        const li = document.createElement("li")
        ul.appendChild(li)

        li.appendChild(getButton(category))
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
                const liParent = document.createElement("li")
                liParent.classList.add("mb-1")
                display.appendChild(liParent)

                const ul = document.createElement("ul")
                ul.classList.add("btn-toggle-nav", "list-unstyled", "fw-normal", "pb-1", "small")
                liParent.appendChild(ul)

                const li = document.createElement("li")
                ul.appendChild(li)

                li.appendChild(
                    getButton({
                        id: null,
                        text: "카테고리 없음",
                        parent: null,
                    })
                )
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
