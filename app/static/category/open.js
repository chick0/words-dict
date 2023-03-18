function searchCategory(id) {
    const elementId = id == null ? "null" : `category-${id}`
    let element = document.getElementById(elementId)

    let tryToGetElement = setInterval(() => {
        if (element == null) {
            console.warn("카테고리 버튼 찾을 수 없습니다...")
            element = document.getElementById(elementId)
        } else {
            clearInterval(tryToGetElement)

            if (id == null) {
                selectCategory(element)
            } else {
                openCategory(element)
            }
        }
    }, 100)
}

function openCategory(element) {
    function openCollapse(target) {
        target.parentNode.querySelector("button").setAttribute("aria-expanded", "true")
        target.classList.add("show")
    }

    const parent = document.getElementById(element.dataset.parentId)

    if (parent == null) {
        openCollapse(element)
        selectCategory(element.querySelector("button"))
    } else {
        openCollapse(parent)
        selectCategory(element)
    }
}

function selectCategory(element) {
    element.classList.add("is-focused")
}
